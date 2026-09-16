#!/usr/bin/env python3
"""Audit top-reconstruction bundles for recoverable, uncopied source.

This is a protocol-development diagnostic.  It makes no physics score and does
not infer a method from a result, plot, or report.  It only classifies copied
files and direct code-writing/execution evidence in preserved transcripts.
"""
from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[3]
RUNS = ROOT / "results/paper/top-reconstruction-paper-version"
OUT = Path(__file__).resolve().parent

EXECUTE = re.compile(r"(?:python3?|uv run python)\s+([/A-Za-z0-9_.-]+\.py)")
WRITE = re.compile(r"(?:cat|tee|printf)\b[^\n]{0,700}?>\s*([/A-Za-z0-9_.-]+\.(?:py|sh))")
CODE_PAYLOAD = re.compile(r"write_file|apply_patch|create_file|replace_file")
HEREDOC = re.compile(r"<<")


def posix(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def read_text(path: Path) -> str:
    try:
        return path.read_text(errors="ignore")
    except OSError:
        return ""


def metadata(run: Path) -> dict[str, Any]:
    try:
        payload = json.loads((run / "result.json").read_text())
    except (OSError, json.JSONDecodeError):
        payload = {}
    agent_info = payload.get("agent_info") or {}
    model_info = agent_info.get("model_info") or {}
    verifier = payload.get("verifier_result") or {}
    rewards = verifier.get("rewards") or {}
    exception = payload.get("exception_info")
    return {
        "run_id": payload.get("trial_name", payload.get("run_id", run.name)),
        "agent": agent_info.get("name", run.parts[-3] if len(run.parts) > 2 else "unknown"),
        "model": model_info.get("name", (payload.get("config") or {}).get("agent", {}).get("model_name", "unknown")),
        "status": "errored" if exception else "completed",
        "harbor_reward": rewards.get("reward", payload.get("verifier_reward", payload.get("reward"))),
    }


def inventory(run: Path) -> dict[str, list[str]]:
    groups: dict[str, list[str]] = {
        "final_output_artifacts": [], "agent_session_trajectory_logs": [],
        "terminal_recordings": [], "native_tool_call_telemetry": [],
        "copied_workspace_source": [], "model_report_metadata": [],
    }
    for path in sorted(p for p in run.rglob("*") if p.is_file()):
        rel = path.relative_to(run).as_posix()
        lower = rel.lower()
        if rel.startswith("artifacts/root/results/"):
            groups["final_output_artifacts"].append(rel)
        if rel.startswith("agent/") and ("session" in lower or "trajectory" in lower or path.name.endswith((".jsonl", ".txt"))):
            groups["agent_session_trajectory_logs"].append(rel)
        if path.suffix in {".cast", ".pane"}:
            groups["terminal_recordings"].append(rel)
        if rel.startswith("agent/") and ("events/" in rel or "completion" in lower or path.name.endswith(".jsonl")):
            groups["native_tool_call_telemetry"].append(rel)
        if rel.startswith("artifacts/root/") and not rel.startswith("artifacts/root/results/") and path.suffix in {".py", ".ipynb", ".sh"}:
            groups["copied_workspace_source"].append(rel)
        if path.name in {"result.json", "config.json", "lock.json", "manifest.json"} or "report" in lower or "model" in lower:
            groups["model_report_metadata"].append(rel)
    return groups


def audit_run(run: Path) -> dict[str, Any]:
    info = metadata(run)
    groups = inventory(run)
    transcript_paths = sorted({
        *groups["agent_session_trajectory_logs"], *groups["terminal_recordings"],
        *groups["native_tool_call_telemetry"],
        *[p.relative_to(run).as_posix() for p in run.glob("*.log")],
    })
    commands: set[str] = set()
    writes: set[str] = set()
    code_payload_paths: list[str] = []
    heredoc_paths: list[str] = []
    for rel in transcript_paths:
        text = read_text(run / rel)
        commands.update(EXECUTE.findall(text))
        writes.update(WRITE.findall(text))
        if CODE_PAYLOAD.search(text):
            code_payload_paths.append(rel)
        if HEREDOC.search(text):
            heredoc_paths.append(rel)

    final = groups["final_output_artifacts"]
    train_or_model = [path for path in final if any(word in path.lower() for word in ("train", "model"))]
    selection = [path for path in final if any(word in path.lower() for word in ("select", "selection"))]
    direct = groups["copied_workspace_source"]
    construction = sorted(set(code_payload_paths + heredoc_paths))
    if direct:
        state = "recoverable_final_code"
        gap = "none"
        rule = "Read the copied source artifact directly; retain its path in the evidence ledger."
    elif construction:
        state = "recoverable_from_transcript"
        gap = "evaluator_adapter_gap"
        rule = "Parse shell heredocs/redirections and native write or patch payloads into reviewer-generated recovered-source files; do not execute them."
    elif commands:
        state = "execution_without_recoverable_code"
        gap = "Harbor_artifact_collection_gap"
        rule = "Record the command only. Future collection should copy files created or modified outside results/**, with a manifest."
    else:
        state = "genuinely_absent_evidence"
        gap = "genuinely_absent_evidence"
        rule = "No safe recovery rule: retain the explicit missing-evidence record."

    signatures: list[str] = []
    if (train_or_model or selection) and not direct:
        signatures.append("final training/model or selection outputs exist while no source file was copied outside results/**")
    if commands and not direct:
        signatures.append("preserved transcript executes a .py path that is absent from copied workspace/source directories")
    if final and not construction and not direct:
        signatures.append("final outputs exist but copied transcripts contain no code-writing payload")
    return {
        **info,
        "evidence_root": posix(run),
        "inventory": groups,
        "inventory_counts": {name: len(paths) for name, paths in groups.items()},
        "training_or_model_artifacts": train_or_model,
        "selection_artifacts": selection,
        "executed_script_paths": sorted(commands),
        "transcript_written_script_paths": sorted(writes),
        "code_construction_evidence": construction,
        "source_recovery_state": state,
        "gap_classification": gap,
        "incomplete_copy_signatures": signatures,
        "smallest_safe_recovery_rule": rule,
    }


def markdown(records: list[dict[str, Any]]) -> str:
    lines = [
        "# Top-reconstruction artifact-copy audit",
        "",
        "This is an evaluator-owned recovery audit, not a physics score. It uses only the bounded `results/paper/top-reconstruction-paper-version/` tree. A result, plot, or report is never treated as proof of uncopied source behavior.",
        "",
        "## Summary",
        "",
        f"- Runs inspected: {len(records)}.",
        f"- Direct copied final source: {sum(item['source_recovery_state'] == 'recoverable_final_code' for item in records)}.",
        f"- Source recoverable from already copied transcripts: {sum(item['source_recovery_state'] == 'recoverable_from_transcript' for item in records)}.",
        f"- Execution evidence without recoverable code: {sum(item['source_recovery_state'] == 'execution_without_recoverable_code' for item in records)}.",
        f"- Genuinely absent evidence: {sum(item['source_recovery_state'] == 'genuinely_absent_evidence' for item in records)}.",
        "",
        "## Per-run findings",
        "",
    ]
    for item in records:
        lines += [
            f"### {item['run_id']} — {item['agent']} / {item['model']}",
            "",
            f"- Retained evidence root: `{item['evidence_root']}`",
            f"- Execution status / Harbor reward: `{item['status']}` / `{item['harbor_reward']}`",
            f"- Source state: **{item['source_recovery_state']}**; classification: **{item['gap_classification']}**.",
            f"- Inventory counts: " + ", ".join(f"{name}={count}" for name, count in item["inventory_counts"].items()) + ".",
            f"- Final training/model paths: `{', '.join(item['training_or_model_artifacts']) or 'none'}`.",
            f"- Final selection paths: `{', '.join(item['selection_artifacts']) or 'none'}`.",
            f"- Transcript evidence paths: `{', '.join(item['code_construction_evidence']) or 'none'}`.",
            f"- Executed script paths seen directly in transcripts: `{', '.join(item['executed_script_paths']) or 'none'}`.",
            f"- Runtime source not copied as a workspace artifact: `{', '.join(item['transcript_written_script_paths'] or item['executed_script_paths']) or 'none'}`.",
            f"- Incomplete-copy signatures: {'; '.join(item['incomplete_copy_signatures']) or 'none observed'}.",
            f"- Smallest safe recovery rule: {item['smallest_safe_recovery_rule']}",
            "",
        ]
    lines += [
        "## Prioritized collector fixes",
        "",
        "1. **Copy the final created/modified workspace source outside `results/**`, plus a file manifest.** This is the strongest fix. It can directly support the eight currently evidence-limited question families: final features (Q4), extra features (Q5), tried ML setups (Q7), final selection algorithm (Q8), selection comparisons (Q9), mass usage/window (Q12), optimization attempts (Q13), and reproducibility (Q30). Those account for 82 not-established cells in the current 15-run pilot matrix.",
        "2. **Preserve file-writing tool inputs and terminal input bytes in one normalized telemetry record.** This unlocks adapter recovery for transcript-backed runs without requiring a solver submission format. It addresses the same eight question families where source was written through a tool call, patch, or heredoc but not copied as a file.",
        "3. **For every executed `python PATH.py`, emit a collector manifest with PATH and either its final content or an explicit unavailable marker.** This closes the execution-without-source signature and makes absent code distinguishable from an adapter limitation.",
        "4. **On failed or incomplete runs, retain the workspace snapshot and complete session stream through the final tool action.** This is most important for the three OpenHands runs that show `app.py` execution but no final results or recoverable source; it cannot manufacture missing physics evidence, but it can separate collection loss from a genuinely incomplete run.",
        "",
        "The JSON companion contains the full path inventory for each run and is the machine-readable input for future adapters.",
    ]
    return "\n".join(lines) + "\n"


def main() -> None:
    runs = sorted({path.parent for path in RUNS.rglob("result.json") if "__" in path.parent.name})
    records = [audit_run(run) for run in runs]
    (OUT / "artifact-copy-audit.json").write_text(json.dumps(records, indent=2, sort_keys=True) + "\n")
    (OUT / "artifact-copy-audit.md").write_text(markdown(records))
    print(f"wrote artifact-copy audit for {len(records)} top-reconstruction runs")


if __name__ == "__main__":
    main()
