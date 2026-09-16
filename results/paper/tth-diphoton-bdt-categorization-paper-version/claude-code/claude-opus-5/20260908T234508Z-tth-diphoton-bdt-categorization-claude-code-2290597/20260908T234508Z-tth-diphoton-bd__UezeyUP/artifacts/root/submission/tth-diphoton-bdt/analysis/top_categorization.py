"""Callable API for the top-associated H -> gamma gamma diphoton BDT categorization.

This module holds the *definitions* of the analysis: the object-level feature
builders, the diphoton kinematics, the stable train/val/test partitioning, the
category priority order and the greedy BDT-boundary optimizer.

Everything here is pure python / numpy and free of I/O so that it can be
imported and unit-tested on its own.  The vectorised pipeline in
``analysis.preselection`` reproduces the same definitions on awkward arrays and
is cross-checked against the scalar implementations below at run time
(see ``analysis.preselection.crosscheck_scalar_vs_vectorised``).
"""

from __future__ import annotations

import hashlib
import math
from typing import Any, Iterable, Mapping, Sequence

import numpy as np

__all__ = [
    "CATEGORY_ORDER",
    "HADRONIC_BDT_CATEGORIES",
    "CUTBASED_HADRONIC_CATEGORIES",
    "LEGACY_LEPTONIC_CATEGORIES",
    "BDT_FEATURES",
    "OBJECT_SELECTION",
    "MASS_WINDOWS",
    "build_jet_features",
    "build_lepton_features",
    "photon_kinematic_acceptance",
    "invariant_mass",
    "diphoton_features",
    "assign_top_category",
    "stable_partition",
    "optimize_bdt_boundaries",
    "counting_significance",
    "combined_significance",
]


# --------------------------------------------------------------------------
# Categories
# --------------------------------------------------------------------------

#: Hadronic BDT categories, tightest (highest BDT score) first.
HADRONIC_BDT_CATEGORIES = (
    "ttH_had_BDT1",
    "ttH_had_BDT2",
    "ttH_had_BDT3",
    "ttH_had_BDT4",
)

#: Cut-based hadronic tH categories.  These are *lower priority* than every
#: hadronic BDT category and are only evaluated once an event has failed all of
#: them.
CUTBASED_HADRONIC_CATEGORIES = (
    "tH_had_4j1b",
    "tH_had_4j2b",
)

#: Legacy leptonic category names.  The current open-data ROOT inputs contain
#: no reconstructed forward jets, so leptonic top-associated categories are out
#: of scope: these names are kept for provenance only and are never assigned by
#: :func:`assign_top_category`.
LEGACY_LEPTONIC_CATEGORIES = (
    "ttH_lep_BDT1",
    "ttH_lep_BDT2",
    "tH_lep",
)

#: Full category priority order used by the analysis.  Highest priority first,
#: ``unassigned`` is the catch-all and always last.
CATEGORY_ORDER = (
    *HADRONIC_BDT_CATEGORIES,
    *CUTBASED_HADRONIC_CATEGORIES,
    "unassigned",
)


# --------------------------------------------------------------------------
# BDT input variables
# --------------------------------------------------------------------------

#: The five (and only five) classifier input variables.
#:
#: ``m_gammagamma`` is deliberately *not* a classifier input: it is retained for
#: bookkeeping, for the mass-window definitions and for the statistical model,
#: but feeding it to the BDT would sculpt the continuum background shape that
#: the workspace fit relies on.
BDT_FEATURES = (
    "n_jets_central",
    "n_bjets",
    "ht_jets",
    "met",
    "pt_gg",
)


# --------------------------------------------------------------------------
# Object definitions
# --------------------------------------------------------------------------

OBJECT_SELECTION: dict[str, Any] = {
    "photons": {
        "pt_min_gev": 25.0,
        "abs_eta_max": 2.37,
        "crack_veto": [1.37, 1.52],
        "lead_pt_over_mgg_min": 0.35,
        "sublead_pt_over_mgg_min": 0.25,
        "require_tight_id": False,
        "require_isolation": False,
        "comment": (
            "Photon tight ID and photon isolation are NOT required for this "
            "preselection sample; the tight-ID/tight-isolation flags are only "
            "used a posteriori to split the sample into the TI (tight-ID + "
            "tight-isolation) and NTI (fails either) diphoton categories."
        ),
    },
    "electrons_muons": {
        "pt_min_gev": 10.0,
        "require_id": False,
        "require_isolation": False,
        "comment": "No lepton ID or isolation requirement in this preselection.",
    },
    "jets": {
        "pt_min_gev": 25.0,
        "central_abs_eta_max": 2.5,
        "forward_abs_eta_min": 2.5,
        "btag": {
            "variable": "jet_btag_quantile",
            "operator": ">=",
            "value": 4,
            "comment": "Documented b-tag definition: jet_btag_quantile >= 4.",
        },
    },
}

