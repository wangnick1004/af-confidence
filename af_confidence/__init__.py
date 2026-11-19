"""Map literature protein variants onto AlphaFold DB models and catch numbering mistakes.

Python interface (see ``af_confidence.api`` for details)::

    import af_confidence as afc
    reports = afc.check_list({"HBB": ["E6V"], "SERPINA1": ["E342K", "E264V"]})
    afc.to_dataframe(reports)
"""

__version__ = "0.1.0"

from .api import (afdb_tracks, best_suggestions, check, check_list, chimerax_script,  # noqa: E402
                  to_dataframe, to_records, to_text)
from .inputs import InputError  # noqa: E402
from .mapper import ProteinReport, Result, Suggestion  # noqa: E402
from .sources import Client, SourceError  # noqa: E402
from .variants import Variant, VariantParseError, parse_variant  # noqa: E402

__all__ = [
    "__version__", "check", "check_list", "to_text", "to_records", "to_dataframe", "afdb_tracks",
    "chimerax_script", "best_suggestions", "ProteinReport", "Result", "Suggestion", "Variant",
    "Client", "InputError", "SourceError", "VariantParseError", "parse_variant",
]
