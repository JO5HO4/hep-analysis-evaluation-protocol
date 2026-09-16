"""Public categorization API for the hadronic top-associated H->gamma gamma study.

All momenta are expressed in GeV.  The classifier intentionally uses exactly the
five variables listed in :data:`BDT_FEATURES`; the diphoton mass is bookkeeping
only and is never a classifier input.
"""

from __future__ import annotations

import hashlib
import math
from typing import Any, Iterable, Mapping, Sequence

import numpy as np


BDT_FEATURES = [
    "n_central_jets",
    "n_bjets",
    "jet1_pt",
    "jet_ht",
    "diphoton_pt",
]

CATEGORY_ORDER = [
    "ttH_had_BDT1",
    "ttH_had_BDT2",
    "ttH_had_BDT3",
    "ttH_had_BDT4",
    "tH_had_4j1b",
    "tH_had_4j2b",
]


def _value(obj: Any, name: str, default: Any = None) -> Any:
    if isinstance(obj, Mapping):
        return obj.get(name, default)
    return getattr(obj, name, default)


def build_jet_features(
    jets: Iterable[Any], pt_min: float = 25.0, central_eta_max: float = 2.5,
    btag_quantile_min: int = 4,
) -> dict[str, float]:
    """Build deterministic jet features from dict-like or attribute-like jets.

    The b-tag definition is ``jet_btag_quantile >= 4`` by default.  Central and
    forward counts use the selected jets after the 25 GeV requirement.
    """
    selected = [j for j in jets if float(_value(j, "pt", 0.0)) > pt_min]
    selected.sort(key=lambda j: float(_value(j, "pt", 0.0)), reverse=True)
    central = [j for j in selected if abs(float(_value(j, "eta", 999.0))) <= central_eta_max]
    forward = [j for j in selected if abs(float(_value(j, "eta", 999.0))) > central_eta_max]
    bjets = [j for j in selected if int(_value(j, "btag_quantile", 0)) >= btag_quantile_min]
    return {
        "n_jets": float(len(selected)),
        "n_central_jets": float(len(central)),
        "n_forward_jets": float(len(forward)),
        "n_bjets": float(len(bjets)),
        "jet1_pt": float(_value(selected[0], "pt", 0.0)) if selected else 0.0,
        "jet_ht": float(sum(float(_value(j, "pt", 0.0)) for j in selected)),
    }


def invariant_mass(objects: Iterable[Any]) -> float:
    """Return invariant mass from objects containing pt/eta/phi and e (GeV)."""
    px = py = pz = energy = 0.0
    for obj in objects:
        pt = float(_value(obj, "pt", 0.0))
        eta = float(_value(obj, "eta", 0.0))
        phi = float(_value(obj, "phi", 0.0))
        px += pt * math.cos(phi)
        py += pt * math.sin(phi)
        pz += pt * math.sinh(eta)
        energy += float(_value(obj, "e", pt * math.cosh(eta)))
    return math.sqrt(max(energy * energy - px * px - py * py - pz * pz, 0.0))


def stable_partition(
    event_id: Any, seed: int = 240513, fractions: Sequence[float] = (0.60, 0.20, 0.20),
) -> str:
    """Map a stable event identifier to train/validation/test using SHA-256."""
    if len(fractions) != 3 or any(x < 0 for x in fractions) or not math.isclose(sum(fractions), 1.0):
        raise ValueError("fractions must contain three non-negative values summing to one")
    digest = hashlib.sha256(f"{seed}:{event_id}".encode("utf-8")).digest()
    u = int.from_bytes(digest[:8], "big") / float(2**64)
    if u < fractions[0]:
        return "train"
    if u < fractions[0] + fractions[1]:
        return "validation"
    return "test"


def assign_top_category(event: Any, score: float | None = None, thresholds: Any = None) -> str:
    """Assign the priority-ordered hadronic category, or ``unassigned``.

    BDT regions are evaluated first.  The two cut-based tH regions are evaluated
    only below the minimum BDT threshold.  Exactly four *central* jets are used
    for those cuts, independent of the total selected-jet multiplicity.
    """
    hadronic = bool(_value(event, "hadronic_preselection", False))
    if not hadronic:
        return "unassigned"
    if score is None:
        score = _value(event, "bdt_score", None)
    if thresholds is None:
        thresholds = {"minimum": 1.0, "split_boundaries_desc": []}
    minimum = float(_value(thresholds, "minimum", 1.0))
    splits = sorted([float(x) for x in _value(thresholds, "split_boundaries_desc", [])], reverse=True)
    if score is not None and math.isfinite(float(score)) and float(score) >= minimum:
        index = sum(float(score) < boundary for boundary in splits)
        if index < 4:
            return f"ttH_had_BDT{index + 1}"
    nlep = int(_value(event, "n_leptons", 0))
    ncj = int(_value(event, "n_central_jets", 0))
    nb = int(_value(event, "n_bjets", 0))
    if nlep == 0 and ncj == 4 and nb == 1:
        return "tH_had_4j1b"
    if nlep == 0 and ncj == 4 and nb >= 2:
        return "tH_had_4j2b"
    return "unassigned"