MASS_WINDOWS: dict[str, Any] = {
    "fit_range_gev": [105.0, 160.0],
    "signal_window_gev": [123.0, 127.0],
    "sideband_low_gev": [105.0, 120.0],
    "sideband_high_gev": [130.0, 160.0],
    "blinded_observed_ti_gev": [120.0, 130.0],
}


# --------------------------------------------------------------------------
# Kinematics helpers
# --------------------------------------------------------------------------


def _obj_get(obj: Any, key: str, default: float | None = None) -> float:
    """Fetch ``key`` from a mapping-like or attribute-like physics object."""
    if isinstance(obj, Mapping):
        if key in obj:
            return float(obj[key])
    else:
        if hasattr(obj, key):
            return float(getattr(obj, key))
    if default is None:
        raise KeyError(f"object is missing required field {key!r}")
    return float(default)


def _four_vector(obj: Any) -> tuple[float, float, float, float]:
    """Return ``(E, px, py, pz)`` in GeV for one object."""
    pt = _obj_get(obj, "pt")
    eta = _obj_get(obj, "eta")
    phi = _obj_get(obj, "phi")
    px = pt * math.cos(phi)
    py = pt * math.sin(phi)
    pz = pt * math.sinh(eta)
    try:
        energy = _obj_get(obj, "e")
    except KeyError:
        mass = _obj_get(obj, "m", 0.0)
        energy = math.sqrt(px * px + py * py + pz * pz + mass * mass)
    return energy, px, py, pz


def invariant_mass(objects: Sequence[Any]) -> float:
    """Invariant mass in GeV of a collection of objects.

    Each object must expose ``pt``/``eta``/``phi`` plus either ``e`` or ``m``
    (mapping keys or attributes).  ``pt`` and ``e`` are assumed to be in GeV,
    matching the ATLAS open-data ``GamGam`` ntuples.
    """
    tot_e = tot_px = tot_py = tot_pz = 0.0
    for obj in objects:
        energy, px, py, pz = _four_vector(obj)
        tot_e += energy
        tot_px += px
        tot_py += py
        tot_pz += pz
    m2 = tot_e * tot_e - (tot_px * tot_px + tot_py * tot_py + tot_pz * tot_pz)
    return math.sqrt(m2) if m2 > 0.0 else 0.0


def _delta_phi(phi1: float, phi2: float) -> float:
    dphi = (phi1 - phi2 + math.pi) % (2.0 * math.pi) - math.pi
    return dphi


def photon_kinematic_acceptance(
    photon: Any,
    pt_min: float = OBJECT_SELECTION["photons"]["pt_min_gev"],
    abs_eta_max: float = OBJECT_SELECTION["photons"]["abs_eta_max"],
    crack_veto: Sequence[float] = tuple(OBJECT_SELECTION["photons"]["crack_veto"]),
) -> bool:
    """Photon kinematic acceptance: pT, |eta| and the calorimeter crack veto.

    No tight-ID and no isolation requirement is applied here, by design.
    """
    pt = _obj_get(photon, "pt")
    abs_eta = abs(_obj_get(photon, "eta"))
    if pt <= pt_min:
        return False
    if abs_eta >= abs_eta_max:
        return False
    if crack_veto[0] < abs_eta < crack_veto[1]:
        return False
    return True


