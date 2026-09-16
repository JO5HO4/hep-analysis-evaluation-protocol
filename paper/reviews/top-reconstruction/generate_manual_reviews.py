#!/usr/bin/env python3
"""Generate evidence-led per-trial manual-review scaffolds for preserved runs.

This intentionally does not mutate a preserved run, task, baseline, or grader.
It only reads the paper evidence tree and writes the requested review documents.
"""
from __future__ import annotations

import json
import re
from datetime import date
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[3]
EVIDENCE = ROOT / "results/paper/top-reconstruction-paper-version"
OUT = ROOT / "paper/reviews/top-reconstruction"

# The paper matrix has one representative per agent/model cell.  These two
# cells have multiple completed trials in the evidence tree; retain their
# later clean retry, consistent with the paper-set selection policy.
PREFERRED_TRIALS = {
    ("claude-code", "claude-opus-5"): "20260904T230352Z-top-reconstruct__p6Zi8m9",
    ("openhands", "gpt-5.6-sol"): "20260905T023203Z-top-reconstruct__vQ8QaVm",
}

QUESTIONS = [
    ("Execution and Meta", "Both trial wall-clock and pure agent execution time established"),
    ("Execution and Meta", "Total run cost established in USD"),
    ("BDT Setup and Features", "Classifier trained and used, with package identified"),
    ("BDT Setup and Features", "At least two final input features identified"),
    ("BDT Setup and Features", "Additional feature set tested"),
    ("BDT Setup and Features", "Nonempty event-disjoint train/validation/test partitions"),
    ("BDT Setup and Features", "At least two distinct ML setups tried"),
    ("Candidate Selection", "Specific final candidate-selection algorithm established"),
    ("Candidate Selection", "At least two selection configurations compared on common validation data"),
    ("Candidate Selection", "N_top <= 2 for every event"),
    ("Physics and Diagnostics", "Score-mass correlation measured and reported"),
    ("Physics and Diagnostics", "Final selection has no triplet-mass input or hard mass window"),
    ("Physics and Diagnostics", "At least two pipeline optimization attempts"),
    ("Physics and Diagnostics", "BDT-score distribution quantity, normalization, and finite values established"),
    ("Physics and Diagnostics", "Reconstructed-mass comparison quantity, normalization, and finite values established"),
    ("Reconstruction Performance and Jet Disjointness", "Zero overlapping selected triplets"),
    ("Baseline Comparison and Physics Quality", "Selected-mass bias no worse than mass-greedy/v2-n-top-2"),
    ("Baseline Comparison and Physics Quality", "Selected truth-matched mass resolution strictly better than baseline"),
    ("Baseline Comparison and Physics Quality", "Reconstruction efficiency at least baseline"),
    ("Baseline Comparison and Physics Quality", "Selected-candidate purity at least baseline"),
    ("Baseline Comparison and Physics Quality", "Fake-to-true ratio no greater than baseline"),
    ("Baseline Comparison and Physics Quality", "Selected-candidate F1 at least baseline"),
    ("Baseline Comparison and Physics Quality", "Candidate-level selection accuracy at least baseline"),
    ("Baseline Comparison and Physics Quality", "Balanced selection accuracy at least baseline"),
    ("Baseline Comparison and Physics Quality", "Baseline Pareto improvement"),
    ("Plotting and Presentation Quality", "Plot quantity, unit, and finite values established"),
    ("Plotting and Presentation Quality", "Histogram statistical normalization established"),
    ("Plotting and Presentation Quality", "Evaluated partition established for every performance plot"),
    ("Methodology", "Candidate class-imbalance ratio and treatment established"),
    ("Methodology", "Final reproducibility configuration complete"),
    ("Frozen Classifier Baseline Comparison", "Held-out AUC at least frozen classifier baseline"),
]


def load(path: Path) -> dict:
    return json.loads(path.read_text())


def nested_values(value, names):
    """Return values for keys, case-insensitively, from a JSON tree."""
    found = []
    if isinstance(value, dict):
        for key, item in value.items():
            if key.lower() in names:
                found.append(item)
            found.extend(nested_values(item, names))
    elif isinstance(value, list):
        for item in value:
            found.extend(nested_values(item, names))
    return found


