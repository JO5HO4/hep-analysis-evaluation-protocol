"""Bounded, post-hoc artifact adapters for the traceability review pilot.

These adapters are evaluator code, not a task-solver output contract.  They
inspect only the supplied preserved run directory and create a canonical
reviewer-side table only when a readable artifact establishes its meaning.
"""
from __future__ import annotations

import json
import hashlib
import importlib.util
import itertools
import math
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import pandas as pd


KEY_ALIASES = {
    "event_id": {"event_id", "event", "eventid", "evt_id"},
    "i": {"i", "jet_i", "jet1", "j1", "idx1"},
    "j": {"j", "jet_j", "jet2", "j2", "idx2"},
    "k": {"k", "jet_k", "jet3", "j3", "idx3"},
}
SELECTED_ALIASES = {"selected", "is_selected", "keep", "accepted", "chosen", "final_selection"}
MASS_ALIASES = {"triplet_mass", "m123", "m_jjj", "mass_jjj"}
SCORE_ALIASES = {"score_xgb", "score", "bdt_score", "classifier_score", "prediction", "probability"}


@dataclass(frozen=True)
class AdaptedArtifact:
    status: str  # computed, not_established_after_inventory, invalid
    role: str
    source: Path | None
    canonical: Path | None
    detail: str


def _read_table(path: Path) -> pd.DataFrame | None:
    try:
        if path.suffix.lower() == ".parquet":
            return pd.read_parquet(path)
        if path.suffix.lower() == ".csv":
            return pd.read_csv(path)
        if path.suffix.lower() == ".json":
            payload: Any = json.loads(path.read_text())
            if isinstance(payload, list):
                return pd.DataFrame(payload)
            if isinstance(payload, dict):
                for value in payload.values():
                    if isinstance(value, list) and all(isinstance(item, dict) for item in value):
                        return pd.DataFrame(value)
    except (OSError, ValueError, TypeError, UnicodeDecodeError):
        return None
    return None


def _canonical_keys(frame: pd.DataFrame) -> pd.DataFrame | None:
    lower = {str(column).lower(): column for column in frame.columns}
    rename: dict[object, str] = {}
    for target, aliases in KEY_ALIASES.items():
        source = next((lower[name] for name in aliases if name in lower), None)
        if source is None:
            return None
        rename[source] = target
    keys = frame.rename(columns=rename)[["event_id", "i", "j", "k"]].copy()
    if keys.isna().any().any():
        return None
    for column in ("i", "j", "k"):
        keys[column] = pd.to_numeric(keys[column], errors="coerce")
    if keys[["i", "j", "k"]].isna().any().any():
        return None
    # Canonicalize unordered triplets without changing the event identifier.
    ordered = keys[["i", "j", "k"]].astype(int).apply(lambda row: sorted(row), axis=1, result_type="expand")
    keys[["i", "j", "k"]] = ordered
    return keys


def adapt_selected_candidates(run: Path, destination: Path) -> AdaptedArtifact:
    """Discover a selection table in arbitrary common artifact formats.

    Files are tried in deterministic order, prioritizing names that explicitly
    say selected. A boolean selection flag is honored when present. A table
    without a flag is accepted only when its filename itself states selection.
    """
    candidates = sorted(
        (item for item in run.rglob("*") if item.is_file() and item.suffix.lower() in {".parquet", ".csv", ".json"}),
        key=lambda item: (0 if "selected" in item.name.lower() else 1, item.as_posix()),
    )
    attempted: list[str] = []
    for source in candidates:
        frame = _read_table(source)
        keys = _canonical_keys(frame) if frame is not None else None
        if keys is None:
            continue
        lower = {str(column).lower(): column for column in frame.columns}
        flag = next((lower[name] for name in SELECTED_ALIASES if name in lower), None)
        name_declares_selection = any(word in source.name.lower() for word in ("selected", "selection", "chosen"))
        if flag is not None:
            values = frame[flag]
            if values.dtype == bool:
                keys = keys[values.to_numpy()]
            else:
                numeric = pd.to_numeric(values, errors="coerce")
                if numeric.notna().all():
                    keys = keys[numeric.to_numpy().astype(bool)]
                else:
                    attempted.append(f"{source.name}: non-boolean selection flag")
                    continue
        elif not name_declares_selection:
            continue
        if keys.empty:
            attempted.append(f"{source.name}: selection is empty")
            continue
        destination.parent.mkdir(parents=True, exist_ok=True)
        keys.to_parquet(destination, index=False)
        return AdaptedArtifact("computed", "selected_candidates", source, destination, "canonicalized evaluator-side candidate keys")
    detail = "no readable selection table with candidate keys was found"
    if attempted:
        detail += "; " + "; ".join(attempted[:3])
    return AdaptedArtifact("not_established_after_inventory", "selected_candidates", None, None, detail)