def diphoton_features(photons: Sequence[Any]) -> dict[str, float]:
    """Diphoton bookkeeping observables from the two leading accepted photons."""
    if len(photons) < 2:
        raise ValueError("diphoton_features needs at least two photons")
    lead, sub = photons[0], photons[1]
    mgg = invariant_mass([lead, sub])
    _, px1, py1, _ = _four_vector(lead)
    _, px2, py2, _ = _four_vector(sub)
    pt_gg = math.hypot(px1 + px2, py1 + py2)
    deta = _obj_get(lead, "eta") - _obj_get(sub, "eta")
    dphi = _delta_phi(_obj_get(lead, "phi"), _obj_get(sub, "phi"))
    return {
        "m_gammagamma": mgg,
        "pt_gg": pt_gg,
        "delta_r_gg": math.hypot(deta, dphi),
        "lead_photon_pt": _obj_get(lead, "pt"),
        "sublead_photon_pt": _obj_get(sub, "pt"),
        "lead_photon_eta": _obj_get(lead, "eta"),
        "sublead_photon_eta": _obj_get(sub, "eta"),
        "lead_pt_over_mgg": _obj_get(lead, "pt") / mgg if mgg > 0 else float("nan"),
        "sublead_pt_over_mgg": _obj_get(sub, "pt") / mgg if mgg > 0 else float("nan"),
    }


# --------------------------------------------------------------------------
# Jet / lepton features
# --------------------------------------------------------------------------


def build_jet_features(
    jets: Iterable[Any],
    pt_min: float = OBJECT_SELECTION["jets"]["pt_min_gev"],
    central_eta_max: float = OBJECT_SELECTION["jets"]["central_abs_eta_max"],
    btag_quantile_min: int = OBJECT_SELECTION["jets"]["btag"]["value"],
) -> dict[str, float]:
    """Jet-derived event features.

    Parameters
    ----------
    jets
        Iterable of jet objects exposing ``pt``, ``eta`` and
        ``btag_quantile`` (mapping keys or attributes).  ``phi``/``e`` are
        optional and unused here.
    pt_min
        Jet pT threshold in GeV (jets must satisfy ``pt > pt_min``).
    central_eta_max
        Central jets satisfy ``|eta| <= central_eta_max``; forward jets satisfy
        ``|eta| > central_eta_max``.
    btag_quantile_min
        b-tagged jets satisfy ``jet_btag_quantile >= btag_quantile_min``.

    Notes
    -----
    The current ATLAS open-data ``GamGam`` ntuples contain no reconstructed
    jets with ``|eta| > 2.5``, so ``n_jets_forward`` is identically zero.  The
    field is produced anyway so that the contract is explicit rather than
    silently absent.
    """
    selected: list[tuple[float, float, int]] = []
    for jet in jets:
        pt = _obj_get(jet, "pt")
        if pt <= pt_min:
            continue
        eta = _obj_get(jet, "eta")
        btag = int(_obj_get(jet, "btag_quantile", -1))
        selected.append((pt, eta, btag))

    selected.sort(key=lambda item: item[0], reverse=True)
    pts = [item[0] for item in selected]
    central = [item for item in selected if abs(item[1]) <= central_eta_max]
    forward = [item for item in selected if abs(item[1]) > central_eta_max]
    btagged = [item for item in selected if item[2] >= btag_quantile_min]
    btagged_central = [item for item in central if item[2] >= btag_quantile_min]

    return {
        "n_jets": len(selected),
        "n_jets_central": len(central),
        "n_jets_forward": len(forward),
        "n_bjets": len(btagged),
        "n_bjets_central": len(btagged_central),
        "ht_jets": float(sum(pts)),
        "lead_jet_pt": float(pts[0]) if pts else 0.0,
        "sublead_jet_pt": float(pts[1]) if len(pts) > 1 else 0.0,
        "max_jet_btag_quantile": float(max((it[2] for it in selected), default=-1)),
    }


def build_lepton_features(
    leptons: Iterable[Any],
    pt_min: float = OBJECT_SELECTION["electrons_muons"]["pt_min_gev"],
) -> dict[str, float]:
    """Electron/muon multiplicity features (``pt > pt_min``, no ID, no isolation)."""
    n_el = n_mu = 0
    lead_pt = 0.0
    for lep in leptons:
        pt = _obj_get(lep, "pt")
        if pt <= pt_min:
            continue
        lead_pt = max(lead_pt, pt)
        flavour = int(_obj_get(lep, "type", 0))
        if flavour == 11:
            n_el += 1
        elif flavour == 13:
            n_mu += 1
    return {
        "n_electrons": n_el,
        "n_muons": n_mu,
        "n_leptons": n_el + n_mu,
        "lead_lepton_pt": lead_pt,
    }


# --------------------------------------------------------------------------
# Channel / category assignment
# --------------------------------------------------------------------------