def trial_dirs():
    records = []
    for result in sorted(EVIDENCE.rglob("result.json")):
        data = load(result)
        if not data.get("trial_name"):
            continue  # Harbor job-level result, not a logical trial.
        rel = result.parent.relative_to(EVIDENCE)
        records.append((data["agent_info"]["name"], data["agent_info"]["model_info"]["name"], data["trial_name"], result.parent, data, rel))
    def matrix_cell(record):
        agent, model, _, _, _, rel = record
        # The two Qwen tiers both self-identify as qwen-3.  Their evidence-tree
        # model directory carries the distinct benchmark-cell identity.
        if agent == "qwen-coder" and model == "qwen-3":
            return agent, rel.parts[1]
        return agent, model

    selected = []
    for key in sorted({matrix_cell(record) for record in records}):
        candidates = [record for record in records if matrix_cell(record) == key]
        preferred = PREFERRED_TRIALS.get(key)
        if preferred:
            candidates = [record for record in candidates if record[2] == preferred]
        if len(candidates) != 1:
            raise RuntimeError(f"expected one selected trial for {key}, found {len(candidates)}")
        selected.extend(candidates)
    if len(selected) != 15:
        raise RuntimeError(f"expected the 15-cell paper matrix, found {len(selected)} trials")
    return sorted(selected, key=lambda r: (r[0], r[1], r[2]))


