#!/usr/bin/env python3
"""Render descriptive figures from the selected top-reconstruction review."""
from __future__ import annotations

import json
import re
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import ListedColormap


REVIEW = Path(__file__).resolve().parents[1]
SUMMARY = REVIEW / "summary.md"
COMPARISONS = REVIEW / ".baseline-comparisons"
OUT = REVIEW.parents[2] / "paper/plots/top-reconstruction"

COLORS = {"P": "#237a57", "F": "#c2413b", "M": "#b9bec6"}

# Rubric categories are equal-weighted for the descriptive ranking below.
# Their differing criterion counts must not make the baseline-comparison block
# dominate all other aspects of the assessment.
CATEGORY_BLOCKS = [
    ("Execution and meta", range(0, 2)),
    ("BDT setup and features", range(2, 7)),
    ("Candidate selection", range(7, 10)),
    ("Physics and diagnostics", range(10, 15)),
    ("Jet disjointness", range(15, 16)),
    ("Baseline comparison", range(16, 25)),
    ("Plotting and presentation", range(25, 28)),
    ("Methodology", range(28, 30)),
    ("Frozen classifier baseline", range(30, 31)),
]

AGENT_COLORS = {
    "Claude Code": "#7b61a8",
    "Codex": "#187c73",
    "OpenHands": "#c76b2b",
    "Qwen Coder": "#b44b63",
    "Terminus 2": "#3465a4",
}


def save(fig, name):
    """Write vector and raster variants to the paper-wide plot directory."""
    OUT.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUT / f"{name}.svg", bbox_inches="tight")
    fig.savefig(OUT / f"{name}.png", bbox_inches="tight", dpi=220)


def summary_matrix():
    lines = SUMMARY.read_text().splitlines()
    header = next(line for line in lines if line.startswith("| Criterion |"))
    labels = [item.strip() for item in header.strip("|").split("|")[1:]]
    rows = []
    for line in lines:
        if not line.startswith("| Q"):
            continue
        cells = [item.strip() for item in line.strip("|").split("|")]
        if len(cells) == len(labels) + 1 and re.match(r"Q\d+\.", cells[0]):
            rows.append((cells[0].split(".", 1)[0], cells[1:]))
    return labels, rows


def registry():
    rows = []
    pattern = re.compile(r"^\| ([^|]+) \| \[[^]]+\]\([^)]*\) \| \[[^]]+\]\([^)]*\) \| (\d+) \| (\d+) \| (\d+) \|")
    for line in SUMMARY.read_text().splitlines():
        match = pattern.match(line)
        if match:
            name, passed, failed, missing = match.groups()
            rows.append((name.strip(), int(passed), int(failed), int(missing)))
    return rows


def short_labels(labels):
    return [display_label(label).replace(" / ", "\n") for label in labels]


def display_label(label):
    """Use benchmark agent/model identities, never trial suffixes, in figures."""
    agent, *model_parts, suffix = label.split("/")
    model = "/".join(model_parts)
    agent_names = {
        "claude-code": "Claude Code",
        "codex": "Codex",
        "openhands": "OpenHands",
        "qwen-coder": "Qwen Coder",
        "terminus-2": "Terminus 2",
    }
    if "cborg" in model:
        model_name = "gpt-oss-120b"
    elif agent == "qwen-coder" and suffix == "WZoC7Fw":
        model_name = "Qwen 3 Medium"
    elif agent == "qwen-coder" and suffix == "7vNThUn":
        model_name = "Qwen 3 Best"
    else:
        model_name = model
    return f"{agent_names.get(agent, agent)} / {model_name}"


def plot_status_heatmap(labels, rows):
    value = {"M": 0, "F": 1, "P": 2}
    matrix = np.array([[value[item] for item in states] for _, states in rows])
    fig, ax = plt.subplots(figsize=(13, 9))
    ax.imshow(matrix, aspect="auto", cmap=ListedColormap([COLORS["M"], COLORS["F"], COLORS["P"]]), vmin=0, vmax=2)
    ax.set_xticks(range(len(labels)), short_labels(labels), rotation=50, ha="right", fontsize=8)
    ax.set_yticks(range(len(rows)), [question for question, _ in rows], fontsize=8)
    ax.set_title("Top reconstruction: evidence status by criterion and selected run")
    ax.set_xlabel("Agent / model")
    ax.set_ylabel("Evaluation criterion")
    for y in (1, 3, 7, 10, 15, 25, 28, 30):
        ax.axhline(y - 0.5, color="white", lw=1.2)
    for label, color in [("pass", COLORS["P"]), ("fail", COLORS["F"]), ("missing", COLORS["M"])]:
        ax.scatter([], [], c=color, marker="s", s=90, label=label)
    ax.legend(ncol=3, loc="upper center", bbox_to_anchor=(0.5, -0.18), frameon=False)
    fig.tight_layout()
    save(fig, "01-rubric-status-heatmap")
    plt.close(fig)


