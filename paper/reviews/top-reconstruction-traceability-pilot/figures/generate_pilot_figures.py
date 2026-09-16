#!/usr/bin/env python3
"""Render descriptive figures from the artifact-adaptive pilot records.

These figures are deliberately downstream of the review records: no solver
artifact layout is assumed, and every plotted comparison is already linked to
the corresponding evaluator record.  They are meeting aids, not outcome
grades or a replacement for the Harbor verifier reward.
"""
from __future__ import annotations

import json
from collections import Counter, defaultdict
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import ListedColormap


PILOT = Path(__file__).resolve().parents[1]
ROOT = Path(__file__).resolve().parents[4]
RUNS = PILOT / "runs"
COMPARISONS = PILOT / "baseline-comparisons"
DIAGNOSTICS = PILOT / "evaluator-diagnostics"
OUT = ROOT / "paper/plots/top-reconstruction-traceability-pilot"

STATUS_COLORS = {"missing": "#b9bec6", "fail": "#c2413b", "pass": "#237a57"}
AGENT_COLORS = {
    "claude-code": "#7b61a8",
    "codex": "#187c73",
    "openhands": "#c76b2b",
    "qwen-coder": "#b44b63",
    "terminus-2": "#3465a4",
}
CATEGORY_ORDER = [
    "Execution and Meta",
    "BDT Setup and Features",
    "Candidate Selection",
    "Physics and Diagnostics",
    "Reconstruction Performance and Jet Disjointness",
    "Baseline Comparison and Physics Quality",
    "Plotting and Presentation Quality",
    "Methodology",
    "Frozen Classifier Baseline Comparison",
]


def write_figure(fig: plt.Figure, name: str) -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUT / f"{name}.svg", bbox_inches="tight")
    fig.savefig(OUT / f"{name}.png", bbox_inches="tight", dpi=220)
    plt.close(fig)


def display_run(record: dict) -> str:
    run = record["run"]
    agent_names = {
        "claude-code": "Claude Code",
        "codex": "Codex",
        "openhands": "OpenHands",
        "qwen-coder": "Qwen Coder",
        "terminus-2": "Terminus 2",
    }
    agent = agent_names.get(run["agent"], run["agent"])
    model = run["model"].replace("google--", "").replace("openai--", "")
    return f"{agent}\n{model}"


def short_run(record: dict) -> str:
    """Harness and model only; run identifiers must not appear in figures."""
    names = {
        "claude-code": "Claude Code",
        "codex": "Codex",
        "openhands": "OpenHands",
        "qwen-coder": "Qwen Coder",
        "terminus-2": "Terminus 2",
    }
    model = record["run"]["model"].replace("google--", "").replace("openai--", "")
    return f"{names.get(record['run']['agent'], record['run']['agent'])}\n{model}"


def load_records() -> list[dict]:
    records = [json.loads(path.read_text()) for path in sorted(RUNS.glob("*.json"))]
    if not records:
        raise RuntimeError(f"no pilot records found in {RUNS}")
    return sorted(records, key=lambda record: (record["run"]["agent"], record["run"]["model"], record["run"]["id"]))


def comparison_by_run() -> dict[str, dict]:
    # Comparison schema intentionally contains only evaluator-derived values;
    # its filename is the stable retained-run identifier.
    return {path.stem: json.loads(path.read_text()) for path in COMPARISONS.glob("*.json")}


def diagnostic_by_run() -> dict[str, dict]:
    return {
        path.stem: json.loads(path.read_text())
        for path in DIAGNOSTICS.glob("*.json")
    }


def status_heatmap(records: list[dict]) -> None:
    questions = sorted({answer["id"] for record in records for answer in record["rubric_answers"]}, key=lambda value: int(value[1:]))
    value = {"missing": 0, "fail": 1, "pass": 2}
    matrix = np.array([
        [value[next(answer["status"] for answer in record["rubric_answers"] if answer["id"] == question)] for record in records]
        for question in questions
    ])
    fig, ax = plt.subplots(figsize=(13.5, 9))
    ax.imshow(matrix, aspect="auto", cmap=ListedColormap([STATUS_COLORS["missing"], STATUS_COLORS["fail"], STATUS_COLORS["pass"]]), vmin=0, vmax=2)
    ax.set_xticks(range(len(records)), [display_run(record) for record in records], rotation=50, ha="right", fontsize=7)
    ax.set_yticks(range(len(questions)), questions, fontsize=8)
    ax.set_ylabel("Evaluation-protocol question")
    ax.set_xlabel("Retained run")
    ax.set_title("Artifact-adaptive traceability review: status of all 31 questions")
    category_by_question = {answer["id"]: answer["criterion_group"] for answer in records[0]["rubric_answers"]}
    previous = category_by_question[questions[0]]
    for position, question in enumerate(questions[1:], 1):
        category = category_by_question[question]
        if category != previous:
            ax.axhline(position - 0.5, color="white", lw=1.2)
            previous = category
    for label, color in (("pass", STATUS_COLORS["pass"]), ("fail", STATUS_COLORS["fail"]), ("not established", STATUS_COLORS["missing"])):
        ax.scatter([], [], c=color, marker="s", s=70, label=label)
    ax.legend(ncol=3, loc="upper center", bbox_to_anchor=(0.5, -0.27), frameon=False)
    fig.text(0.5, 0.01, "Review rewards are non-authoritative. Missing means the bounded evidence inventory did not establish the criterion.", ha="center", fontsize=8)
    fig.tight_layout(rect=(0, 0.07, 1, 1))
    write_figure(fig, "01-rubric-status-heatmap")


