"""Fetch AlphaFold DB and UniProt data, with a simple on-disk cache.

Uses only the standard library. AlphaFold DB file downloads are refused (HTTP 403)
when no User-Agent is sent, so every request sets one.
"""
from __future__ import annotations

import json
import os
import urllib.error
import urllib.request
from dataclasses import dataclass, field
from pathlib import Path

from . import __version__

USER_AGENT = f"af-confidence/{__version__} (+https://github.com/wangnick1004/af-confidence)"
AFDB_API = "https://alphafold.ebi.ac.uk/api/prediction/{acc}"
UNIPROT_API = ("https://rest.uniprot.org/uniprotkb/{acc}.json"
               "?fields=ft_init_met,ft_signal,ft_chain,ft_propep,ft_transit,sequence")


class SourceError(RuntimeError):
    """Raised when data cannot be fetched or is not available offline."""


@dataclass
class Model:
    entry_id: str          # e.g. AF-P04637-F1
    accession: str         # UniProt accession of the modelled sequence, e.g. P04637 or P04637-2
    version: int
    sequence: str
    start: int             # first residue number covered by the model (usually 1)
    confidence_url: str
    plddt: dict[int, float] | None = None


@dataclass
class ProteinData:
    accession: str
    models: list[Model]                    # canonical first, then isoforms
    processing: list[tuple[str, int, int, str]] = field(default_factory=list)
    # (feature type, start, end, description) for Initiator methionine, Signal, Chain, ...

    @property
    def canonical(self) -> Model:
        return self.models[0]


def default_cache_dir() -> Path:
    base = os.environ.get("XDG_CACHE_HOME") or os.path.join(os.path.expanduser("~"), ".cache")
    return Path(base) / "af-confidence"


class Client:
    def __init__(self, cache_dir: Path | str | None = None, offline: bool = False, timeout: float = 30):
        self.cache_dir = Path(cache_dir) if cache_dir else default_cache_dir()
        self.offline = offline
        self.timeout = timeout

    # -- low level -------------------------------------------------------
    def _get_json(self, url: str, cache_name: str):
        path = self.cache_dir / cache_name
        if path.exists():
            with open(path, encoding="utf-8") as fh:
                return json.load(fh)
        if self.offline:
            raise SourceError(f"offline mode: {cache_name} is not in the cache ({self.cache_dir})")
        req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT, "Accept": "application/json"})
        try:
            with urllib.request.urlopen(req, timeout=self.timeout) as resp:
                data = json.loads(resp.read().decode("utf-8"))
        except urllib.error.HTTPError as exc:
            if exc.code == 404:
                raise SourceError(f"not found: {url}") from None
            raise SourceError(f"HTTP {exc.code} for {url}") from None
        except urllib.error.URLError as exc:
            raise SourceError(f"cannot reach {url}: {exc.reason}") from None
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        with open(path, "w", encoding="utf-8") as fh:
            json.dump(data, fh)
        return data

    # -- AlphaFold DB ----------------------------------------------------
    def models(self, accession: str) -> list[Model]:
        try:
            entries = self._get_json(AFDB_API.format(acc=accession), f"api_{accession}.json")
        except SourceError as exc:
            if str(exc).startswith("not found"):
                raise SourceError(f"{accession}: no AlphaFold DB model found") from None
            raise
        models = []
        for e in entries:
            models.append(Model(
                entry_id=e["modelEntityId"],
                accession=e.get("uniprotAccession", ""),
                version=int(e["latestVersion"]),
                sequence=e["sequence"],
                start=int(e.get("sequenceStart", 1)),
                confidence_url=e["plddtDocUrl"],
            ))
        if not models:
            raise SourceError(f"{accession}: no AlphaFold DB model found")
        # canonical entry (accession without isoform suffix) first
        models.sort(key=lambda m: (m.accession != accession, m.accession))
        return models

    def load_plddt(self, model: Model) -> dict[int, float] | None:
        """Per-residue pLDDT; returns None if unavailable (e.g. offline and not cached)."""
        if model.plddt is None:
            name = f"{model.entry_id}-confidence_v{model.version}.json"
            try:
                conf = self._get_json(model.confidence_url, name)
            except SourceError:
                return None
            model.plddt = dict(zip(conf["residueNumber"], conf["confidenceScore"]))
        return model.plddt

    # -- UniProt ---------------------------------------------------------
    def processing_features(self, accession: str) -> list[tuple[str, int, int, str]]:
        try:
            d = self._get_json(UNIPROT_API.format(acc=accession), f"uniprot_{accession}.json")
        except SourceError:
            return []
        out = []
        for f in d.get("features", []):
            loc = f.get("location", {})
            try:
                start, end = int(loc["start"]["value"]), int(loc["end"]["value"])
            except (KeyError, TypeError, ValueError):
                continue
            out.append((f.get("type", ""), start, end, f.get("description", "")))
        return out

    def protein(self, accession: str) -> ProteinData:
        accession = accession.strip()
        return ProteinData(accession, self.models(accession), self.processing_features(accession))