def plot_outcome_bars(rows):
    names = [display_label("/".join((*item[0].split(" / ")[:2], item[0].split(" / ")[2][-7:]))) for item in rows]
    passed = np.array([item[1] for item in rows])
    failed = np.array([item[2] for item in rows])
    missing = np.array([item[3] for item in rows])
    y = np.arange(len(rows))
    fig, ax = plt.subplots(figsize=(9, 8))
    ax.barh(y, passed, color=COLORS["P"], label="pass")
    ax.barh(y, failed, left=passed, color=COLORS["F"], label="fail")
    ax.barh(y, missing, left=passed + failed, color=COLORS["M"], label="missing")
    ax.set_yticks(y, names, fontsize=8)
    ax.set_xlim(0, 31)
    ax.set_xlabel("Number of 31 rubric criteria")
    ax.set_title("Top reconstruction: established evidence per selected run")
    ax.legend(frameon=False, ncol=3, loc="lower right")
    ax.invert_yaxis()
    fig.tight_layout()
    save(fig, "02-rubric-outcome-bars")
    plt.close(fig)


def plot_category_average_ranking(labels, rows):
    """Rank runs by the equally weighted mean of category pass fractions."""
    states = np.array([[cell == "P" for cell in row] for _, row in rows], dtype=float)
    scores = np.array([states[list(indices)].mean(axis=0) for _, indices in CATEGORY_BLOCKS]).mean(axis=0)
    order = np.argsort(scores)[::-1]
    ranked_labels = [display_label(labels[index]) for index in order]
    ranked_scores = scores[order]
    y = np.arange(len(order))
    fig, ax = plt.subplots(figsize=(8.5, 7.5))
    bars = ax.barh(y, ranked_scores, color="#3465a4")
    ax.set_yticks(y, [label.replace(" / ", "\n") for label in ranked_labels], fontsize=8)
    ax.set_xlim(0, 1)
    ax.set_xlabel("Equal-category average of pass fractions")
    ax.set_title("Top reconstruction: descriptive agent/model ranking")
    ax.invert_yaxis()
    ranks = [1 + int(np.sum(ranked_scores > score + 1e-12)) for score in ranked_scores]
    for bar, score, rank in zip(bars, ranked_scores, ranks):
        ax.text(min(score + 0.02, 0.97), bar.get_y() + bar.get_height() / 2, f"#{rank}  {score:.2f}", va="center", fontsize=8)
    fig.text(
        0.5,
        0.01,
        "Each of 9 rubric categories has equal weight; pass = 1, fail/missing = 0. Descriptive manual-review score only.",
        ha="center",
        fontsize=8,
    )
    fig.tight_layout(rect=(0, 0.04, 1, 1))
    save(fig, "05-category-averaged-ranking")
    plt.close(fig)


def category_scores(rows):
    states = np.array([[cell == "P" for cell in row] for _, row in rows], dtype=float)
    return np.array([states[list(indices)].mean(axis=0) for _, indices in CATEGORY_BLOCKS])


def plot_category_profile(labels, rows):
    scores = category_scores(rows)
    overall = scores.mean(axis=0)
    order = np.argsort(overall)[::-1]
    fig, ax = plt.subplots(figsize=(11, 7.5))
    image = ax.imshow(scores[:, order].T, aspect="auto", cmap="YlGnBu", vmin=0, vmax=1)
    ax.set_xticks(range(len(CATEGORY_BLOCKS)), [name.replace(" and ", "\n").replace(" ", "\n") for name, _ in CATEGORY_BLOCKS], fontsize=7)
    ax.set_yticks(range(len(order)), [short_labels([labels[index]])[0] for index in order], fontsize=8)
    ax.set_title("Top reconstruction: rubric-category evidence profile")
    for row, run_index in enumerate(order):
        for column in range(len(CATEGORY_BLOCKS)):
            value = scores[column, run_index]
            ax.text(column, row, f"{value:.1f}", ha="center", va="center", fontsize=7, color="white" if value > 0.55 else "black")
    fig.colorbar(image, ax=ax, label="Pass fraction within rubric category")
    fig.tight_layout()
    save(fig, "06-category-profile-heatmap")
    plt.close(fig)


def compatible_comparisons(labels):
    by_suffix = {label.rsplit("/", 1)[-1]: label for label in labels}
    records = []
    for path in sorted(COMPARISONS.glob("*.json")):
        payload = json.loads(path.read_text())
        run_id = payload.get("run_id", path.stem)
        label = by_suffix.get(run_id[-7:])
        if label:
            records.append((label, payload))
    return records