def review_reward_and_coverage(records: list[dict]) -> None:
    counts = [Counter(answer["status"] for answer in record["rubric_answers"]) for record in records]
    y = np.arange(len(records))
    passed = np.array([count["pass"] for count in counts])
    failed = np.array([count["fail"] for count in counts])
    missing = np.array([count["missing"] for count in counts])
    harbor = np.array([record["run"]["harbor_verifier_reward"] for record in records])
    fig, (ax, reward_ax) = plt.subplots(1, 2, figsize=(14, 8), gridspec_kw={"width_ratios": [2.4, 1]})
    ax.barh(y, passed, color=STATUS_COLORS["pass"], label="pass")
    ax.barh(y, failed, left=passed, color=STATUS_COLORS["fail"], label="fail")
    ax.barh(y, missing, left=passed + failed, color=STATUS_COLORS["missing"], label="not established")
    ax.set_yticks(y, [display_run(record) for record in records], fontsize=7)
    ax.set_xlim(0, 31)
    ax.set_xlabel("Number of evaluation-protocol questions")
    ax.set_title("Evidence-backed review coverage")
    ax.legend(ncol=3, frameon=False, loc="lower right")
    ax.invert_yaxis()
    review = np.array([record["review_reward"]["fraction"] for record in records])
    reward_ax.scatter(harbor, y, color="#111827", marker="o", label="Harbor verifier reward", zorder=3)
    reward_ax.scatter(review, y, color="#3465a4", marker="D", label="non-authoritative review fraction", zorder=3)
    reward_ax.set_xlim(-0.03, 1.03)
    reward_ax.set_yticks(y, [])
    reward_ax.grid(axis="x", alpha=0.25)
    reward_ax.set_xlabel("Reward / fraction")
    reward_ax.set_title("Separate quantities")
    reward_ax.legend(fontsize=7, frameon=False, loc="lower left")
    reward_ax.invert_yaxis()
    fig.text(0.5, 0.01, "Harbor verifier reward and pilot review fraction are shown separately; neither is an authoritative physics outcome grade.", ha="center", fontsize=8)
    fig.tight_layout(rect=(0, 0.04, 1, 1))
    write_figure(fig, "02-review-reward-and-evidence-coverage")


def topic_scores(records: list[dict]) -> tuple[list[str], np.ndarray]:
    """Return per-topic pass fractions, with fail and missing both uncredited."""
    categories = [
        category for category in CATEGORY_ORDER
        if any(answer["criterion_group"] == category for answer in records[0]["rubric_answers"])
    ]
    scores = np.empty((len(categories), len(records)))
    for category_index, category in enumerate(categories):
        for record_index, record in enumerate(records):
            answers = [answer for answer in record["rubric_answers"] if answer["criterion_group"] == category]
            scores[category_index, record_index] = sum(answer["status"] == "pass" for answer in answers) / len(answers)
    return categories, scores


def overall_descriptive_ranking(records: list[dict]) -> None:
    categories, scores = topic_scores(records)
    overall = scores.mean(axis=0)
    order = np.argsort(overall)[::-1]
    fig, ax = plt.subplots(figsize=(8.8, 7.6))
    y = np.arange(len(order))
    bars = ax.barh(y, overall[order], color="#3465a4")
    ax.set_yticks(y, [short_run(records[index]) for index in order], fontsize=8)
    ax.set_xlim(0, 1)
    ax.set_xlabel("Equal-topic average of pass fractions")
    ax.set_title("Pilot overall ranking: non-authoritative evidence-backed review")
    ax.invert_yaxis()
    for rank, (bar, score) in enumerate(zip(bars, overall[order]), 1):
        ax.text(min(score + 0.018, 0.965), bar.get_y() + bar.get_height() / 2, f"#{rank}  {score:.2f}", va="center", fontsize=8)
    fig.text(0.5, 0.01, f"Each of {len(categories)} protocol topics has equal weight; pass = 1 and fail/not-established = 0. Not an authoritative grade.", ha="center", fontsize=8)
    fig.tight_layout(rect=(0, 0.04, 1, 1))
    write_figure(fig, "06-overall-descriptive-ranking")


