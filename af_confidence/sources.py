"""Fetch AlphaFold DB and UniProt data, with a simple on-disk cache.

Uses only the standard library. AlphaFold DB file downloads are refused (HTTP 403)
when no User-Agent is sent, so every request sets one.
"""
from __future__ import annotations

import json
import os
import re
import tempfile
import time
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass, field
from pathlib import Path

from . import __version__

USER_AGENT = f"af-confidence/{__version__} (+https://github.com/wangnick1004/af-confidence)"
AFDB_API = "https://alphafold.ebi.ac.uk/api/prediction/{acc}"
UNIPROT_ENTRY = ("https://rest.uniprot.org/uniprotkb/{acc}.json"
                 "?fields=ft_init_met,ft_signal,ft_chain,ft_peptide,ft_propep,ft_transit,sequence")
UNIPROT_SEARCH = "https://rest.uniprot.org/uniprotkb/search?{query}"

HUMAN = 9606
RETRIES = 3                  # attempts per request
RETRY_STATUS = {429, 500, 502, 503, 504}

# UniProt accession, optionally with an isoform suffix (P04637-2)
_ACCESSION = re.compile(
    r"^(?:[OPQ][0-9][A-Z0-9]{3}[0-9]|[A-NR-Z][0-9](?:[A-Z][A-Z0-9]{2}[0-9]){1,2})(?:-\d+)?$")
_GENE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]{0,29}$")


class SourceError(RuntimeError):
    """Raised when data cannot be fetched or is not available offline."""


class NotFound(SourceError):
    """The remote service has no record for the request."""


class NotCached(SourceError):
    """Offline mode and the file is not in the cache."""


@dataclass
class Model:
    entry_id: str          # e.g. AF-P04637-F1
    accession: str         # UniProt accession of the modelled sequence, e.g. P04637 or P04637-2
    version: int
    sequence: str
    start: int             # first residue number covered by the model (usually 1)
    confidence_url: str
    uniprot_sequence_matches: bool = True
    plddt: dict[int, float] | None = None


@dataclass
class ProteinData:
    query: str                             # what the user typed (accession or gene name)
    accession: str                         # resolved UniProt accession
    models: list[Model]                    # requested model first, then the other isoforms
    processing: list[tuple[str, int, int, str]] = field(default_factory=list)
    # (feature type, start, end, description) for Initiator methionine, Signal, Chain, ...
    warnings: list[str] = field(default_factory=list)

    @property
    def canonical(self) -> Model:
        """The model the variants are checked against (the requested accession)."""
        return self.models[0]


def is_accession(text: str) -> bool:
    return bool(_ACCESSION.match(text.strip().upper()))


def default_cache_dir() -> Path:
    base = os.environ.get("XDG_CACHE_HOME") or os.path.join(os.path.expanduser("~"), ".cache")
    return Path(base) / "af-confidence"