def plot_baseline_pareto(labels):
    records = compatible_comparisons(labels)
    label_offsets = {
        "p6Zi8m9": (7, 7),
        "sw4nasz": (7, 7),
        "6FYNaKM": (7, 7),
        "LzgRW3i": (-62, -18),
        "Nhn5tZT": (7, 14),
        "GewouzN": (-45, 14),
        "jSysaoA": (-55, -18),
    }
    fig, ax = plt.subplots(figsize=(8.8, 6.5))
    for label, payload in records:
        metrics = payload["metric_comparisons"]
        base_x = metrics["reconstruction_efficiency"]["baseline"]
        base_y = metrics["fake_to_true_ratio"]["baseline"]
        agent_x = metrics["reconstruction_efficiency"]["agent"]
        agent_y = metrics["fake_to_true_ratio"]["agent"]
        agent = display_label(label).split(" / ")[0]
        color = AGENT_COLORS[agent]
        ax.annotate("", xy=(agent_x, agent_y), xytext=(base_x, base_y), arrowprops={"arrowstyle": "->", "color": color, "lw": 1.6, "alpha": 0.85})
        ax.scatter(base_x, base_y, facecolors="white", edgecolors=color, s=52, zorder=3)
        ax.scatter(agent_x, agent_y, color=color, marker="D", s=48, zorder=4)
        ax.annotate(
            display_label(label).replace(" / ", "\n"),
            (agent_x, agent_y),
            xytext=label_offsets.get(label.rsplit("/", 1)[-1], (5, 4)),
            textcoords="offset points",
            fontsize=7,
        )
    ax.set_xlabel("Reconstruction efficiency (higher is better)")
    ax.set_ylabel("Fake-to-true ratio (lower is better)")
    ax.set_title("Top reconstruction: movement from mass-greedy baseline to agent result")
    ax.text(0.98, 0.03, "Desirable direction: right and down", transform=ax.transAxes, ha="right", fontsize=8)
    ax.scatter([], [], facecolors="white", edgecolors="#333333", s=52, label="mass-greedy baseline")
    ax.scatter([], [], color="#333333", marker="D", s=48, label="agent result")
    ax.legend(frameon=False, loc="upper right", fontsize=8)
    fig.tight_layout()
    save(fig, "07-baseline-pareto")
    plt.close(fig)


def plot_score_vs_evidence(labels, rows):
    states = np.array([[cell == "P" for cell in row] for _, row in rows], dtype=float)
    established = np.array([[cell != "M" for cell in row] for _, row in rows], dtype=float).mean(axis=0)
    score = category_scores(rows).mean(axis=0)
    fig, ax = plt.subplots(figsize=(8.5, 6.5))
    seen = set()
    label_offsets = {
        "tAwiCUD": (6, 6), "p6Zi8m9": (-62, 14), "sw4nasz": (6, -18),
        "6FYNaKM": (6, 6), "LzgRW3i": (-54, 16), "Nhn5tZT": (6, 2),
        "vQ8QaVm": (6, 6), "qvptHf2": (6, -12), "cXMdcuS": (6, 8),
        "nqv9SXY": (6, 6), "WZoC7Fw": (6, 6), "7vNThUn": (6, 6),
        "GewouzN": (6, 14), "jSysaoA": (-48, -16), "wPhYzVM": (-45, -11),
    }
    for index, label in enumerate(labels):
        agent, model = display_label(label).split(" / ")
        ax.scatter(score[index], established[index], s=70, color=AGENT_COLORS[agent], label=agent if agent not in seen else None, zorder=3)
        seen.add(agent)
        ax.annotate(
            model,
            (score[index], established[index]),
            xytext=label_offsets.get(label.rsplit("/", 1)[-1], (5, 4)),
            textcoords="offset points",
            fontsize=7,
        )
    ax.set_xlim(-0.02, 1.02)
    ax.set_ylim(-0.02, 1.02)
    ax.set_xlabel("Equal-category average score")
    ax.set_ylabel("Fraction of criteria with direct evidence")
    ax.set_title("Top reconstruction: manual-review score versus evidence availability")
    ax.grid(alpha=0.25)
    ax.legend(title="Agent", frameon=False, loc="lower right", fontsize=8, title_fontsize=8)
    fig.tight_layout()
    save(fig, "08-score-vs-evidence-availability")
    plt.close(fig)