def adapt_labeled_candidates(run: Path, destination: Path) -> AdaptedArtifact:
    """Find any preserved candidate table that carries mass and truth labels."""
    def candidate_rank(item: Path) -> tuple[int, str]:
        lower = item.as_posix().lower()
        # Prefer explicitly held-out/evaluation data over train/raw tables;
        # this is a discovery priority, not a filename requirement.
        return (0 if any(word in lower for word in ("test", "eval", "heldout", "held-out")) else 1, lower)
    for source in sorted((item for item in run.rglob("*") if item.is_file() and item.suffix.lower() in {".parquet", ".csv", ".json"}), key=candidate_rank):
        # A selected-only table is never the pre-selection candidate universe.
        # Using it here would fabricate a baseline comparison with no negatives.
        if any(word in source.name.lower() for word in ("selected", "selection", "chosen")):
            continue
        frame = _read_table(source)
        if frame is None or _canonical_keys(frame) is None:
            continue
        lower = {str(column).lower(): column for column in frame.columns}
        mass_column = next((lower[name] for name in MASS_ALIASES if name in lower), None)
        if mass_column is not None and "is_truth" in lower:
            keys = _canonical_keys(frame)
            assert keys is not None
            canonical = keys.copy()
            canonical["triplet_mass"] = pd.to_numeric(frame[mass_column], errors="coerce")
            canonical["is_truth"] = frame[lower["is_truth"]]
            if canonical[["triplet_mass", "is_truth"]].isna().any().any():
                continue
            destination.parent.mkdir(parents=True, exist_ok=True)
            canonical.to_parquet(destination, index=False)
            return AdaptedArtifact("computed", "labeled_candidates", source, destination, "canonicalized evaluator-side labeled candidates")
    return AdaptedArtifact("not_established_after_inventory", "labeled_candidates", None, None, "no readable candidate table with triplet_mass and is_truth was found")