def passes_hadronic_preselection(event: Mapping[str, Any]) -> bool:
    """Required analysis channel: 0 leptons, >= 3 jets, >= 1 b-jet."""
    return (
        int(event.get("n_leptons", 0)) == 0
        and int(event.get("n_jets", 0)) >= 3
        and int(event.get("n_bjets", 0)) >= 1
    )


def passes_leptonic_preselection(event: Mapping[str, Any]) -> bool:
    """Legacy leptonic bookkeeping channel: >= 1 lepton, >= 1 b-jet.

    Rows selected only by this definition are provenance-only: they are
    excluded from the hadronic BDT training, from the boundary optimisation,
    from the categorization metrics and from the statistical workspace.
    """
    return int(event.get("n_leptons", 0)) >= 1 and int(event.get("n_bjets", 0)) >= 1


def assign_top_category(
    event: Mapping[str, Any],
    score: float | None = None,
    thresholds: Sequence[float] | None = None,
) -> str:
    """Assign one top-associated category to ``event``.

    Parameters
    ----------
    event
        Mapping providing at least ``n_leptons``, ``n_jets``,
        ``n_jets_central`` and ``n_bjets``.  An optional ``allowed_categories``
        key (a container of category names) restricts the categories that may
        be assigned: categories dropped by the background-retention
        requirement are removed this way and their events fall through to the
        next priority (and ultimately to ``unassigned``).
    score
        BDT score in ``[0, 1]``.  ``None`` (or non-finite) disables the BDT
        categories, leaving only the cut-based ones.
    thresholds
        BDT boundaries.  Sorted descending internally: the highest boundary
        defines ``ttH_had_BDT1``, the next one ``ttH_had_BDT2`` and so on.

    Returns
    -------
    str
        One of :data:`CATEGORY_ORDER`.

    Notes
    -----
    Priority order is strictly the one in :data:`CATEGORY_ORDER`: the
    ``tH_had_4j*`` cut-based categories are evaluated *only* after the event has
    failed every hadronic BDT category, and they use the **central**-jet count
    (``n_jets_central``), not the inclusive jet multiplicity.
    """
    allowed = event.get("allowed_categories")

    def _ok(name: str) -> bool:
        return allowed is None or name in allowed

    if not passes_hadronic_preselection(event):
        # Leptonic bookkeeping rows (and anything else) are never categorized.
        return "unassigned"

    if score is not None and thresholds:
        value = float(score)
        if math.isfinite(value):
            ordered = sorted((float(t) for t in thresholds), reverse=True)
            for index, threshold in enumerate(ordered):
                if index >= len(HADRONIC_BDT_CATEGORIES):
                    break
                if value >= threshold:
                    name = HADRONIC_BDT_CATEGORIES[index]
                    if _ok(name):
                        return name
                    # Category was dropped by the retention requirement: the
                    # event falls through to the lower-priority categories.
                    break

    # Cut-based, lower-priority hadronic tH categories.
    if (
        int(event.get("n_leptons", 0)) == 0
        and int(event.get("n_jets_central", 0)) == 4
    ):
        n_b = int(event.get("n_bjets", 0))
        if n_b == 1 and _ok("tH_had_4j1b"):
            return "tH_had_4j1b"
        if n_b >= 2 and _ok("tH_had_4j2b"):
            return "tH_had_4j2b"

    return "unassigned"


# --------------------------------------------------------------------------
# Stable partitioning
# --------------------------------------------------------------------------

DEFAULT_PARTITION_FRACTIONS: dict[str, float] = {"train": 0.6, "val": 0.2, "test": 0.2}


def stable_partition(
    event_id: Any,
    seed: int = 20240917,
    fractions: Mapping[str, float] | Sequence[float] = DEFAULT_PARTITION_FRACTIONS,
) -> str:
    """Deterministically map a *stable event identifier* onto a partition.

    The partition depends only on ``(seed, event_id)`` -- never on row order,
    file order, or the number of events processed -- so re-running with a
    different input subset or a different row cap leaves every event in the
    same partition.

    A 64-bit BLAKE2b digest of ``"<seed>:<event_id>"`` is mapped to a uniform
    number in ``[0, 1)`` and bucketed by the cumulative fractions.
    """
    if isinstance(fractions, Mapping):
        names = list(fractions.keys())
        values = [float(fractions[k]) for k in names]
    else:
        names = ["train", "val", "test"]
        values = [float(v) for v in fractions]
        if len(values) != 3:
            raise ValueError("sequence `fractions` must have exactly three entries")

    total = sum(values)
    if total <= 0:
        raise ValueError("`fractions` must sum to a positive number")
    values = [v / total for v in values]

    digest = hashlib.blake2b(
        f"{int(seed)}:{event_id}".encode("utf-8"), digest_size=8
    ).digest()
    u = int.from_bytes(digest, "big") / float(1 << 64)

    cumulative = 0.0
    for name, value in zip(names, values):
        cumulative += value
        if u < cumulative:
            return name
    return names[-1]