def plot_baseline_deltas():
    # Select comparison records whose trial suffix occurs in the active matrix.
    labels, _ = summary_matrix()
    suffixes = {label.rsplit("/", 1)[-1] for label in labels}
    metric_names = [
        ("truth_matched_selected_mass_bias_GeV", "mass bias", "lower"),
        ("truth_matched_selected_mass_resolution_GeV", "mass resolution", "lower"),
        ("reconstruction_efficiency", "efficiency", "higher"),
        ("purity", "purity", "higher"),
        ("fake_to_true_ratio", "fake / true", "lower"),
        ("f1", "F1", "higher"),
        ("selection_accuracy", "accuracy", "higher"),
        ("balanced_selection_accuracy", "balanced accuracy", "higher"),
    ]
    data, run_labels = [], []
    for path in sorted(COMPARISONS.glob("*.json")):
        payload = json.loads(path.read_text())
        run_id = payload.get("run_id", path.stem)
        if run_id[-7:] not in suffixes:
            continue
        deltas = []
        for key, _, direction in metric_names:
            detail = payload["metric_comparisons"][key]
            agent, baseline = detail["agent"], detail["baseline"]
            delta = (agent - baseline) / abs(baseline)
            deltas.append(100 * (delta if direction == "higher" else -delta))
        data.append(deltas)
        matching = next(label for label in labels if label.rsplit("/", 1)[-1] == run_id[-7:])
        run_labels.append(display_label(matching))
    if not data:
        return
    matrix = np.array(data)
    # Large relative changes in mass bias otherwise wash out the classification
    # and efficiency cells; retain their sign while clipping the color scale.
    scale = 100
    fig, ax = plt.subplots(figsize=(11, 4.5))
    image = ax.imshow(matrix, aspect="auto", cmap="RdYlGn", vmin=-scale, vmax=scale)
    ax.set_xticks(range(len(metric_names)), [name for _, name, _ in metric_names], rotation=35, ha="right")
    ax.set_yticks(range(len(run_labels)), [label.replace(" / ", "\n") for label in run_labels], fontsize=8)
    ax.set_title("Selected runs with compatible mass-greedy baseline comparisons")
    ax.set_xlabel("Positive = improvement relative to baseline (%)")
    ax.set_ylabel("Agent / model")
    fig.colorbar(image, ax=ax, label="Relative improvement (%) — colors clipped at ±100")
    fig.tight_layout()
    save(fig, "03-baseline-relative-improvement")
    plt.close(fig)


def plot_workflow_evidence(labels):
    workflow = (REVIEW / "workflow-characterization.md").read_text().splitlines()
    records = {}
    for line in workflow:
        if not line.startswith("|"):
            continue
        cells = [item.strip() for item in line.strip("|").split("|")]
        if len(cells) >= 6 and any(token in cells[1].lower() for token in ("shell", "python", "source editing")):
            records[cells[0].split("/")[-1]] = (cells[1].lower(), cells[3].lower())
    tool_categories = ["shell", "source editing", "python", "root/roofit", "plotting"]
    stages = ["data preparation", "training", "validation", "inference_or_selection", "reporting"]
    tool_matrix, stage_matrix = [], []
    for label in labels:
        suffix = label.rsplit("/", 1)[-1]
        tools, timeline = records.get(suffix, ("", ""))
        tool_matrix.append([int(category in tools) for category in tool_categories])
        stage_matrix.append([int(category in timeline) for category in stages])
    y = np.arange(len(labels))
    fig, (left, right) = plt.subplots(1, 2, figsize=(11, 7), sharey=True)
    cmap = ListedColormap([COLORS["M"], "#3465a4"])
    left.imshow(np.array(tool_matrix), aspect="auto", cmap=cmap, vmin=0, vmax=1)
    left.set_xticks(range(len(tool_categories)), [item.replace(" ", "\n") for item in tool_categories], fontsize=8)
    left.set_title("Documented tool categories")
    right.imshow(np.array(stage_matrix), aspect="auto", cmap=cmap, vmin=0, vmax=1)
    right.set_xticks(range(len(stages)), [item.replace("_", "\n") for item in stages], fontsize=8)
    right.set_title("Documented completed stages")
    right.set_yticks(y, short_labels(labels), fontsize=8)
    right.invert_yaxis()
    for label, color in [("directly documented", "#3465a4"), ("not established", COLORS["M"])]:
        right.scatter([], [], c=color, marker="s", s=70, label=label)
    right.legend(loc="lower center", bbox_to_anchor=(0.5, -0.22), ncol=2, frameon=False, fontsize=8)
    fig.suptitle("Top reconstruction: directly documented workflow evidence", y=0.98)
    fig.tight_layout()
    save(fig, "04-workflow-evidence")
    plt.close(fig)


def main():
    labels, rows = summary_matrix()
    plot_status_heatmap(labels, rows)
    plot_outcome_bars(registry())
    plot_category_average_ranking(labels, rows)
    plot_baseline_deltas()
    plot_workflow_evidence(labels)
    plot_category_profile(labels, rows)
    plot_baseline_pareto(labels)
    plot_score_vs_evidence(labels, rows)


if __name__ == "__main__":
    main()