def _inference_event_ids(run: Path) -> tuple[set[int] | None, Path | None]:
    def inference_rank(item: Path) -> tuple[int, str]:
        lower = item.as_posix().lower()
        if "inference_test" in lower:
            return (0, lower)
        if "infer" in lower and not any(word in lower for word in ("tuning", "validation", "_val")):
            return (1, lower)
        return (2, lower)
    tables = sorted(
        (item for item in run.rglob("*") if item.is_file() and item.suffix.lower() in {".parquet", ".csv", ".json"}),
        key=inference_rank,
    )
    for source in tables:
        frame = _read_table(source)
        if frame is None:
            continue
        lower = {str(column).lower(): column for column in frame.columns}
        event_column = next((lower[name] for name in KEY_ALIASES["event_id"] if name in lower), None)
        lower_path = source.as_posix().lower()
        if event_column is not None and "infer" in lower_path and not any(word in lower_path for word in ("tuning", "validation", "_val")):
            values = pd.to_numeric(frame[event_column], errors="coerce").dropna().astype(int)
            if not values.empty:
                return set(values.tolist()), source
    return None, None


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def reconstruct_labeled_candidates(run: Path, raw_root: Path, destination: Path) -> AdaptedArtifact:
    """Rebuild the labeled candidate universe from evaluator-owned raw ROOT input.

    The inferred event set is discovered from the preserved run, but candidate
    masses and truth labels are derived only from the fixed raw input. Jets are
    treated as massless, exactly as the task's public data provenance states.
    """
    event_ids, event_source = _inference_event_ids(run)
    if not event_ids or event_source is None:
        return AdaptedArtifact("not_established_after_inventory", "labeled_candidates", None, None, "no readable inference artifact established the evaluated event set")
    if not raw_root.is_file():
        return AdaptedArtifact("not_established_after_inventory", "labeled_candidates", None, None, "evaluator-owned raw ROOT input is unavailable")
    try:
        import uproot
        with uproot.open(raw_root) as source:
            tree = source["output"]
            branches = ["Number", "genjet_pt", "genjet_eta", "genjet_phi", "truth_triplet_0", "truth_triplet_1", "truth_triplet_2", "truth_triplet_3"]
            arrays = tree.arrays(branches, library="ak")
    except Exception as exc:  # evaluator input errors remain evidence, not guesses
        return AdaptedArtifact("invalid", "labeled_candidates", raw_root, None, f"cannot read evaluator raw ROOT input: {type(exc).__name__}")
    rows: list[dict[str, Any]] = []
    for entry, number in enumerate(arrays["Number"].to_list()):
        event_id = int(number)
        if event_id not in event_ids:
            continue
        pt = arrays["genjet_pt"][entry].to_list()
        eta = arrays["genjet_eta"][entry].to_list()
        phi = arrays["genjet_phi"][entry].to_list()
        truth: set[tuple[int, int, int]] = set()
        for branch in ("truth_triplet_0", "truth_triplet_1", "truth_triplet_2", "truth_triplet_3"):
            triplet = [int(value) for value in arrays[branch][entry].to_list()]
            if len(triplet) == 3 and all(0 <= value < len(pt) for value in triplet) and len(set(triplet)) == 3:
                truth.add(tuple(sorted(triplet)))
        for triplet in itertools.combinations(range(len(pt)), 3):
            def pair_mass(a: int, b: int) -> float:
                pair_px = float(pt[a]) * math.cos(float(phi[a])) + float(pt[b]) * math.cos(float(phi[b]))
                pair_py = float(pt[a]) * math.sin(float(phi[a])) + float(pt[b]) * math.sin(float(phi[b]))
                pair_pz = float(pt[a]) * math.sinh(float(eta[a])) + float(pt[b]) * math.sinh(float(eta[b]))
                pair_e = float(pt[a]) * math.cosh(float(eta[a])) + float(pt[b]) * math.cosh(float(eta[b]))
                return math.sqrt(max(0.0, pair_e * pair_e - pair_px * pair_px - pair_py * pair_py - pair_pz * pair_pz))
            def delta_r(a: int, b: int) -> float:
                delta_phi = (float(phi[a]) - float(phi[b]) + math.pi) % (2 * math.pi) - math.pi
                return math.hypot(float(eta[a]) - float(eta[b]), delta_phi)
            px = sum(float(pt[index]) * math.cos(float(phi[index])) for index in triplet)
            py = sum(float(pt[index]) * math.sin(float(phi[index])) for index in triplet)
            pz = sum(float(pt[index]) * math.sinh(float(eta[index])) for index in triplet)
            energy = sum(float(pt[index]) * math.cosh(float(eta[index])) for index in triplet)
            mass_squared = max(0.0, energy * energy - px * px - py * py - pz * pz)
            mass = math.sqrt(mass_squared)
            a, b, c = triplet
            rows.append({"event_id": event_id, "i": a, "j": b, "k": c, "triplet_mass": mass, "is_truth": triplet in truth,
                         "dr_ab": delta_r(a, b), "dr_ac": delta_r(a, c), "dr_bc": delta_r(b, c),
                         "mij_over_m123_ab": pair_mass(a, b) / mass if mass else 0.0,
                         "mij_over_m123_ac": pair_mass(a, c) / mass if mass else 0.0,
                         "mij_over_m123_bc": pair_mass(b, c) / mass if mass else 0.0})
    if not rows:
        return AdaptedArtifact("invalid", "labeled_candidates", raw_root, None, "raw evaluator input had no candidates for the discovered inference events")
    destination.parent.mkdir(parents=True, exist_ok=True)
    pd.DataFrame(rows).to_parquet(destination, index=False)
    return AdaptedArtifact(
        "computed", "labeled_candidates", raw_root, destination,
        f"reconstructed {len(rows)} massless triplet candidates for {len(event_ids)} inference events from {event_source.name}; raw_sha256={_sha256(raw_root)}",
    )


