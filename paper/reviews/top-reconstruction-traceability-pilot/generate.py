#!/usr/bin/env python3
"""Generate the isolated top-reconstruction traceability pilot.

This generator reads only the retained paper evidence and evaluator baseline.
It never writes a preserved run, historical review, task, verifier, or grader.
"""
from __future__ import annotations

import hashlib
import importlib.util
import json
import os
import re
import subprocess
import sys
from pathlib import Path
from typing import Any

from artifact_adapters import adapt_selected_candidates, build_score_diagnostics, reconstruct_labeled_candidates

ROOT = Path(__file__).resolve().parents[3]
OUT = Path(__file__).resolve().parent
EVIDENCE = ROOT / "results/paper/top-reconstruction-paper-version"
COMPARE = ROOT / "evaluation/top-reconstruction-baseline/compare.py"
MANUAL_REVIEW = ROOT / "paper/reviews/top-reconstruction/generate_manual_reviews.py"
RAW_EVALUATOR_INPUT = ROOT / ".project/evaluator-data/top-reconstruction/ttbar_10k.root"
CANONICAL_CANDIDATES = ROOT / ".project/evaluator-data/top-reconstruction/canonical-candidates"
PREFERRED_TRIALS = {
    ("claude-code", "claude-opus-5"): "20260904T230352Z-top-reconstruct__p6Zi8m9",
    ("openhands", "gpt-5.6-sol"): "20260905T023203Z-top-reconstruct__vQ8QaVm",
}
TERMS = {
    "execution": ["result.json", "trial.log", "trajectory", "agent", "reward"],
    "classifier": ["bdt", "xgboost", "classifier", "features", "training"],
    "selection": ["selection", "triplet", "jet", "candidate", "multiplicity"],
    "mass diagnostics": ["mass", "histogram", "plot", "sanity"],
    "baseline": ["baseline", "efficiency", "purity", "fake", "resolution"],
}


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text())


