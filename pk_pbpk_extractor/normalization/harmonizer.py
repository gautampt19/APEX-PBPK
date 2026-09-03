"""
pk_pbpk_extractor/normalization/harmonizer.py
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Merges and deduplicates PK parameter records from multiple extraction passes.

Priority order (highest confidence → lowest):
    xml_table  >  colpali_page  >  prose_pass

Records with the same PBPKO canonical name + species + route are considered
the same parameter. When conflicts exist, the higher-priority source wins.
Conflicts are logged for review.
"""
from __future__ import annotations
import logging
from typing import List, Tuple, Optional, Any

from .entity_linker import link_pk_entity
from .unit_normalizer import normalize_unit

logger = logging.getLogger(__name__)

# Source pass priority (higher index = higher confidence)
_PRIORITY = {"prose_pass": 0, "colpali_page": 1, "xml_table": 2}

# A single normalized parameter record
ParamRecord = Tuple[
    str,    # paper_id
    str,    # table_id / source chunk
    str,    # species
    str,    # formulation
    str,    # route
    Optional[float],  # dose
    str,    # parameter_name (raw)
    str,    # canonical_name (PBPKO)
    Optional[float],  # value
    Optional[float],  # deviation_value
    str,    # measure_type
    str,    # unit
    str,    # source_pass
]


def _record_key(rec: ParamRecord) -> str:
    """Generate dedup key from canonical name + species + route."""
    _, _, species, _, route, _, _, canonical, _, _, _, _, _ = rec
    return f"{canonical}|{species.lower()}|{route.lower()}"


def harmonize(records: List[ParamRecord]) -> List[ParamRecord]:
    """
    Merge and deduplicate a list of parameter records from all passes.

    Steps:
    1. Normalise each record's canonical name and unit.
    2. Group by dedup key (canonical + species + route).
    3. Within each group, keep the record from the highest-priority source.
    4. Log any conflicts (same canonical, different numeric value).

    Returns the harmonised list sorted by canonical_name.
    """
    # Re-normalise canonical names + units (in case something slipped through)
    normalised: List[ParamRecord] = []
    for rec in records:
        (paper_id, table_id, species, formulation, route, dose,
         raw_name, canonical, value, deviation, measure_type, unit,
         source_pass) = rec

        new_canonical = link_pk_entity(raw_name) or canonical or raw_name
        new_unit = normalize_unit(unit)

        normalised.append((
            paper_id, table_id, species, formulation, route, dose,
            raw_name, new_canonical, value, deviation, measure_type,
            new_unit, source_pass
        ))

    # Group by key, keeping track of all candidates
    groups: dict[str, List[ParamRecord]] = {}
    for rec in normalised:
        key = _record_key(rec)
        groups.setdefault(key, []).append(rec)

    result: List[ParamRecord] = []
    for key, candidates in groups.items():
        if len(candidates) == 1:
            result.append(candidates[0])
            continue

        # Sort by priority desc
        candidates.sort(
            key=lambda r: _PRIORITY.get(r[12], 0),
            reverse=True
        )
        winner = candidates[0]

        # Check for value conflicts
        values_by_source = [
            (c[12], c[8]) for c in candidates if c[8] is not None
        ]
        unique_values = set(v for _, v in values_by_source if v is not None)
        if len(unique_values) > 1:
            logger.info(
                "Conflict for '%s': %s — keeping %s (priority %d)",
                key,
                [(s, v) for s, v in values_by_source],
                winner[12],
                _PRIORITY.get(winner[12], 0),
            )

        result.append(winner)

    # Sort final list by canonical_name for clean output
    result.sort(key=lambda r: r[7])
    logger.info("Harmonizer: %d raw records → %d harmonised", len(records), len(result))
    return result