class Client:
    def __init__(self, cache_dir: Path | str | None = None, offline: bool = False,
                 timeout: float = 30, organism: int = HUMAN, retry_wait: float = 1.0):
        self.cache_dir = Path(cache_dir) if cache_dir else default_cache_dir()
        self.offline = offline
        self.timeout = timeout
        self.organism = organism
        self.retry_wait = retry_wait

    # -- low level -------------------------------------------------------
    def _download(self, url: str):
        """GET a JSON document, retrying transient failures."""
        req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT,
                                                   "Accept": "application/json"})
        last = ""
        for attempt in range(RETRIES):
            if attempt:
                time.sleep(self.retry_wait * 2 ** (attempt - 1))
            try:
                with urllib.request.urlopen(req, timeout=self.timeout) as resp:
                    return json.loads(resp.read().decode("utf-8"))
            except urllib.error.HTTPError as exc:
                if exc.code in (400, 404):
                    raise NotFound(url) from None
                if exc.code not in RETRY_STATUS:
                    raise SourceError(f"HTTP {exc.code} from {_host(url)}") from None
                last = f"HTTP {exc.code}"
            except urllib.error.URLError as exc:
                last = str(exc.reason)
            except (TimeoutError, OSError) as exc:      # socket timeout, connection reset
                last = str(exc) or type(exc).__name__
            except ValueError:
                last = "invalid JSON in response"
        raise SourceError(f"cannot get data from {_host(url)} after {RETRIES} attempts ({last}); "
                          f"check your network, or use --offline with a cache")

    def _get_json(self, url: str, cache_name: str):
        path = self.cache_dir / cache_name
        if path.exists():
            try:
                with open(path, encoding="utf-8") as fh:
                    return json.load(fh)
            except ValueError:
                if self.offline:
                    raise SourceError(f"cached file {path} is corrupt; run once without "
                                      f"--offline to refresh it") from None
                path.unlink()                      # corrupt cache: fetch again
        if self.offline:
            raise NotCached(f"offline mode: {cache_name} is not in the cache ({self.cache_dir})")
        data = self._download(url)
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        fd, tmp = tempfile.mkstemp(dir=self.cache_dir, suffix=".tmp")
        with os.fdopen(fd, "w", encoding="utf-8") as fh:
            json.dump(data, fh)
        os.replace(tmp, path)                      # atomic: no half-written cache files
        return data

    # -- name resolution -------------------------------------------------
    def resolve(self, query: str) -> str:
        """Turn an accession or a gene name into a UniProt accession."""
        q = query.strip()
        if is_accession(q):
            return q.upper()
        if not _GENE.match(q):
            raise SourceError(f"{query!r} is neither a UniProt accession nor a gene name")
        params = urllib.parse.urlencode({
            "query": f"gene_exact:{q} AND organism_id:{self.organism} AND reviewed:true",
            "fields": "accession,gene_primary", "format": "json", "size": "10"})
        cache = f"gene_{self.organism}_{q.upper()}.json"
        data = self._get_json(UNIPROT_SEARCH.format(query=params), cache)
        hits = []
        for r in data.get("results", []):
            genes = r.get("genes") or [{}]
            primary = genes[0].get("geneName", {}).get("value", "")
            hits.append((r["primaryAccession"], primary))
        if not hits:
            raise SourceError(f"gene {q!r}: no reviewed UniProt entry for organism {self.organism}"
                              f"{'' if self.organism != HUMAN else ' (human)'}; "
                              f"use a UniProt accession or --organism")
        exact = [h for h in hits if h[1].upper() == q.upper()]
        if len(exact) == 1:
            return exact[0][0]
        if len(hits) == 1:
            return hits[0][0]
        listing = ", ".join(f"{a} ({g})" for a, g in hits)
        raise SourceError(f"gene {q!r} is ambiguous: {listing}; use a UniProt accession")

    # -- AlphaFold DB ----------------------------------------------------
    def _entries(self, accession: str) -> list[dict]:
        try:
            return self._get_json(AFDB_API.format(acc=accession), f"api_{accession}.json")
        except NotFound:
            return []

    def models(self, accession: str) -> list[Model]:
        base = accession.split("-")[0]
        entries = self._entries(base)
        if accession != base and not any(e.get("uniprotAccession") == accession for e in entries):
            entries = entries + self._entries(accession)
        models, seen = [], set()
        for e in entries:
            if e["modelEntityId"] in seen or e.get("entityType", "protein") != "protein":
                continue
            seen.add(e["modelEntityId"])
            models.append(Model(
                entry_id=e["modelEntityId"],
                accession=e.get("uniprotAccession", ""),
                version=int(e["latestVersion"]),
                sequence=e["sequence"],
                start=int(e.get("sequenceStart", 1)),
                confidence_url=e["plddtDocUrl"],
                uniprot_sequence_matches=e.get("uniprotSequence", e["sequence"]) == e["sequence"],
            ))
        target = [m for m in models if m.accession == accession]
        if not target:
            raise SourceError(f"{accession}: no AlphaFold DB model (AlphaFold DB does not cover "
                              f"every protein, e.g. some very long ones)")
        rest = sorted((m for m in models if m.accession != accession),
                      key=lambda m: (m.accession != base, m.accession))
        return target[:1] + rest

    def load_plddt(self, model: Model) -> dict[int, float] | None:
        """Per-residue pLDDT; returns None if unavailable (e.g. offline and not cached)."""
        if model.plddt is None:
            name = f"{model.entry_id}-confidence_v{model.version}.json"
            try:
                conf = self._get_json(model.confidence_url, name)
                model.plddt = dict(zip(conf["residueNumber"], conf["confidenceScore"]))
            except (SourceError, KeyError, TypeError):
                return None
        return model.plddt

    # -- UniProt ---------------------------------------------------------
    def _features(self, accession: str) -> tuple[list[tuple[str, int, int, str]], str]:
        """Processing features and sequence; raises NotCached/SourceError if unavailable."""
        try:
            d = self._get_json(UNIPROT_ENTRY.format(acc=accession), f"uniprot_{accession}.json")
        except NotFound:
            return [], ""
        out = []
        for f in d.get("features", []):
            loc = f.get("location", {})
            try:
                start, end = int(loc["start"]["value"]), int(loc["end"]["value"])
            except (KeyError, TypeError, ValueError):
                continue
            out.append((f.get("type", ""), start, end, f.get("description", "")))
        return out, d.get("sequence", {}).get("value", "")

    def processing_features(self, accession: str) -> list[tuple[str, int, int, str]]:
        feats, seq = self._features(accession)
        base = accession.split("-")[0]
        if feats or accession == base:
            return feats
        # UniProt annotates processing on the canonical entry only. N-terminal features
        # (initiator Met, signal/transit peptide, propeptide starting at 1) carry over to an
        # isoform when the isoform's N-terminus is identical over that stretch.
        base_feats, base_seq = self._features(base)
        return [f for f in base_feats
                if f[1] == 1 and f[0] in ("Initiator methionine", "Signal", "Transit peptide",
                                          "Propeptide")
                and seq and base_seq and seq[:f[2] + 1] == base_seq[:f[2] + 1]]

    def protein(self, query: str) -> ProteinData:
        accession = self.resolve(query)
        models = self.models(accession)
        warnings = []
        try:
            processing = self.processing_features(accession)
        except SourceError as exc:
            processing = []
            warnings.append(f"UniProt processing annotations unavailable ({exc}); "
                            f"annotated offsets were not checked")
        if not models[0].uniprot_sequence_matches:
            warnings.append(f"the AlphaFold DB model {models[0].entry_id} was built on an older "
                            f"UniProt sequence; positions are checked against the model sequence")
        return ProteinData(query.strip(), accession, models, processing, warnings)


def _host(url: str) -> str:
    return urllib.parse.urlsplit(url).netloc
