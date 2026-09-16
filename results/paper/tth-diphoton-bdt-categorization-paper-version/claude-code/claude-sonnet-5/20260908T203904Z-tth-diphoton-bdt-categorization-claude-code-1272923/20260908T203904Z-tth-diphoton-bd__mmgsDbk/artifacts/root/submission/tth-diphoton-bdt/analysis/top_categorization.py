"""Required callable API for the tth-diphoton-bdt hadronic categorization.

This module intentionally has no third-party dependencies beyond the
Python standard library so it can be imported and unit-exercised in
isolation from the rest of the pipeline (ROOT / pandas / sklearn).
"""
import hashlib
import math

# ---------------------------------------------------------------------------
# Category priority order.
#
# The hadronic BDT categories are evaluated first, in order of decreasing
# expected S/sqrt(B) (BDT1 is the tightest / purest bin). The cut-based
# tH categories are lower priority and are only evaluated for events that
# fail every hadronic BDT category. "unassigned" is the catch-all.
#
# Legacy leptonic bookkeeping rows are never assigned one of these hadronic
# categories -- they are labelled "leptonic_bookkeeping" (not part of the
# required categorization, kept only so the name is available to callers
# that want to recognize/skip bookkeeping rows).
# ---------------------------------------------------------------------------
CATEGORY_ORDER = [
    "ttH_had_BDT1",
    "ttH_had_BDT2",
    "ttH_had_BDT3",
    "ttH_had_BDT4",
    "tH_had_4j1b",
    "tH_had_4j2b",
    "unassigned",
]

# Legacy / bookkeeping-only label, not part of the required categorization.
LEPTONIC_BOOKKEEPING_CATEGORY = "leptonic_bookkeeping"

#: Exactly five variables used to train/score the hadronic BDT.
#: m_gammagamma is deliberately excluded (bookkeeping only).
BDT_FEATURES = [
    "n_jets_central",
    "n_bjets",
    "jet_ht",
    "leading_jet_pt",
    "dijet_mass_leading",
]

CENTRAL_JET_ETA_MAX = 2.5
BTAG_QUANTILE_MIN = 4


def _get(obj, key, default=None):
    if isinstance(obj, dict):
        return obj.get(key, default)
    return getattr(obj, key, default)


def invariant_mass(objects):
    """Invariant mass of a list of four-momenta.

    Each element of ``objects`` may be a dict or object exposing ``pt``,
    ``eta``, ``phi`` and ``e`` (energy). Returns ``float('nan')`` for fewer
    than two inputs or non-finite inputs, never raises on bad kinematics.
    """
    objs = list(objects)
    if len(objs) < 2:
        return float("nan")

    px = py = pz = e = 0.0
    for o in objs:
        pt = _get(o, "pt")
        eta = _get(o, "eta")
        phi = _get(o, "phi")
        energy = _get(o, "e")
        if pt is None or eta is None or phi is None or energy is None:
            return float("nan")
        if not all(math.isfinite(v) for v in (pt, eta, phi, energy)):
            return float("nan")
        px += pt * math.cos(phi)
        py += pt * math.sin(phi)
        pz += pt * math.sinh(eta)
        e += energy

    m2 = e * e - (px * px + py * py + pz * pz)
    if not math.isfinite(m2):
        return float("nan")
    return math.sqrt(m2) if m2 > 0 else 0.0