def topic_breakdown(records: list[dict]) -> None:
    categories, scores = topic_scores(records)
    order = np.argsort(scores.mean(axis=0))[::-1]
    fig, ax = plt.subplots(figsize=(11.5, 8))
    image = ax.imshow(scores[:, order].T, aspect="auto", cmap="YlGnBu", vmin=0, vmax=1)
    ax.set_xticks(range(len(categories)), [category.replace(" and ", " & ").replace(" ", "\n") for category in categories], fontsize=7)
    ax.set_yticks(range(len(order)), [short_run(records[index]) for index in order], fontsize=8)
    ax.set_title("Pilot breakdown by evaluation-protocol topic")
    for row, record_index in enumerate(order):
        for column in range(len(categories)):
            value = scores[column, record_index]
            ax.text(column, row, f"{value:.2f}", ha="center", va="center", fontsize=7, color="white" if value > 0.55 else "black")
    fig.colorbar(image, ax=ax, label="Pass fraction within topic")
    fig.text(0.5, 0.01, "Fail and not-established results both contribute zero; color values are descriptive non-authoritative review coverage.", ha="center", fontsize=8)
    fig.tight_layout(rect=(0, 0.04, 1, 1))
    write_figure(fig, "07-topic-breakdown-heatmap")


def baseline_pareto(records: list[dict], comparisons: dict[str, dict]) -> None:
    available = [(record, comparisons[record["run"]["id"]]) for record in records if record["run"]["id"] in comparisons]
    fig, ax = plt.subplots(figsize=(9.5, 6.8))
    for record, comparison in available:
        metrics = comparison["metric_comparisons"]
        base_x = metrics["reconstruction_efficiency"]["baseline"]
        base_y = metrics["fake_to_true_ratio"]["baseline"]
        agent_x = metrics["reconstruction_efficiency"]["agent"]
        agent_y = metrics["fake_to_true_ratio"]["agent"]
        agent_key = record["run"]["agent"]
        color = AGENT_COLORS.get(agent_key, "#374151")
        ax.annotate("", xy=(agent_x, agent_y), xytext=(base_x, base_y), arrowprops={"arrowstyle": "->", "color": color, "lw": 1.2, "alpha": 0.78})
        ax.scatter(base_x, base_y, facecolors="white", edgecolors=color, s=44, zorder=2)
        ax.scatter(agent_x, agent_y, color=color, marker="D", s=38, zorder=3)
        ax.annotate(short_run(record), (agent_x, agent_y), xytext=(4, 3), textcoords="offset points", fontsize=6)
    ax.set_xlabel("Reconstruction efficiency (higher is better)")
    ax.set_ylabel("Fake-to-true ratio (lower is better)")
    ax.set_title("Evaluator-side comparison: movement from mass-greedy/v2-n-top-2")
    ax.text(0.98, 0.03, "Desirable direction: right and down", transform=ax.transAxes, ha="right", fontsize=8)
    ax.scatter([], [], facecolors="white", edgecolors="#374151", s=44, label="mass-greedy baseline")
    ax.scatter([], [], color="#374151", marker="D", s=38, label="agent selection")
    ax.legend(frameon=False, loc="upper left", fontsize=8)
    fig.text(0.5, 0.01, f"{len(available)} of {len(records)} retained runs had selections recoverable for the same-sample evaluator comparison.", ha="center", fontsize=8)
    fig.tight_layout(rect=(0, 0.035, 1, 1))
    write_figure(fig, "03-baseline-efficiency-fake-ratio")