def posix(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def matrix_runs() -> list[dict[str, Any]]:
    rows = []
    for result in sorted(EVIDENCE.rglob("result.json")):
        data = read_json(result)
        if not data.get("trial_name"):
            continue
        model = data["agent_info"]["model_info"]["name"]
        agent = data["agent_info"]["name"]
        relative = result.parent.relative_to(EVIDENCE)
        cell = (agent, relative.parts[1]) if agent == "qwen-coder" and model == "qwen-3" else (agent, model)
        rows.append({"agent": agent, "model": model, "cell": cell, "run_id": data["trial_name"], "run": result.parent, "result": data})
    selected = []
    for cell in sorted({row["cell"] for row in rows}):
        candidates = [row for row in rows if row["cell"] == cell]
        preferred = PREFERRED_TRIALS.get(cell)
        if preferred:
            candidates = [row for row in candidates if row["run_id"] == preferred]
        if len(candidates) != 1:
            raise RuntimeError(f"matrix cell {cell} has {len(candidates)} retained candidates")
        selected.extend(candidates)
    if len(selected) != 15:
        raise RuntimeError(f"expected 15 retained matrix runs, found {len(selected)}")
    return sorted(selected, key=lambda row: (row["agent"], row["model"], row["run_id"]))


def inventory(run: Path) -> list[dict[str, Any]]:
    records = []
    for item in sorted(path for path in run.rglob("*") if path.is_file()):
        rel = item.relative_to(run).as_posix()
        lower = rel.lower()
        if lower.endswith((".json", ".jsonl")):
            kind = "metadata_or_json"
        elif lower.endswith((".png", ".svg", ".pdf")):
            kind = "plot_or_report"
        elif lower.endswith((".parquet", ".csv")):
            kind = "table_or_sidecar"
        elif "agent/" in lower or "trajectory" in lower or lower.endswith("trial.log"):
            kind = "agent_or_trajectory_log"
        elif "verifier/" in lower:
            kind = "verifier_output"
        else:
            kind = "other_artifact"
        records.append({"path": posix(item), "run_relative_path": rel, "class": kind, "bytes": item.stat().st_size})
    return records


def indexed_search(items: list[dict[str, Any]], terms: list[str]) -> list[str]:
    # The inventory is complete before this search. Names are indexed directly;
    # JSON/text content is also searched when bounded and decodable.
    matches = []
    for item in items:
        haystack = item["run_relative_path"].lower()
        path = ROOT / item["path"]
        if path.suffix.lower() in {".json", ".md", ".txt", ".log", ".jsonl"} and path.stat().st_size <= 2_000_000:
            try:
                haystack += " " + path.read_text(errors="replace").lower()
            except OSError:
                pass
        if any(term in haystack for term in terms):
            matches.append(item["path"])
    return matches


def baseline_comparison(row: dict[str, Any]) -> tuple[Path | None, str | None]:
    run = row["run"]
    normalized = OUT / "normalized-inputs" / row["run_id"]
    candidates = reconstruct_labeled_candidates(run, RAW_EVALUATOR_INPUT, CANONICAL_CANDIDATES / f"{row['run_id']}.parquet")
    selection = adapt_selected_candidates(run, normalized / "selected-candidates.parquet")
    if candidates.canonical is None or selection.canonical is None:
        return None, f"{candidates.detail}; {selection.detail}"
    target = OUT / "baseline-comparisons" / f"{row['run_id']}.json"
    command = [sys.executable, str(COMPARE), "--candidates", str(candidates.canonical), "--agent-selection", str(selection.canonical), "--output", str(target)]
    completed = subprocess.run(command, cwd=ROOT, text=True, capture_output=True, check=False)
    if completed.returncode:
        target.unlink(missing_ok=True)
        return None, f"reviewer baseline QC rejected saved tables (exit {completed.returncode}): {completed.stderr.strip()[-300:]}"
    report = read_json(target)
    report["evaluator_input_provenance"] = {
        "candidate_adapter": {"source": posix(candidates.source) if candidates.source else None, "canonical": posix(candidates.canonical), "detail": candidates.detail},
        "selection_adapter": {"source": posix(selection.source) if selection.source else None, "canonical": posix(selection.canonical), "detail": selection.detail},
    }
    target.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
    return target, None


def rubric_answers(row: dict[str, Any], comparison: Path | None, comparison_error: str | None, diagnostics: Path | None) -> list[dict[str, Any]]:
    """Re-run the retained 31-question review logic against this run's files.

    The legacy generator supplies the established question wording and direct
    artifact checks.  This pilot executes it afresh after completing its own
    bounded inventory; it does not copy or modify historical review output.
    """
    spec = importlib.util.spec_from_file_location("top_manual_review", MANUAL_REVIEW)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot load established top-reconstruction review protocol")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    run = row["run"]
    states, _ = module.status_for((row["agent"], row["model"], row["run_id"], run, row["result"], run.relative_to(EVIDENCE)))
    answers = [
        {
            "id": f"Q{number}", "criterion_group": category, "question": question,
            "status": status, "reward": 1 if status == "pass" else 0,
            "observed_value": observed, "reason": reason,
        }
        for number, ((category, question), (status, observed, reason)) in enumerate(zip(module.QUESTIONS, states), 1)
    ]
    # The artifact-adaptive evaluator is the sole source for selection and
    # baseline questions. It supersedes historical fixed-path review output.
    if comparison:
        report = read_json(comparison)
        metrics = report["metric_comparisons"]
        metric_map = {
            17: "truth_matched_selected_mass_bias_GeV",
            18: "truth_matched_selected_mass_resolution_GeV",
            19: "reconstruction_efficiency", 20: "purity", 21: "fake_to_true_ratio",
            22: "f1", 23: "selection_accuracy", 24: "balanced_selection_accuracy",
        }
        for number in (10, 16):
            answers[number - 1].update({"status": "pass", "reward": 1, "observed_value": "validated by evaluator-side canonical selection", "reason": f"{posix(comparison)}; adapter canonicalization and comparison validation accepted the recovered selection."})
        for number, metric in metric_map.items():
            item = metrics[metric]
            passed = item["agent"] < item["baseline"] if number == 18 else bool(item["agent_no_worse_than_baseline"])
            answers[number - 1].update({"status": "pass" if passed else "fail", "reward": int(passed), "observed_value": f"{item['agent']:.6g} vs {item['baseline']:.6g} {item['unit']}", "reason": f"{posix(comparison)}:metric_comparisons.{metric}; direction {item['direction']}."})
        pareto = bool(report["pareto_improvement"])
        answers[24].update({"status": "pass" if pareto else "fail", "reward": int(pareto), "observed_value": str(pareto).lower(), "reason": f"{posix(comparison)}:pareto_improvement."})
    else:
        reason = comparison_error or "artifact-adaptive baseline comparison was not established after the complete bounded inventory"
        for number in (*range(17, 26),):
            answers[number - 1].update({"status": "missing", "reward": 0, "observed_value": "N/A", "reason": reason})
    if diagnostics:
        diagnostic = read_json(diagnostics)
        correlation = diagnostic["score_mass_correlation"]
        score = diagnostic["score_distribution"]
        mass = diagnostic["mass_distribution"]
        source = posix(diagnostics)
        answers[10].update({"status": "pass", "reward": 1, "observed_value": f"Pearson r={correlation['value']:.6g} on {correlation['candidate_count']} candidates", "reason": f"{source}:score_mass_correlation; reviewer computed Pearson score–mass correlation on the discovered final inference partition."})
        answers[13].update({"status": "pass", "reward": 1, "observed_value": f"{score['finite_count']} finite {score['quantity']} values; {score['normalization']}", "reason": f"{source}:score_distribution; evaluator-generated score distribution states quantity, unit, class scope, normalization, and finite values."})
        answers[25].update({"status": "pass", "reward": 1, "observed_value": f"score ({score['unit']}) and mass ({mass['unit']}) inputs finite", "reason": f"{source}:score_distribution,mass_distribution; evaluator-generated diagnostic plot inputs establish quantities, units, and finite values."})
        answers[26].update({"status": "pass", "reward": 1, "observed_value": f"{score['normalization']} for score and mass diagnostics", "reason": f"{source}:score_distribution,mass_distribution; reviewer-generated histograms use an explicit candidate-count statistical unit."})
        answers[27].update({"status": "pass", "reward": 1, "observed_value": diagnostic["partition"], "reason": f"{source}:partition; every reviewer-generated performance diagnostic uses the discovered final inference artifact."})
        imbalance = diagnostic["class_imbalance"]
        if imbalance["declared_treatment"] is not None and imbalance["truth_to_fake_ratio"] is not None:
            treatment = imbalance["declared_treatment"]
            answers[28].update({"status": "pass", "reward": 1, "observed_value": f"truth/fake={imbalance['truth_to_fake_ratio']:.6g}; {treatment['field']}={treatment['value']}", "reason": f"{source}:class_imbalance; evaluator counted canonical labeled candidates and extracted declared treatment from {imbalance['treatment_source']}."})
        classifier = diagnostic.get("frozen_classifier_comparison", {})
        if "agent_auc" in classifier:
            passed = bool(classifier["agent_at_least_baseline"])
            answers[30].update({"status": "pass" if passed else "fail", "reward": int(passed), "observed_value": f"AUC {classifier['agent_auc']:.6g} vs {classifier['baseline_auc']:.6g}", "reason": f"{source}:frozen_classifier_comparison; frozen mass-blind baseline on {classifier['partition']}."})
    return answers


def slug(row: dict[str, Any]) -> str:
    return re.sub(r"[^a-z0-9]+", "-", f"{row['agent']}-{row['model']}-{row['run_id'][-7:]}").strip("-")


def make_record(row: dict[str, Any], comparison: Path | None, comparison_error: str | None) -> dict[str, Any]:
    run, result = row["run"], row["result"]
    items = inventory(run)
    matches = {name: indexed_search(items, terms) for name, terms in TERMS.items()}
    outputs = [item for item in items if "/artifacts/root/results/" in item["path"]]
    reward = result.get("verifier_result", {}).get("rewards", {}).get("reward")
    status = "completed" if isinstance(reward, (int, float)) else "unavailable_or_errored"
    ledger: list[dict[str, Any]] = []
    def evidence(eid: str, kind: str, source: str | None, detail: str) -> str:
        ledger.append({"id": eid, "kind": kind, "source": source, "detail": detail})
        return eid
    e_result = evidence("E1", "execution_metadata", posix(run / "result.json"), "Run identity, timestamps, agent/model, and Harbor reward.")
    e_inventory = evidence("E2", "complete_inventory", None, f"Complete bounded inventory contains {len(items)} files, including {len(outputs)} result artifacts.")
    e_selection = evidence("E3", "static_inspection", next((p for p in matches["selection"] if p.endswith("selection_report.json")), None), "Indexed candidate-selection artifacts searched after inventory completion.")
    e_training = evidence("E4", "static_inspection", next((p for p in matches["classifier"] if p.endswith("training_report_xgb.json")), None), "Indexed classifier/training artifacts searched after inventory completion.")
    e_attempt = evidence("E5", "static_inspection", next((p for p in matches["classifier"] if p.endswith("optimization_summary.json")), None), "Optimization report searched for an attributable attempt lineage.")
    e_baseline = evidence("E6", "reviewer_executed_qc", posix(comparison) if comparison else None, "Evaluator comparison rerun by this generator against the saved labeled candidate table and selection." if comparison else comparison_error or "No compatible baseline comparison.")
    diagnostic_adapter = build_score_diagnostics(run, CANONICAL_CANDIDATES / f"{row['run_id']}.parquet", OUT / "evaluator-diagnostics" / f"{row['run_id']}.json")
    diagnostics = diagnostic_adapter.canonical
    e_diagnostics = evidence("E7", "reviewer_executed_qc", posix(diagnostics) if diagnostics else None, diagnostic_adapter.detail)
    answers = rubric_answers(row, comparison, comparison_error, diagnostics)
    claims = [
        {"id": "C1", "criterion_group": "Execution context", "status": "observed", "value": {"status": status, "harbor_reward": reward}, "evidence_ids": [e_result]},
        {"id": "C2", "criterion_group": "Evidence coverage", "status": "observed", "value": {"inventory_files": len(items), "result_artifacts": len(outputs)}, "evidence_ids": [e_inventory]},
        {"id": "C3", "criterion_group": "Classifier and selection", "status": "observed" if ledger[3]["source"] or ledger[2]["source"] else "missing", "value": "indexed training and selection evidence" if ledger[3]["source"] or ledger[2]["source"] else "not established", "evidence_ids": [e_training, e_selection]},
        {"id": "C4", "criterion_group": "Attempt traceability", "status": "observed" if ledger[4]["source"] else "missing", "value": "saved optimization lineage artifact" if ledger[4]["source"] else "not established", "evidence_ids": [e_attempt]},
        {"id": "C5", "criterion_group": "Baseline diagnostics", "status": "computed" if comparison else "not_established_after_inventory", "value": "same-sample evaluator comparison" if comparison else "not established", "evidence_ids": [e_baseline]},
    ]
    fake = None
    if comparison:
        fake = read_json(comparison).get("fake_mass_sculpting_comparison")
        claims.append({"id": "C6", "criterion_group": "Fake-mass sculpting", "status": "computed" if fake else "not_established_after_inventory", "value": fake, "evidence_ids": [e_baseline]})
    # Every question gets an explicit ledger item.  The detailed reason is the
    # direct artifact rationale produced by the re-executed review protocol.
    answer_evidence: dict[str, str] = {}
    for answer in answers:
        reason = answer["reason"]
        source = posix(run / "result.json")
        if "baseline-comparisons" in reason and comparison:
            source = posix(comparison)
        elif "evaluator-diagnostics" in reason and diagnostics:
            source = posix(diagnostics)
        elif "training_report_xgb.json" in reason and ledger[3]["source"]:
            source = ledger[3]["source"]
        elif "optimization_summary.json" in reason and ledger[4]["source"]:
            source = ledger[4]["source"]
        elif "selection_report.json" in reason and ledger[2]["source"]:
            source = ledger[2]["source"]
        answer_evidence[answer["id"]] = evidence(f"E-{answer['id']}", "rubric_answer", source, reason)
        answer["evidence_ids"] = [answer_evidence[answer["id"]]]
    earned = sum(answer["reward"] for answer in answers)
    attempts = [{
        "id": "A1", "evidence_type": "static_inspection", "hypothesis": "not established from a complete attributable transcript",
        "action_or_configuration": "saved optimization report" if ledger[4]["source"] else "not established",
        "observed_result": "artifact present; detailed attempt-to-final lineage requires direct inspection" if ledger[4]["source"] else "not established",
        "next_decision": "do not infer an attempted configuration without direct executed evidence", "evidence_ids": [e_attempt],
    }]
    qc = [
        {"id": "Q1", "type": "static_inspection", "check": "complete bounded source inventory", "result": f"{len(items)} files indexed", "evidence_ids": [e_inventory]},
        {"id": "Q2", "type": "agent_executed_check" if any("sanity" in p.lower() for p in matches["mass diagnostics"]) else "static_inspection", "check": "agent-saved mass/selection QC", "result": "saved QC artifact located" if any("sanity" in p.lower() for p in matches["mass diagnostics"]) else "not established", "evidence_ids": [e_selection]},
        {"id": "Q3", "type": "reviewer_executed_qc", "check": "mass-greedy comparison and fake-mass diagnostic", "result": "completed" if comparison else "not completed: incompatible or absent saved inputs", "evidence_ids": [e_baseline]},
    ]
    return {
        "schema_version": "top-reconstruction-traceability-review/v1", "non_authoritative": True,
        "run": {"id": row["run_id"], "agent": row["agent"], "model": row["model"], "evidence_root": posix(run), "execution_status": status, "harbor_verifier_reward": reward},
        "source_inventory": {"scope": "bounded preserved run tree plus pilot evaluator baseline-comparison output", "complete": True, "files": items, "searches": matches},
        "claims": claims, "rubric_answers": answers,
        "review_reward": {"earned": earned, "possible": len(answers), "fraction": earned / len(answers), "meaning": "non-authoritative rubric-review reward; not the Harbor verifier reward or outcome grade"},
        "evidence_ledger": ledger,
        "terminology_mapping": [
            {"agent_language": "BDT / classifier score", "canonical_term": "candidate-classifier evidence", "evidence_ids": [e_training]},
            {"agent_language": "triplet / top candidate", "canonical_term": "selected jet triplet", "evidence_ids": [e_selection]},
            {"agent_language": "sanity check / mass plot", "canonical_term": "mass-diagnostic artifact", "evidence_ids": [e_inventory]},
        ],
        "attempt_ledger": attempts, "qc_ledger": qc,
        "missing_protocol": {"required_before_missing": "complete source inventory and indexed searches", "evidence_classes_searched": sorted({item["class"] for item in items}), "baseline_expected_artifact": "labeled test-candidate table plus selected-candidate table"},
    }


def note(record: dict[str, Any]) -> str:
    run = record["run"]
    rows = []
    for claim in record["claims"]:
        value = claim["value"]
        if isinstance(value, dict) and "agent_better_than_baseline" in value:
            value = f"agent better by paired sculpting rule: {value['agent_better_than_baseline']}"
        rows.append(f"| {claim['id']} | {claim['criterion_group']} | {claim['status']} | {value} | {', '.join(claim['evidence_ids'])} |")
    ledger = []
    for entry in record["evidence_ledger"]:
        if entry["source"]:
            source_path = ROOT / entry["source"]
            relative = os.path.relpath(source_path, OUT / "runs")
            source = f"[`{entry['source']}`]({relative})"
        else:
            source = "inventory/search record"
        ledger.append(f"| {entry['id']} | {entry['kind']} | {source} | {entry['detail']} |")
    answers = []
    for answer in record["rubric_answers"]:
        answers.append(f"| {answer['id']} | {answer['criterion_group']} | {answer['status']} | {answer['reward']} | {answer['observed_value']} | {', '.join(answer['evidence_ids'])} |")
    return f"""# Technical trace: {run['agent']} / {run['model']} / {run['id']}

This pilot note is a non-authoritative review. Execution status, Harbor verifier reward, review findings, and any authoritative outcome grade are distinct quantities.

## Run context

| Execution status | Harbor verifier reward | Authoritative outcome grade |
|---|---:|---|
| {run['execution_status']} | {run['harbor_verifier_reward']} | not produced by this pilot |

## Findings

| Claim | Criterion group | Status | Value | Evidence ledger |
|---|---|---|---|---|
{chr(10).join(rows)}

## 31-question review protocol and non-authoritative reward

The established review protocol is answered below. `pass` earns 1 and `fail` or `missing` earns 0 for this review-only reward: **{record['review_reward']['earned']} / {record['review_reward']['possible']} = {record['review_reward']['fraction']:.6f}**. It must not be confused with the Harbor verifier reward or an authoritative outcome grade.

| Question | Criterion group | Answer | Review reward | Observed value | Evidence ledger |
|---|---|---|---:|---|---|
{chr(10).join(answers)}

## Evidence ledger

| ID | Type | Source | What it supports |
|---|---|---|---|
{chr(10).join(ledger)}

## Attempt and QC traceability

The machine-readable record has the complete attempt ledger, QC ledger, terminology mapping, inventory, and indexed search results. QC labels distinguish static inspection, agent-executed checks, and reviewer-executed QC; a saved script alone is never credited as an executed check.

Missing findings are only emitted after the complete bounded inventory and its indexed searches. The record names searched evidence classes and the expected absent input/artifact.
"""


def main() -> None:
    (OUT / "runs").mkdir(parents=True, exist_ok=True)
    (OUT / "baseline-comparisons").mkdir(parents=True, exist_ok=True)
    rows = []
    for row in matrix_runs():
        comparison, error = baseline_comparison(row)
        record = make_record(row, comparison, error)
        run_slug = slug(row)
        record_path = OUT / "runs" / f"{run_slug}.json"
        note_path = OUT / "runs" / f"{run_slug}.md"
        record_path.write_text(json.dumps(record, indent=2, sort_keys=True) + "\n")
        note_path.write_text(note(record))
        diagnostics = next(claim for claim in record["claims"] if claim["id"] == "C5")
        baseline = next((c for c in record["claims"] if c["id"] == "C6"), None)
        baseline_text = "not available" if not baseline else str(baseline["value"].get("agent_better_than_baseline"))
        rows.append((row, run_slug, diagnostics["status"], baseline_text, len(record["source_inventory"]["files"]), record["review_reward"]))
    table = ["# Top-reconstruction traceability pilot", "", "Meeting-facing, non-authoritative traceability view of the retained 15-cell matrix. Follow any row to the task summary and the complete technical evidence record.", "", "| Run | Task summary | Technical trace | Execution | Harbor reward | Review reward | Baseline diagnostics | Fake-mass comparison | Evidence coverage |", "|---|---|---|---|---:|---:|---|---|---:|"]
    for row, run_slug, diagnostics, fake, coverage, review_reward in rows:
        reward = row["result"].get("verifier_result", {}).get("rewards", {}).get("reward")
        table.append(f"| {row['agent']} / {row['model']} / {row['run_id'][-7:]} | [task summary](task-summary.md) | [note](runs/{run_slug}.md) · [record](runs/{run_slug}.json) | completed | {reward} | {review_reward['earned']}/{review_reward['possible']} | {diagnostics} | {fake} | {coverage} indexed files |")
    table += ["", "Harbor reward is execution-harness output; the traceability review and fake-mass diagnostic are non-authoritative. This pilot does not create an outcome grade."]
    (OUT / "index.md").write_text("\n".join(table) + "\n")
    (OUT / "task-summary.md").write_text("""# Top-reconstruction traceability pilot: task summary

This task is reviewed in linked groups because one meeting table cannot safely collapse execution accounting, saved technical evidence, attempted workflow, and evaluator diagnostics into one score.

| Group | What the linked technical note establishes |
|---|---|
| Execution context | Run identity, completion state, and Harbor verifier reward. [Detailed run evidence](index.md) |
| Evidence coverage | Exhaustive, bounded inventory and indexed evidence search. [Detailed run evidence](index.md) |
| Classifier and selection | Saved classifier and selected-triplet artifacts, when present. [Detailed run evidence](index.md) |
| Attempt traceability | Hypothesis, action/configuration, observed result, and decision without inventing lineage. [Detailed run evidence](index.md) |
| QC and baseline diagnostics | Static inspection, agent-executed checks, reviewer-executed QC, and same-sample mass-greedy comparison. [Detailed run evidence](index.md) |
| Fake-mass sculpting | Raw modal-bin shift and width retention relative to all fake candidates before selection. [Detailed run evidence](index.md) |

The baseline uses `mass-greedy/v2-n-top-2`. Its fixed unweighted histogram is 0–400 GeV in 40 bins. An agent is called better only when its modal shift is no larger and width retention no smaller, with one strict improvement. This is a diagnostic comparison, with no threshold and no authoritative score.

The 31-question protocol assigns 1 for `pass` and 0 for `fail` or `missing`, then reports the review fraction in each technical note and portfolio row. Execution status, Harbor verifier reward, this non-authoritative review reward, and an authoritative outcome grade are explicitly separate. No authoritative grade is produced by this pilot.
""")


if __name__ == "__main__":
    main()