def build_jet_features(jets, central_eta_max=CENTRAL_JET_ETA_MAX,
                        btag_quantile_min=BTAG_QUANTILE_MIN):
    """Build the five BDT_FEATURES plus bookkeeping counts from a jet collection.

    ``jets`` is an iterable of dict/objects exposing ``pt``, ``eta``, ``phi``,
    ``e`` and ``btag_quantile``. Jets are not required to be pre-sorted.
    Returns a dict containing BDT_FEATURES plus ``n_jets_total``,
    ``n_jets_forward`` and ``n_bjets_central`` for bookkeeping.
    """
    jets = list(jets)
    central = [j for j in jets if abs(_get(j, "eta", float("nan"))) <= central_eta_max]
    forward = [j for j in jets if abs(_get(j, "eta", float("nan"))) > central_eta_max]

    n_bjets_central = sum(
        1 for j in central if _get(j, "btag_quantile", -1) >= btag_quantile_min
    )
    n_bjets_total = sum(
        1 for j in jets if _get(j, "btag_quantile", -1) >= btag_quantile_min
    )

    central_sorted = sorted(central, key=lambda j: _get(j, "pt", 0.0), reverse=True)
    jet_ht = sum(_get(j, "pt", 0.0) for j in central_sorted)
    leading_jet_pt = _get(central_sorted[0], "pt", float("nan")) if central_sorted else float("nan")
    dijet_mass_leading = (
        invariant_mass(central_sorted[:2]) if len(central_sorted) >= 2 else float("nan")
    )

    return {
        "n_jets_central": len(central),
        "n_jets_forward": len(forward),
        "n_jets_total": len(jets),
        "n_bjets": n_bjets_total,
        "n_bjets_central": n_bjets_central,
        "jet_ht": jet_ht,
        "leading_jet_pt": leading_jet_pt,
        "dijet_mass_leading": dijet_mass_leading,
    }


def _default_thresholds():
    # Descending score cuts for BDT1..BDT4; overwritten by
    # optimize_bdt_boundaries in the real pipeline run.
    return [0.85, 0.70, 0.55, 0.40]


def assign_top_category(event, score=None, thresholds=None):
    """Assign one of CATEGORY_ORDER to a single hadronic-or-leptonic event.

    ``event`` must expose (dict or attrs): ``channel`` ("hadronic" or
    "leptonic"), ``n_leptons``, ``n_jets_central``, ``n_bjets``.
    ``score`` overrides ``event['bdt_score']`` when provided.
    ``thresholds`` is a list of 4 descending BDT-score boundaries
    [t1 > t2 > t3 > t4] defining ttH_had_BDT1..BDT4; defaults to a fixed
    fallback used only when no optimized boundaries are supplied.
    """
    channel = _get(event, "channel")
    if channel != "hadronic":
        return LEPTONIC_BOOKKEEPING_CATEGORY

    n_leptons = _get(event, "n_leptons", 0)
    n_jets_central = _get(event, "n_jets_central", 0)
    n_bjets = _get(event, "n_bjets", 0)

    if score is None:
        score = _get(event, "bdt_score")

    thr = list(thresholds) if thresholds else _default_thresholds()
    thr = sorted(thr, reverse=True)
    bdt_labels = [c for c in CATEGORY_ORDER if c.startswith("ttH_had_BDT")]

    if score is not None and isinstance(score, (int, float)) and math.isfinite(score):
        for label, cut in zip(bdt_labels, thr):
            if score >= cut:
                return label

    # Failed all hadronic BDT categories (or no finite score) -> cut-based
    # tH categories, using central-jet count only (not total multiplicity).
    if n_leptons == 0 and n_jets_central == 4:
        if n_bjets == 1:
            return "tH_had_4j1b"
        if n_bjets >= 2:
            return "tH_had_4j2b"

    return "unassigned"


def stable_partition(event_id, seed=2024, fractions=(0.6, 0.2, 0.2)):
    """Deterministically map an event identifier to train/val/test.

    Uses a stable hash of (seed, event_id) so the partition does not depend
    on row order, table sort order, or process. Returns one of
    "train", "val", "test".
    """
    total = sum(fractions)
    if total <= 0:
        raise ValueError("fractions must sum to a positive number")
    f_train, f_val, f_test = (f / total for f in fractions)

    key = f"{seed}:{event_id}".encode("utf-8")
    digest = hashlib.sha256(key).hexdigest()
    # 52 bits of entropy is ample for a uniform [0, 1) draw.
    u = int(digest[:13], 16) / float(16 ** 13)

    if u < f_train:
        return "train"
    if u < f_train + f_val:
        return "val"
    return "test"