def build_score_diagnostics(run: Path, candidates_path: Path, destination: Path) -> AdaptedArtifact:
    """Compute reviewer-owned score and mass diagnostics from discovered scores."""
    if not candidates_path.is_file():
        return AdaptedArtifact("not_established_after_inventory", "score_diagnostics", None, None, "canonical evaluator candidate table is unavailable")
    tables = sorted(
        (item for item in run.rglob("*") if item.is_file() and item.suffix.lower() in {".parquet", ".csv", ".json"}),
        key=lambda item: (0 if "inference_test" in item.as_posix().lower() else 1, item.as_posix()),
    )
    for source in tables:
        if "infer" not in source.as_posix().lower():
            continue
        frame = _read_table(source)
        keys = _canonical_keys(frame) if frame is not None else None
        if keys is None:
            continue
        lower = {str(column).lower(): column for column in frame.columns}
        score_column = next((lower[name] for name in SCORE_ALIASES if name in lower), None)
        if score_column is None:
            continue
        scores = keys.copy()
        scores["score"] = pd.to_numeric(frame[score_column], errors="coerce")
        candidates = pd.read_parquet(candidates_path)
        joined = scores.merge(candidates, on=["event_id", "i", "j", "k"], how="inner", validate="one_to_one")
        finite = joined.dropna(subset=["score", "triplet_mass"])
        if len(finite) < 2:
            continue
        correlation = float(finite["score"].corr(finite["triplet_mass"], method="pearson"))
        if not math.isfinite(correlation):
            continue
        truth = finite["is_truth"].astype(bool)
        treatment = None
        treatment_source = None
        def walk(value: Any) -> list[tuple[str, Any]]:
            found: list[tuple[str, Any]] = []
            if isinstance(value, dict):
                for key, item in value.items():
                    found.append((str(key).lower(), item)); found.extend(walk(item))
            elif isinstance(value, list):
                for item in value: found.extend(walk(item))
            return found
        for report in sorted(run.rglob("training*.json")):
            try: fields = walk(json.loads(report.read_text()))
            except (OSError, ValueError): continue
            match = next(((key, value) for key, value in fields if any(token in key for token in ("scale_pos_weight", "class_weight", "resampl", "ranking_objective"))), None)
            if match and match[1] is not None:
                treatment = {"field": match[0], "value": match[1]}; treatment_source = report; break
        result = {
            "schema_version": "top-reconstruction-evaluator-diagnostics/v1",
            "owner": "reviewer",
            "source_inference": source.as_posix(),
            "source_candidates": candidates_path.as_posix(),
            "score_column": str(score_column),
            "partition": "discovered final inference artifact",
            "score_mass_correlation": {"method": "pearson", "value": correlation, "candidate_count": int(len(finite))},
            "score_distribution": {"quantity": str(score_column), "unit": "unitless classifier score", "normalization": "candidate count", "finite_count": int(len(finite)), "truth_count": int(truth.sum()), "fake_count": int((~truth).sum()), "minimum": float(finite["score"].min()), "maximum": float(finite["score"].max())},
            "mass_distribution": {"quantity": "triplet_mass", "unit": "GeV", "normalization": "candidate count", "finite_count": int(len(finite)), "minimum": float(finite["triplet_mass"].min()), "maximum": float(finite["triplet_mass"].max())},
            "class_imbalance": {"truth_candidates": int(truth.sum()), "fake_candidates": int((~truth).sum()), "truth_to_fake_ratio": float(truth.sum() / (~truth).sum()) if (~truth).sum() else None, "declared_treatment": treatment, "treatment_source": treatment_source.as_posix() if treatment_source else None},
        }
        # Q31: both models are evaluated only on the fixed modulo-10 test
        # partition and only if recovered scores cover every candidate there.
        try:
            baseline_path = Path(__file__).resolve().parents[3] / "evaluation/top-reconstruction-baseline/classifier_baseline.py"
            spec = importlib.util.spec_from_file_location("frozen_top_classifier", baseline_path)
            if spec is None or spec.loader is None: raise RuntimeError("cannot load frozen classifier")
            classifier = importlib.util.module_from_spec(spec); spec.loader.exec_module(classifier)
            if len(joined) != len(candidates): raise ValueError("inference scores do not cover every evaluator candidate")
            baseline = classifier.evaluate(candidates)
            test = finite[finite["event_id"].astype(int) % 10 >= 8]
            agent_auc = classifier.auc(test["is_truth"].astype(bool).to_numpy(), test["score"].to_numpy(float))
            result["frozen_classifier_comparison"] = {"baseline": baseline["baseline"]["name"], "partition": baseline["baseline"]["partition"], "agent_auc": agent_auc, "baseline_auc": baseline["test"]["roc_auc"], "agent_at_least_baseline": bool(agent_auc >= baseline["test"]["roc_auc"])}
        except Exception as exc:
            result["frozen_classifier_comparison"] = {"unavailable": f"{type(exc).__name__}: {exc}"}
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
        return AdaptedArtifact("computed", "score_diagnostics", source, destination, "reviewer-generated score/mass diagnostics from recovered inference scores")
    return AdaptedArtifact("not_established_after_inventory", "score_diagnostics", None, None, "no readable inference table with canonical candidate keys and a continuous score was found")
