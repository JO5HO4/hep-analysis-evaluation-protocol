# Top-reconstruction workflow characterization

Protocol version: `workflow-characterization/v1`. Generated 2026-09-09. This is descriptive evidence only: no workflow score, rank, or weighted total.

## Included and excluded evidence

The included 15 logical trials are the same selected matrix and stable order as `evaluation-report.md`. Excluded supplementary paths: Claude Opus `MHMWqxn` (API error) and `zuYpFe4` (earlier completed attempt), plus OpenHands/Sol `DRCvkJN` (earlier attempt). Parent summaries, locks, wrapper/scheduler logs, and retry catalogues are not logical trials.

## Cross-run workflow summary

| Run | Harbor status / verifier reward | Commands | Failed commands | Error signatures | Recoveries | Analysis iterations | Superseded iterations | Final iteration | Reproducibility | Artifact coverage |
|---|---|---|---|---|---|---|---|---|---|---|
| Claude/cborg/tAwiCUD | completed/.916667 | not established | not established | not established | not established | 3 | 2 | Symmetric Features | not established | 12 / 12 |
| Claude/opus/p6Zi8m9 | completed/.916667 | not established | not established | not established | not established | 2 | 1 | pair_alpha | not established | 12 / 12 |
| Claude/sonnet/sw4nasz | completed/.833333 | not established | not established | not established | not established | 3 | 2 | optimal threshold .03 | not established | 12 / 12 |
| Codex/cborg/6FYNaKM | completed/.896937 | not established | not established | not established | not established | not established | not established | not established | not established | 12 / 12 |
| Codex/sol/LzgRW3i | completed/.916667 | not established | not established | not established | not established | 5 | 4 | event_selection_optimization | not established | 12 / 12 |
| Codex/terra/Nhn5tZT | completed/.916667 | not established | not established | not established | not established | 4 | 3 | score-ordered greedy | not established | 12 / 12 |
| OpenHands/sol/vQ8QaVm | completed/.000000 | not established | not established | not established | not established | not established | not established | not established | not established | 0 / 12 |
| OpenHands/terra/qvptHf2 | completed/.000000 | not established | not established | not established | not established | not established | not established | not established | not established | 0 / 12 |
| OpenHands/cborg/cXMdcuS | completed/.083333 | not established | not established | not established | not established | not established | not established | not established | not established | 12 / 12 |
| Qwen/cborg/nqv9SXY | completed/.166667 | not established | not established | not established | not established | not established | not established | not established | not established | 12 / 12 |
| Qwen/Best/7vNThUn | completed/.350805 | not established | not established | not established | not established | 1 | 0 | baseline implementation | not established | 12 / 12 |
| Qwen/Medium/WZoC7Fw | completed/.833333 | not established | not established | not established | not established | not established | not established | not established | not established | 12 / 12 |
| Terminus/sol/GewouzN | completed/.916667 | not established | not established | not established | not established | 4 | 3 | baseline_depth4 | not established | 12 / 12 |
| Terminus/terra/jSysaoA | completed/.916667 | not established | not established | not established | not established | 3 | 2 | pairmax | not established | 12 / 12 |
| Terminus/cborg/wPhYzVM | completed/.346174 | not established | not established | not established | not established | not established | not established | not established | not established | 12 / 12 |

## Per-run workflow profiles

For every run, direct sources were `R/<ID>/trial.log`, readable agent transcript/trajectory, and `R/<ID>/artifacts/root/results/`. Invocation exit states are not consistently recorded, so command count, failed-command count, signatures, and recovery count are **not established**, never zero.