def fake_mass_sculpting(records: list[dict], comparisons: dict[str, dict]) -> None:
    available = [(record, comparisons[record["run"]["id"]]) for record in records if record["run"]["id"] in comparisons]
    fig, ax = plt.subplots(figsize=(9.5, 6.8))
    for record, comparison in available:
        values = comparison["fake_mass_sculpting_comparison"]
        baseline = values["baseline"]
        agent = values["agent"]
        base_x = baseline["selected_fake_modal_bin_center_shift_GeV"]
        base_y = baseline["selected_fake_width_retention"]
        agent_x = agent["selected_fake_modal_bin_center_shift_GeV"]
        agent_y = agent["selected_fake_width_retention"]
        color = AGENT_COLORS.get(record["run"]["agent"], "#374151")
        ax.annotate("", xy=(agent_x, agent_y), xytext=(base_x, base_y), arrowprops={"arrowstyle": "->", "color": color, "lw": 1.2, "alpha": 0.78})
        ax.scatter(base_x, base_y, facecolors="white", edgecolors=color, s=44, zorder=2)
        ax.scatter(agent_x, agent_y, color=color, marker="D", s=38, zorder=3)
        ax.annotate(short_run(record), (agent_x, agent_y), xytext=(4, 3), textcoords="offset points", fontsize=6)
    ax.set_xlabel("Selected-fake modal-bin-center shift from unselected fakes [GeV] (lower is better)")
    ax.set_ylabel("Selected-fake width retention (higher is better)")
    ax.set_title("Fake-mass sculpting diagnostic on the reconstructed comparison sample")
    ax.text(0.98, 0.03, "Paired improvement: left and up", transform=ax.transAxes, ha="right", fontsize=8)
    ax.scatter([], [], facecolors="white", edgecolors="#374151", s=44, label="mass-greedy baseline")
    ax.scatter([], [], color="#374151", marker="D", s=38, label="agent selection")
    ax.legend(frameon=False, loc="upper right", fontsize=8)
    fig.text(0.5, 0.01, "Fixed unweighted 0–400 GeV, 40-bin histogram; descriptive diagnostic with no threshold or authoritative score.", ha="center", fontsize=8)
    fig.tight_layout(rect=(0, 0.035, 1, 1))
    write_figure(fig, "04-fake-mass-sculpting")


def evaluator_diagnostic_coverage(records: list[dict], diagnostics: dict[str, dict]) -> None:
    counts: dict[str, Counter] = defaultdict(Counter)
    for record in records:
        for answer in record["rubric_answers"]:
            counts[answer["criterion_group"]][answer["status"]] += 1
    categories = [category for category in CATEGORY_ORDER if category in counts]
    y = np.arange(len(categories))
    passed = np.array([counts[category]["pass"] for category in categories])
    failed = np.array([counts[category]["fail"] for category in categories])
    missing = np.array([counts[category]["missing"] for category in categories])
    fig, ax = plt.subplots(figsize=(10.5, 6.5))
    ax.barh(y, passed, color=STATUS_COLORS["pass"], label="pass")
    ax.barh(y, failed, left=passed, color=STATUS_COLORS["fail"], label="fail")
    ax.barh(y, missing, left=passed + failed, color=STATUS_COLORS["missing"], label="not established")
    ax.set_yticks(y, [category.replace(" and ", " & ") for category in categories], fontsize=8)
    ax.set_xlim(0, max(passed + failed + missing) + 2)
    ax.set_xlabel("Question results across retained runs")
    ax.set_title("Which evaluation-protocol areas are established by the initial records")
    ax.legend(frameon=False, ncol=3, loc="lower right")
    ax.invert_yaxis()
    usable = sum("unavailable" not in payload.get("frozen_classifier_comparison", {}) for payload in diagnostics.values())
    fig.text(0.5, 0.01, f"Evaluator diagnostics found for {len(diagnostics)} runs; frozen classifier comparison usable for {usable} runs.", ha="center", fontsize=8)
    fig.tight_layout(rect=(0, 0.04, 1, 1))
    write_figure(fig, "05-protocol-area-coverage")


def write_readme() -> None:
    (OUT / "README.md").write_text(
        """# Top-reconstruction traceability-pilot figures

These descriptive figures are generated from the machine-readable pilot records
under `paper/reviews/top-reconstruction-traceability-pilot/`. They do not
replace the Harbor verifier reward and do not constitute an authoritative
physics outcome grade.

- `01-rubric-status-heatmap`: all 31 evaluation-protocol questions by retained run.
- `02-review-reward-and-evidence-coverage`: evidence status plus the separately reported Harbor verifier reward and non-authoritative review fraction.
- `03-baseline-efficiency-fake-ratio`: evaluator-side selection comparison to `mass-greedy/v2-n-top-2`.
- `04-fake-mass-sculpting`: evaluator-side fake-mass diagnostic using a fixed 0–400 GeV, 40-bin histogram.
- `05-protocol-area-coverage`: established, failed, and not-established question results grouped by protocol area.
- `06-overall-descriptive-ranking`: equal-topic pass-fraction ranking, explicitly non-authoritative.
- `07-topic-breakdown-heatmap`: per-run pass fraction within each evaluation-protocol topic.

Regenerate with:

```bash
python paper/reviews/top-reconstruction-traceability-pilot/figures/generate_pilot_figures.py
```
"""
    )


def main() -> None:
    records = load_records()
    comparisons = comparison_by_run()
    diagnostics = diagnostic_by_run()
    status_heatmap(records)
    review_reward_and_coverage(records)
    baseline_pareto(records, comparisons)
    fake_mass_sculpting(records, comparisons)
    evaluator_diagnostic_coverage(records, diagnostics)
    overall_descriptive_ranking(records)
    topic_breakdown(records)
    write_readme()
    print(f"wrote 7 pilot figures for {len(records)} runs to {OUT}")


if __name__ == "__main__":
    main()
