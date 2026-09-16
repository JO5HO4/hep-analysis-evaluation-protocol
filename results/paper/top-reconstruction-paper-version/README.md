# Top reconstruction paper-version evidence

This directory is a self-contained working copy of the selected final
top-reconstruction Harbor job bundles. Each first-level directory is the
agent/harness; its children identify the actual model used by that run.
Directory names are filesystem-safe model IDs: `/` is represented as `--`.

- Best-tier jobs came from `results/haichen`.
- Medium-tier jobs came from
  `results/dongwon/private-runs/medium-tier-remaining-15`.
- Free-tier jobs came from `results/free-tier-physics-20260902-rerun`.

Qwen Best and Medium both use `google/qwen-3`; those otherwise-colliding
directories retain `--best` and `--medium` suffixes.

Every copied child is the complete original Harbor job directory, including
its configuration, job log, result summary, and trial artifacts.  The source
directories are unchanged.

| Agent | Top-tier model / reward | Medium-tier model / reward | Free-tier reward |
| --- | --- | --- | --- |
| `codex` | `gpt-5.6-sol` / 0.916667 | `gpt-5.6-terra` / 0.916667 | 0.896937 |
| `claude-code` | `claude-opus-5` / 0.000000 | `claude-sonnet-5` / 0.833333 | 0.916667 |
| `terminus-2` | `gpt-5.6-sol` / 0.916667 | `gpt-5.6-terra` / 0.916667 | 0.346174 |
| `qwen-coder` | `google/qwen-3` / 0.350805 | `google/qwen-3` / 0.833333 | 0.166667 |
| `openhands` | `gpt-5.6-sol` / 0.000000 | `gpt-5.6-terra` / 0.000000 | 0.083333 |

The Oracle control and incomplete Claude timeout attempts from the Haichen
source are intentionally not copied: this paper-version set is model-agent
final runs only.