def _significance(s, b):
    if b <= 0:
        return 0.0
    return math.sqrt(2.0 * ((s + b) * math.log(1.0 + s / b) - s))


def optimize_bdt_boundaries(rows, config=None):
    """Greedily add BDT-score category boundaries.

    ``rows`` is an iterable of dicts with ``bdt_score`` (float in [0, 1]),
    ``signal_weight`` and ``background_weight`` (36fb-normalized model
    yields used for the significance estimate; NOT the classifier fit
    weights). A boundary is only accepted while it improves the combined
    expected significance (quadrature sum over the resulting bins) by at
    least ``min_relative_improvement`` (default 5%) relative to the
    previous accepted iteration. Boundaries are searched on a fixed grid.

    Returns a dict with ``boundaries`` (sorted descending list of accepted
    score cuts), ``n_categories`` (= len(boundaries) + 1), and
    ``iterations`` (list of dicts recording every accepted step: the
    boundary added, the significance before/after and the relative
    improvement), plus ``rejected`` describing the first boundary that
    failed the improvement threshold (if the search stopped early).
    """
    cfg = dict(config or {})
    min_rel_improvement = cfg.get("min_relative_improvement", 0.05)
    max_boundaries = cfg.get("max_boundaries", 4)
    grid = cfg.get("grid", [round(x * 0.01, 2) for x in range(5, 100, 1)])

    rows = [
        r for r in rows
        if r.get("bdt_score") is not None and math.isfinite(r.get("bdt_score", float("nan")))
    ]

    def combined_significance(boundaries):
        edges = sorted(set([0.0] + list(boundaries) + [1.0]))
        z_tot2 = 0.0
        bins = []
        for lo, hi in zip(edges[:-1], edges[1:]):
            s = sum(r["signal_weight"] for r in rows if lo <= r["bdt_score"] < hi or (hi == 1.0 and r["bdt_score"] == 1.0))
            b = sum(r["background_weight"] for r in rows if lo <= r["bdt_score"] < hi or (hi == 1.0 and r["bdt_score"] == 1.0))
            z = _significance(s, b)
            z_tot2 += z * z
            bins.append({"lo": lo, "hi": hi, "s": s, "b": b, "z": z})
        return math.sqrt(z_tot2), bins

    accepted = []
    iterations = []
    prev_z, _ = combined_significance(accepted)
    rejected = None

    while len(accepted) < max_boundaries:
        best_cut = None
        best_z = prev_z
        for cut in grid:
            if any(abs(cut - a) < 1e-9 for a in accepted):
                continue
            candidate = accepted + [cut]
            z, _ = combined_significance(candidate)
            if z > best_z:
                best_z = z
                best_cut = cut

        if best_cut is None:
            rejected = {"reason": "no_candidate_improves_significance"}
            break

        rel_improvement = (best_z - prev_z) / prev_z if prev_z > 0 else float("inf")
        if rel_improvement < min_rel_improvement:
            rejected = {
                "candidate_boundary": best_cut,
                "significance_before": prev_z,
                "significance_after": best_z,
                "relative_improvement": rel_improvement,
                "reason": "below_min_relative_improvement",
            }
            break

        accepted.append(best_cut)
        accepted.sort(reverse=True)
        iterations.append({
            "step": len(accepted),
            "boundary": best_cut,
            "significance_before": prev_z,
            "significance_after": best_z,
            "relative_improvement": rel_improvement,
        })
        prev_z = best_z

    final_z, final_bins = combined_significance(accepted)
    return {
        "boundaries": sorted(accepted, reverse=True),
        "n_categories": len(accepted) + 1,
        "iterations": iterations,
        "rejected": rejected,
        "final_significance": final_z,
        "final_bins": final_bins,
        "min_relative_improvement": min_rel_improvement,
    }