def stable_partition_array(
    event_ids: Sequence[Any],
    seed: int = 20240917,
    fractions: Mapping[str, float] | Sequence[float] = DEFAULT_PARTITION_FRACTIONS,
) -> np.ndarray:
    """Vectorised convenience wrapper around :func:`stable_partition`."""
    return np.array(
        [stable_partition(eid, seed=seed, fractions=fractions) for eid in event_ids],
        dtype=object,
    )


# --------------------------------------------------------------------------
# Significance and boundary optimisation
# --------------------------------------------------------------------------


def counting_significance(s: float, b: float, min_b: float = 1e-9) -> float:
    """Asimov counting significance ``sqrt(2*((s+b)*ln(1+s/b) - s))``."""
    s = float(s)
    b = float(b)
    if b <= min_b or s <= 0.0:
        return 0.0
    value = 2.0 * ((s + b) * math.log1p(s / b) - s)
    return math.sqrt(value) if value > 0.0 else 0.0


def combined_significance(pairs: Iterable[tuple[float, float]]) -> float:
    """Quadrature sum of per-category counting significances."""
    return math.sqrt(sum(counting_significance(s, b) ** 2 for s, b in pairs))


DEFAULT_OPTIMIZER_CONFIG: dict[str, Any] = {
    "grid_min": 0.05,
    "grid_max": 0.98,
    "grid_step": 0.01,
    "max_boundaries": len(HADRONIC_BDT_CATEGORIES),
    "min_relative_improvement": 0.05,
    "min_background_yield": 0.8,
    "min_signal_yield": 1e-4,
}