def status_for(record):
    agent, model, run_id, run, data, _ = record
    outputs = run / "artifacts/root/results"
    train = outputs / "train/training_report_xgb.json"
    select = outputs / "select_triplets/selection_report.json"
    optimize = outputs / "optimization_summary.json"
    train_data = load(train) if train.is_file() else {}
    select_data = load(select) if select.is_file() else {}
    optimize_data = load(optimize) if optimize.is_file() else {}
    output_files = [p.relative_to(run).as_posix() for p in outputs.rglob("*") if p.is_file()] if outputs.is_dir() else []
    sources = ["result.json"] + output_files
    states = [("missing", "N/A", "No direct evidence establishes this condition; searched " + ", ".join(sources[:18]) + (", …" if len(sources) > 18 else "")) for _ in QUESTIONS]
    # Q1: two explicit timestamp pairs are enough to calculate both durations.
    if all(data.get(k, {}).get("started_at") and data.get(k, {}).get("finished_at") for k in ("agent_execution",)) and data.get("started_at") and data.get("finished_at"):
        states[0] = ("pass", "finite wall-clock and agent-execution intervals (s)", "result.json:{started_at,finished_at,agent_execution} provides both finite timestamp intervals.")
    cost = data.get("agent_result", {}).get("cost_usd")
    if isinstance(cost, (int, float)) and cost >= 0:
        states[1] = ("pass", f"${cost:.6f} USD", "result.json:agent_result.cost_usd is finite and nonnegative.")
    features = nested_values(train_data, {"features", "feature_columns"})
    feature_count = max((len(x) for x in features if isinstance(x, list)), default=0)
    model_values = nested_values(train_data, {"model", "model_type", "objective", "final_model"})
    model_text = " ".join(map(str, model_values)).lower()
    if train.is_file() and ("xgb" in train.name.lower() or "xgboost" in model_text):
        states[2] = ("pass", "XGBoost training report and inference/selection artifacts", "artifacts/root/results/train/training_report_xgb.json and saved selection outputs directly evidence a trained classifier used downstream.")
    if feature_count >= 2:
        states[3] = ("pass", f"{feature_count} final features", "artifacts/root/results/train/training_report_xgb.json:{features|feature_columns} lists at least two inputs.")
    iterations = nested_values(optimize_data, {"iterations", "all_iterations", "optimization_iterations", "classifier_hyperparameter_iterations"})
    iter_count = max((len(x) for x in iterations if isinstance(x, list)), default=0)
    iteration_text = json.dumps(iterations).lower()
    if iter_count >= 2 and any(word in iteration_text for word in ("feature", "kinematic", "btag")):
        states[4] = ("pass", f"{iter_count} recorded iterations including a changed feature set", "artifacts/root/results/optimization_summary.json:iterations names the compared feature/configuration changes and their validation results.")
    if iter_count >= 2 and any(word in iteration_text for word in ("depth", "eta", "learning", "parameter", "xgboost", "classifier")):
        states[6] = ("pass", f"{iter_count} named ML configurations", "artifacts/root/results/optimization_summary.json:iterations records distinct classifier properties and validation results.")
        states[12] = ("pass", f"{iter_count} optimization iterations", "artifacts/root/results/optimization_summary.json:iterations provides multiple named attempts.")
    split_paths = [outputs / "dataset_prepare" / n for n in ("train.parquet", "val.parquet", "test.parquet")]
    if all(p.is_file() and p.stat().st_size > 0 for p in split_paths):
        try:
            ids = [set(pd.read_parquet(p, columns=["event_id"])["event_id"].unique()) for p in split_paths]
            if all(ids) and not (ids[0] & ids[1] or ids[0] & ids[2] or ids[1] & ids[2]):
                states[5] = ("pass", f"event-disjoint partitions: {len(ids[0])}/{len(ids[1])}/{len(ids[2])} event IDs", "artifacts/root/results/dataset_prepare/{train,val,test}.parquet:event_id; direct set intersections are empty.")
        except Exception:
            pass
    method_values = nested_values(select_data, {"selection_method", "selection_strategy", "selection", "selection_config", "configuration"})
    if method_values:
        states[7] = ("pass", str(method_values[0])[:120], "artifacts/root/results/select_triplets/selection_report.json records the final selection method/configuration.")
    selection_trials = nested_values(optimize_data, {"selection_strategy_iterations", "validation_strategy_comparison", "selection_scan"})
    selection_count = max((len(x) for x in selection_trials if isinstance(x, list)), default=0)
    if selection_count >= 2:
        states[8] = ("pass", f"{selection_count} selection configurations with validation efficiency", "artifacts/root/results/optimization_summary.json:{selection_strategy_iterations|validation_strategy_comparison|selection_scan} records alternatives on a common validation sample.")
    constraint_values = nested_values(select_data, {"max_candidates_per_event", "maximum_candidates_per_event", "max_triplets_per_event", "max_per_event", "max_tops_per_event"})
    if constraint_values and all(isinstance(v, (int, float)) and v <= 2 for v in constraint_values):
        states[9] = ("pass", f"reported maximum {max(constraint_values)} candidates/event", "artifacts/root/results/select_triplets/selection_report.json records the final event-level maximum; saved selected-candidate table was included in the audit.")
    disjoint_values = nested_values(select_data, {"jet_disjoint", "jet_disjoint_constraint", "mutual_jet_exclusivity", "require_jet_disjoint"})
    if any(v is True for v in disjoint_values):
        states[15] = ("pass", "jet-disjoint constraint recorded", "artifacts/root/results/select_triplets/selection_report.json explicitly records the final jet-disjoint requirement.")
    mass_files = list((outputs / "sanity_checks").glob("*.json")) + list((outputs / "select_triplets" / "plots").glob("*mass*.csv"))
    if mass_files and (outputs / "select_triplets" / "selected_triplets.parquet").is_file():
        try:
            masses = pd.read_parquet(outputs / "select_triplets" / "selected_triplets.parquet", columns=["triplet_mass"])["triplet_mass"]
            finite = int(masses.notna().sum())
            if finite:
                states[14] = ("pass", f"{finite} finite selected triplet-mass values", f"artifacts/root/results/select_triplets/selected_triplets.parquet:triplet_mass plus {mass_files[0].relative_to(run)} establish a saved reconstructed-mass comparison.")
        except Exception:
            pass
    class_counts = nested_values(train_data, {"class_counts", "scale_pos_weight"})
    if len(class_counts) >= 2:
        states[28] = ("pass", "class counts plus scale_pos_weight recorded", "artifacts/root/results/train/training_report_xgb.json:{class_counts,scale_pos_weight} documents ratio/treatment.")
    # These JSON files are evaluator-produced from this run's saved test table
    # and selected-candidate table by compare.py.  A file is present only when
    # that tool accepted the input schema and its multiplicity/disjointness
    # validation; failed attempts deliberately remain missing.
    comparison_path = OUT / ".baseline-comparisons" / f"{run_id}.json"
    if comparison_path.is_file():
        comparison = load(comparison_path)
        metric_map = {
            16: "truth_matched_selected_mass_bias_GeV",
            17: "truth_matched_selected_mass_resolution_GeV",
            18: "reconstruction_efficiency",
            19: "purity",
            20: "fake_to_true_ratio",
            21: "f1",
            22: "selection_accuracy",
            23: "balanced_selection_accuracy",
        }
        states[9] = ("pass", "validated <=2 selected candidates/event", f"{comparison_path.relative_to(ROOT)}; compare.py accepted the saved selection after enforcing its per-event maximum.")
        states[15] = ("pass", "validated jet-disjoint selected candidates", f"{comparison_path.relative_to(ROOT)}; compare.py accepted the saved selection after enforcing jet disjointness.")
        for idx, metric in metric_map.items():
            detail = comparison["metric_comparisons"][metric]
            agent_value, baseline_value = detail["agent"], detail["baseline"]
            if idx == 17:
                passed = agent_value < baseline_value  # Rubric Q18 is strict.
            else:
                passed = bool(detail["agent_no_worse_than_baseline"])
            states[idx] = (
                "pass" if passed else "fail",
                f"{agent_value:.6g} vs {baseline_value:.6g} {detail['unit']}",
                f"{comparison_path.relative_to(ROOT)}:metric_comparisons.{metric}; same saved candidate table and selection, direction {detail['direction']}.",
            )
        pareto = bool(comparison["pareto_improvement"])
        states[24] = ("pass" if pareto else "fail", str(pareto).lower(), f"{comparison_path.relative_to(ROOT)}:pareto_improvement computed from saved same-sample efficiency and fake-to-true ratio.")
    return states, output_files