| Run | Tool categories | Iteration lineage | Stage timeline | Validation checks | Reproducibility | Artifact coverage / evidence |
|---|---|---|---|---|---|---|
| Claude/cborg/tAwiCUD | shell; source editing; Python/scientific computation; file inspection; plotting | 3 / Symmetric Features | data preparation → training → validation → inference_or_selection → reporting; completed; stage durations not established | not established | not established | 12 / 12; training/selection reports and optimization record where present |
| Claude/opus/p6Zi8m9 | shell; source editing; Python/scientific computation; file inspection; plotting | 2 / pair_alpha | data preparation → training → validation → inference_or_selection → reporting; completed; stage durations not established | not established | not established | 12 / 12; training/selection reports and optimization record where present |
| Claude/sonnet/sw4nasz | shell; source editing; Python/scientific computation; file inspection; plotting | 3 / optimal threshold .03 | data preparation → training → validation → inference_or_selection → reporting; completed; stage durations not established | documented check present; detail in reports | not established | 12 / 12; training/selection reports and optimization record where present |
| Codex/cborg/6FYNaKM | shell; source editing; Python/scientific computation; file inspection | not established | data preparation → training → validation → inference_or_selection → reporting; completed; stage durations not established | not established | not established | 12 / 12; training/selection reports and optimization record where present |
| Codex/sol/LzgRW3i | shell; source editing; Python/scientific computation; file inspection; plotting | 5 / event_selection_optimization | data preparation → training → validation → inference_or_selection → reporting; completed; stage durations not established | documented check present; detail in reports | not established | 12 / 12; training/selection reports and optimization record where present |
| Codex/terra/Nhn5tZT | shell; source editing; Python/scientific computation; file inspection; plotting | 4 / score-ordered greedy | data preparation → training → validation → inference_or_selection → reporting; completed; stage durations not established | not established | not established | 12 / 12; training/selection reports and optimization record where present |
| OpenHands/sol/vQ8QaVm | shell; source editing; Python/scientific computation; file inspection | not established | setup → inference attempt; completion not established | not established | not established | 0 / 12; no task-result tree |
| OpenHands/terra/qvptHf2 | shell; source editing; Python/scientific computation; file inspection | not established | setup → inference attempt; completion not established | not established | not established | 0 / 12; no task-result tree |
| OpenHands/cborg/cXMdcuS | shell; source editing; Python/scientific computation; file inspection; plotting | not established | data preparation → training → validation → inference_or_selection → reporting; completed; stage durations not established | not established | not established | 12 / 12; training/selection reports and optimization record where present |
| Qwen/cborg/nqv9SXY | shell; source editing; Python/scientific computation; file inspection | not established | data preparation → training → validation → inference_or_selection → reporting; completed; stage durations not established | not established | not established | 12 / 12; training/selection reports and optimization record where present |
| Qwen/Best/7vNThUn | shell; source editing; Python/scientific computation; file inspection; plotting | 1 / baseline implementation | data preparation → training → validation → inference_or_selection → reporting; completed; stage durations not established | not established | not established | 12 / 12; training/selection reports and optimization record where present |
| Qwen/Medium/WZoC7Fw | shell; source editing; Python/scientific computation; file inspection; plotting | not established | data preparation → training → validation → inference_or_selection → reporting; completed; stage durations not established | not established | not established | 12 / 12; training/selection reports and optimization record where present |
| Terminus/sol/GewouzN | shell; source editing; Python/scientific computation; file inspection; plotting | 4 / baseline_depth4 | data preparation → training → validation → inference_or_selection → reporting; completed; stage durations not established | documented check present; detail in reports | not established | 12 / 12; training/selection reports and optimization record where present |
| Terminus/terra/jSysaoA | shell; source editing; Python/scientific computation; file inspection; plotting | 3 / pairmax | data preparation → training → validation → inference_or_selection → reporting; completed; stage durations not established | not established | not established | 12 / 12; training/selection reports and optimization record where present |
| Terminus/cborg/wPhYzVM | shell; source editing; Python/scientific computation; file inspection | not established | data preparation → training → validation → inference_or_selection → reporting; completed; stage durations not established | not established | not established | 12 / 12; training/selection reports and optimization record where present |

### Error signatures, recovery, and timing

No included run directly establishes a normalized error signature followed by completed same-stage recovery. Trial-level timing is available in `result.json`, but no per-stage duration is established. The excluded API-error attempt is not attributed to a selected trial.

### Iteration evidence

The non-missing lineages above are directly recorded in `optimization_summary.json:iterations` (ClC, CoS, CoT, QwB, TeS, TeT) or `optimization_report.md` (ClO, ClS). No iteration is inferred merely from multiple files.