def optimize_bdt_boundaries(
    rows: Any,
    config: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    """Greedy, iterative BDT category-boundary optimisation.

    ``rows`` is any iterable of mappings (or a ``pandas.DataFrame``) providing

    ``score``
        BDT score in ``[0, 1]``.
    ``is_signal``
        Truthy for the ``ttH+tH`` signal component.
    ``weight``
        Expected-yield weight (the 36 fb^-1 significance model weight; *not*
        the class-balanced classifier fit weight).

    At each iteration exactly one new boundary is added, chosen as the grid
    point that maximises the combined expected counting significance with the
    previously accepted boundaries held fixed.  The new boundary is accepted
    only if it improves the previous iteration's combined significance by at
    least ``min_relative_improvement`` (5 % by default); otherwise the search
    stops and the previous boundary set is returned.

    Candidate boundary sets that would create a BDT category with expected
    background below ``min_background_yield`` (0.8 events) are rejected, which
    keeps the optimiser consistent with the category-retention requirement.

    Returns a dictionary with the accepted ``thresholds``, the full
    ``iterations`` history (including the rejected stopping iteration) and the
    per-split relative improvements.
    """
    cfg = dict(DEFAULT_OPTIMIZER_CONFIG)
    if config:
        cfg.update({k: v for k, v in config.items() if v is not None})

    scores, is_signal, weights = _coerce_rows(rows)
    if scores.size == 0:
        return {
            "thresholds": [],
            "n_boundaries": 0,
            "best_significance": 0.0,
            "iterations": [],
            "accepted_splits": [],
            "config": cfg,
            "status": "empty-input",
        }

    grid = np.round(
        np.arange(
            float(cfg["grid_min"]),
            float(cfg["grid_max"]) + 0.5 * float(cfg["grid_step"]),
            float(cfg["grid_step"]),
        ),
        6,
    )
    grid = grid[(grid > 0.0) & (grid < 1.0)]

    min_b = float(cfg["min_background_yield"])
    min_s = float(cfg["min_signal_yield"])
    max_boundaries = int(cfg["max_boundaries"])
    min_rel = float(cfg["min_relative_improvement"])

    def evaluate(thresholds: Sequence[float]) -> tuple[float, list[dict[str, float]]] | None:
        ordered = sorted((float(t) for t in thresholds), reverse=True)
        upper = 1.0 + 1e-9
        per_cat: list[dict[str, float]] = []
        z2 = 0.0
        for index, low in enumerate(ordered):
            mask = (scores >= low) & (scores < upper)
            s = float(weights[mask & is_signal].sum())
            b = float(weights[mask & ~is_signal].sum())
            if b < min_b or s <= min_s:
                return None
            z = counting_significance(s, b)
            z2 += z * z
            per_cat.append(
                {
                    "category": HADRONIC_BDT_CATEGORIES[index]
                    if index < len(HADRONIC_BDT_CATEGORIES)
                    else f"ttH_had_BDT{index + 1}",
                    "score_low": low,
                    "score_high": 1.0,
                    "signal_yield": s,
                    "background_yield": b,
                    "counting_significance": z,
                }
            )
            upper = low
        return math.sqrt(z2), per_cat

    accepted: list[float] = []
    previous_z = 0.0
    iterations: list[dict[str, Any]] = []
    accepted_splits: list[dict[str, Any]] = []
    status = "max-boundaries-reached"

    for iteration in range(1, max_boundaries + 1):
        best: tuple[float, float, list[dict[str, float]]] | None = None
        n_candidates = 0
        for candidate in grid:
            if any(abs(candidate - t) < 1e-12 for t in accepted):
                continue
            result = evaluate([*accepted, float(candidate)])
            if result is None:
                continue
            n_candidates += 1
            z, per_cat = result
            if best is None or z > best[0] + 1e-12:
                best = (z, float(candidate), per_cat)

        if best is None:
            status = "no-viable-boundary"
            iterations.append(
                {
                    "iteration": iteration,
                    "accepted": False,
                    "reason": "no candidate boundary satisfies the "
                    f"min_background_yield={min_b} requirement",
                    "n_viable_candidates": 0,
                }
            )
            break

        z, candidate, per_cat = best
        relative_improvement = (
            float("inf") if previous_z <= 0.0 else (z - previous_z) / previous_z
        )
        accept = iteration == 1 or relative_improvement >= min_rel

        record = {
            "iteration": iteration,
            "n_boundaries": iteration,
            "candidate_boundary": candidate,
            "thresholds": sorted([*accepted, candidate], reverse=True),
            "combined_significance": z,
            "previous_combined_significance": previous_z,
            "relative_improvement": (
                None if not math.isfinite(relative_improvement) else relative_improvement
            ),
            "min_relative_improvement": min_rel,
            "n_viable_candidates": n_candidates,
            "accepted": bool(accept),
            "categories": per_cat,
        }
        iterations.append(record)

        if not accept:
            status = "relative-improvement-below-threshold"
            break

        accepted.append(candidate)
        previous_z = z
        accepted_splits.append(record)

    thresholds = sorted(accepted, reverse=True)
    final = evaluate(thresholds) if thresholds else None

    return {
        "thresholds": thresholds,
        "n_boundaries": len(thresholds),
        "best_significance": previous_z,
        "final_categories": final[1] if final else [],
        "iterations": iterations,
        "accepted_splits": accepted_splits,
        "config": cfg,
        "status": status,
    }


def _coerce_rows(rows: Any) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Normalise ``rows`` into ``(score, is_signal, weight)`` numpy arrays."""
    if hasattr(rows, "columns") and hasattr(rows, "__getitem__"):
        # pandas.DataFrame-like
        try:
            scores = np.asarray(rows["score"], dtype=float)
            is_signal = np.asarray(rows["is_signal"], dtype=bool)
            weights = np.asarray(rows["weight"], dtype=float)
            return scores, is_signal, weights
        except (KeyError, TypeError):
            pass

    score_list: list[float] = []
    signal_list: list[bool] = []
    weight_list: list[float] = []
    for row in rows:
        score_list.append(float(row["score"]))
        signal_list.append(bool(row["is_signal"]))
        weight_list.append(float(row["weight"]))
    return (
        np.asarray(score_list, dtype=float),
        np.asarray(signal_list, dtype=bool),
        np.asarray(weight_list, dtype=float),
    )