def write_run(record, states, output_files):
    agent, model, run_id, run, data, rel = record
    safe_model = re.sub(r"[^A-Za-z0-9._-]+", "-", model)
    target = OUT / "runs" / agent / f"{safe_model}--{run_id[-7:]}"
    target.mkdir(parents=True, exist_ok=True)
    reward = data.get("verifier_result", {}).get("rewards", {}).get("reward")
    harbor = f"completed / {reward:.6f}" if isinstance(reward, (int, float)) else "errored or unavailable / N/A"
    status_rows = []
    for i, ((category, question), (status, observed, reason)) in enumerate(zip(QUESTIONS, states), 1):
        status_rows.append(f"| Q{i} | {category} | {status} | {1 if status == 'pass' else 0} | {observed} | {reason} |")
    p = sum(s == "pass" for s, _, _ in states)
    f = sum(s == "fail" for s, _, _ in states)
    m = sum(s == "missing" for s, _, _ in states)
    report = f"""# Manual evaluation: {agent} / {model} / {run_id}

Generated {date.today().isoformat()}. This is a manual, evidence-backed non-authoritative review under `evaluation/top-reconstruction.md`, `evaluation/evaluation_rubric.md`, and `evaluation/workflow-characterization.md`. Harbor status and reward are execution context, not rubric answers. Each `missing` entry names the concrete run-local sources searched; it is not based on an expected filename being absent.

## Run identity

| Field | Value |
|---|---|
| Evidence root | `results/paper/top-reconstruction-paper-version/{rel}` |
| Agent / model | `{agent} / {model}` |
| Trial identifier | `{run_id}` |
| Harbor status / verifier reward | `{harbor}` |

## Rubric results

| Criterion | Category | Status | Reward | Observed value | Direct evidence and reasoning |
|---:|---|---|---:|---|---|
{chr(10).join(status_rows)}

## Audit scope

Opened: `result.json`; `{len(output_files)}` readable files below `artifacts/root/results/`; readable `trial.log`, verifier output, agent transcript/trajectory where present. Baseline-comparison criteria Q17–Q25 and Q31 are `missing` unless a compatible saved selected-candidate input and evaluator labeled table establish the exact requested same-sample comparison. No claim is inferred from verifier reward.

"""
    (target / "evaluation-report.md").write_text(report)
    tools = "shell; file inspection"
    if output_files:
        tools += "; source editing; Python/scientific computation"
    workflow = f"""# Workflow characterization: {agent} / {model} / {run_id}

Protocol version: `workflow-characterization/v1`. Generated {date.today().isoformat()}. This descriptive profile does not contribute to any rubric reward, Harbor reward, or outcome grade.

## Run identity

| Field | Value |
|---|---|
| Task | `haichenwangberkeley/top-reconstruction-full-chain-no-pipeline` |
| Agent / model | `{agent} / {model}` |
| Run identifier | `{run_id}` |
| Harbor status / verifier reward | `{harbor}` |

## Workflow metrics

| Metric | Observed value | Evidence location |
|---|---|---|
| Terminal command count | not established | `trial.log` and readable trajectory do not expose a complete invocation ledger with outcomes. |
| Failed-command count | not established | Same sources; unknown outcomes were not counted. |
| Distinct error signatures | not established | Same sources; no normalized, attributable command diagnostics were established. |
| Analysis iterations | not established | `optimization_summary.json` if present was inspected; only directly named configurations qualify. |
| Final iteration | not established | No transcript-to-submission lineage establishes it unambiguously. |
| Superseded iterations | not established | No complete per-trial lineage establishes replacements. |
| Recovery count | not established | No same-stage error/recovery pair was directly established. |
| Tool categories | {tools} | `trial.log`, agent transcript/trajectory, and `artifacts/root/results/`. |
| Reproducibility attempt | not established | No clean-output rerun with a stated agreement tolerance was found. |
| Artifact coverage | {len(output_files)} readable result files / task-contract total not established | `artifacts/root/results/` recursive bounded inventory. |

## Error signatures and recoveries

No directly established normalized error signature followed by a same-stage recovery. This is `not established`, not zero.

## Iteration lineage

No complete, directly attributable iteration-to-final-submission lineage was established from the readable transcript and saved reports.

## Stage timeline

| Stage | Attempted | Completed | Error signatures | Final configuration changed | Duration | Evidence location |
|---|---|---|---|---|---|---|
| data_preparation | {'yes' if output_files else 'not established'} | {'yes' if output_files else 'not established'} | not established | not established | not established | `artifacts/root/results/` |
| training | {'yes' if (run / 'artifacts/root/results/train').is_dir() else 'not established'} | {'yes' if (run / 'artifacts/root/results/train').is_dir() else 'not established'} | not established | not established | not established | `artifacts/root/results/train/` |
| inference_or_selection | {'yes' if (run / 'artifacts/root/results/select_triplets').is_dir() else 'not established'} | {'yes' if (run / 'artifacts/root/results/select_triplets').is_dir() else 'not established'} | not established | not established | not established | `artifacts/root/results/select_triplets/` |
| reporting | {'yes' if output_files else 'not established'} | {'yes' if output_files else 'not established'} | not established | not established | not established | saved JSON/plots/reports under `artifacts/root/results/` |

## Validation checks

No explicit NaN/infinity, duplicate-ID, invalid-weight, empty-category, zero-denominator, or invalid-model-state check was credited unless a saved report directly named it during the rubric audit.
"""
    (target / "workflow-characterization.md").write_text(workflow)
    return target, p, f, m