def _asimov_z(signal: float, background: float) -> float:
    signal, background = max(float(signal), 0.0), max(float(background), 0.0)
    if signal <= 0 or background <= 0:
        return 0.0
    return math.sqrt(max(2.0 * ((signal + background) * math.log1p(signal / background) - signal), 0.0))


def optimize_bdt_boundaries(rows: Any, config: Mapping[str, Any] | None = None) -> dict[str, Any]:
    """Iteratively optimize up to four score bins using physical yield weights.

    ``rows`` may be a pandas DataFrame or an iterable of mappings.  Expected
    columns are ``bdt_score``, ``is_signal`` and ``optimization_weight``.  The
    first threshold defines the inclusive BDT region; each subsequent boundary
    is accepted only when the combined quadrature Asimov significance improves
    by at least five percent (configurable through ``minimum_relative_improvement``).
    """
    cfg = {
        "minimum_relative_improvement": 0.05,
        "max_categories": 4,
        "minimum_background": 0.8,
        "candidate_quantiles": 80,
    }
    if config:
        cfg.update(dict(config))
    if hasattr(rows, "to_dict"):
        records = rows.to_dict("records")
    else:
        records = list(rows)
    score = np.asarray([float(_value(r, "bdt_score", np.nan)) for r in records])
    signal_mask = np.asarray([bool(_value(r, "is_signal", False)) for r in records])
    weight = np.asarray([float(_value(r, "optimization_weight", 0.0)) for r in records])
    finite = np.isfinite(score) & np.isfinite(weight)
    score, signal_mask, weight = score[finite], signal_mask[finite], weight[finite]
    if len(score) == 0:
        return {"minimum": 1.0, "split_boundaries_desc": [], "accepted_splits": [], "stop_reason": "no_finite_rows"}
    # Signed MC bookkeeping is retained upstream.  A negative aggregate yield is
    # non-physical for a counting objective, so per-region aggregates are clipped.
    def yields(lo: float, hi: float) -> tuple[float, float]:
        mask = (score >= lo) & (score < hi)
        return max(weight[mask & signal_mask].sum(), 0.0), max(weight[mask & ~signal_mask].sum(), 0.0)

    candidates = np.unique(np.quantile(score, np.linspace(0.02, 0.92, int(cfg["candidate_quantiles"]))))
    candidates = candidates[(candidates > 0.0) & (candidates < 1.0)]
    base_options: list[tuple[float, float, float, float]] = []
    for low in candidates:
        s, b = yields(float(low), 1.0000001)
        if b >= float(cfg["minimum_background"]):
            base_options.append((_asimov_z(s, b), float(low), s, b))
    if base_options:
        z0, minimum, s0, b0 = max(base_options, key=lambda x: (x[0], -x[1]))
    else:
        minimum = float(np.min(score))
        s0, b0 = yields(minimum, 1.0000001)
        z0 = _asimov_z(s0, b0)
    accepted: list[dict[str, Any]] = [{
        "iteration": 1, "boundary": minimum, "kind": "minimum_score",
        "combined_expected_z": z0, "relative_improvement": None,
        "signal": s0, "background": b0,
    }]
    edges = [minimum, 1.0000001]
    previous = z0
    stop_reason = "maximum_categories_reached"
    while len(edges) - 1 < int(cfg["max_categories"]):
        best = None
        for boundary in candidates:
            boundary = float(boundary)
            if boundary <= minimum or any(abs(boundary - e) < 1e-12 for e in edges):
                continue
            trial = sorted(edges + [boundary])
            parts = [yields(trial[i], trial[i + 1]) for i in range(len(trial) - 1)]
            if any(b < float(cfg["minimum_background"]) for _, b in parts):
                continue
            z = math.sqrt(sum(_asimov_z(s, b) ** 2 for s, b in parts))
            if best is None or z > best[0]:
                best = (z, boundary, parts)
        if best is None:
            stop_reason = "no_valid_additional_boundary"
            break
        z, boundary, parts = best
        relative = (z - previous) / previous if previous > 0 else (math.inf if z > 0 else 0.0)
        if relative < float(cfg["minimum_relative_improvement"]):
            stop_reason = "best_relative_improvement_below_5_percent"
            break
        edges = sorted(edges + [boundary])
        accepted.append({
            "iteration": len(edges) - 1, "boundary": boundary, "kind": "split",
            "combined_expected_z": z, "relative_improvement": relative,
            "bin_yields_low_to_high": [{"signal": s, "background": b} for s, b in parts],
        })
        previous = z
    return {
        "minimum": float(minimum),
        "split_boundaries_desc": sorted([x for x in edges if minimum < x < 1.0], reverse=True),
        "accepted_splits": accepted,
        "minimum_relative_improvement": float(cfg["minimum_relative_improvement"]),
        "maximum_categories": int(cfg["max_categories"]),
        "stop_reason": stop_reason,
        "final_combined_expected_z": previous,
    }