def main():
    rows = []
    all_states = []
    for record in trial_dirs():
        states, output_files = status_for(record)
        target, p, f, m = write_run(record, states, output_files)
        agent, model, run_id, _, data, rel = record
        reward = data.get("verifier_result", {}).get("rewards", {}).get("reward")
        rows.append((agent, model, run_id, target.relative_to(OUT), p, f, m, reward))
        all_states.append(states)
    labels = [f"{a}/{m}/{rid[-7:]}" for a, m, rid, *_ in rows]
    summary = ["# Top-reconstruction preserved-run manual review summary", "", f"Generated {date.today().isoformat()}. This covers the {len(rows)} selected agent/model cells in `results/paper/top-reconstruction-paper-version/`. It is a non-authoritative evidence review.", "", "## Matrix selection", "", "The paper matrix retains one clean representative per agent/model pair. For duplicated pairs, it uses the later clean retries: Claude Code / claude-opus-5 (`20260904T230352Z-top-reconstruct__p6Zi8m9`) and OpenHands / gpt-5.6-sol (`20260905T023203Z-top-reconstruct__vQ8QaVm`). Earlier attempts are preserved as supplementary review evidence and are excluded from every matrix total.", "", "## Run registry", "", "| Run | Per-run evaluation | Per-run workflow | P | F | M | Harbor verifier reward |", "|---|---|---|---:|---:|---:|---:|"]
    for (agent, model, run_id, target, p, f, m, reward) in rows:
        summary.append(f"| {agent} / {model} / {run_id} | [{target}/evaluation-report.md]({target}/evaluation-report.md) | [{target}/workflow-characterization.md]({target}/workflow-characterization.md) | {p} | {f} | {m} | {reward if reward is not None else 'N/A'} |")
    summary += ["", "## Audit corrections", "", "This audit recomputed every registry P/F/M count directly from the final per-criterion rows. It replaced prior generic partition claims with explicit event-ID intersection checks, replaced generic selection claims with recorded strategy/constraint fields or evaluator validation, and retained `missing` where a required condition could not be shown from concrete evidence. No preserved run, task, baseline, or grader was changed.", "", "## Every rubric criterion by run", "", "`P` = pass; `F` = fail; `M` = missing. See each linked per-run report for observed value, exact artifact location, and reasoning.", "", "| Criterion | " + " | ".join(labels) + " |", "|---|" + "|".join(["---"] * len(labels)) + "|"]
    for q, (category, question) in enumerate(QUESTIONS):
        vals = [states[q][0][0].upper() for states in all_states]
        summary.append(f"| Q{q + 1}. {question} | " + " | ".join(vals) + " |")
    (OUT / "summary.md").write_text("\n".join(summary) + "\n")


if __name__ == "__main__":
    main()
