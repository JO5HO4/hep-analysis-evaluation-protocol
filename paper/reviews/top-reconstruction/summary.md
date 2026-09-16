# Top-reconstruction preserved-run manual review summary

Generated 2026-09-09. This covers the 15 selected agent/model cells in `results/paper/top-reconstruction-paper-version/`. It is a non-authoritative evidence review.

## Matrix selection

The paper matrix retains one clean representative per agent/model pair. For duplicated pairs, it uses the later clean retries: Claude Code / claude-opus-5 (`20260904T230352Z-top-reconstruct__p6Zi8m9`) and OpenHands / gpt-5.6-sol (`20260905T023203Z-top-reconstruct__vQ8QaVm`). Earlier attempts are preserved as supplementary review evidence and are excluded from every matrix total.

## Run registry

| Run | Per-run evaluation | Per-run workflow | P | F | M | Harbor verifier reward |
|---|---|---|---:|---:|---:|---:|
| claude-code / cborg-coder / 20260902T201601Z-top-reconstruct__tAwiCUD | [runs/claude-code/cborg-coder--tAwiCUD/evaluation-report.md](runs/claude-code/cborg-coder--tAwiCUD/evaluation-report.md) | [runs/claude-code/cborg-coder--tAwiCUD/workflow-characterization.md](runs/claude-code/cborg-coder--tAwiCUD/workflow-characterization.md) | 8 | 0 | 23 | 0.916667 |
| claude-code / claude-opus-5 / 20260904T230352Z-top-reconstruct__p6Zi8m9 | [runs/claude-code/claude-opus-5--p6Zi8m9/evaluation-report.md](runs/claude-code/claude-opus-5--p6Zi8m9/evaluation-report.md) | [runs/claude-code/claude-opus-5--p6Zi8m9/workflow-characterization.md](runs/claude-code/claude-opus-5--p6Zi8m9/workflow-characterization.md) | 19 | 2 | 10 | 0.916667 |
| claude-code / claude-sonnet-5 / 20260829T211123Z-top-reconstruct__sw4nasz | [runs/claude-code/claude-sonnet-5--sw4nasz/evaluation-report.md](runs/claude-code/claude-sonnet-5--sw4nasz/evaluation-report.md) | [runs/claude-code/claude-sonnet-5--sw4nasz/workflow-characterization.md](runs/claude-code/claude-sonnet-5--sw4nasz/workflow-characterization.md) | 19 | 2 | 10 | 0.833333 |
| codex / cborg-coder / 20260902T205040Z-top-reconstruct__6FYNaKM | [runs/codex/cborg-coder--6FYNaKM/evaluation-report.md](runs/codex/cborg-coder--6FYNaKM/evaluation-report.md) | [runs/codex/cborg-coder--6FYNaKM/workflow-characterization.md](runs/codex/cborg-coder--6FYNaKM/workflow-characterization.md) | 16 | 1 | 14 | 0.896937 |
| codex / gpt-5.6-sol / 20260831T230056Z-top-reconstruct__LzgRW3i | [runs/codex/gpt-5.6-sol--LzgRW3i/evaluation-report.md](runs/codex/gpt-5.6-sol--LzgRW3i/evaluation-report.md) | [runs/codex/gpt-5.6-sol--LzgRW3i/workflow-characterization.md](runs/codex/gpt-5.6-sol--LzgRW3i/workflow-characterization.md) | 20 | 2 | 9 | 0.916667 |
| codex / gpt-5.6-terra / 20260829T202756Z-top-reconstruct__Nhn5tZT | [runs/codex/gpt-5.6-terra--Nhn5tZT/evaluation-report.md](runs/codex/gpt-5.6-terra--Nhn5tZT/evaluation-report.md) | [runs/codex/gpt-5.6-terra--Nhn5tZT/workflow-characterization.md](runs/codex/gpt-5.6-terra--Nhn5tZT/workflow-characterization.md) | 20 | 1 | 10 | 0.916667 |
| openhands / gpt-5.6-sol / 20260905T023203Z-top-reconstruct__vQ8QaVm | [runs/openhands/gpt-5.6-sol--vQ8QaVm/evaluation-report.md](runs/openhands/gpt-5.6-sol--vQ8QaVm/evaluation-report.md) | [runs/openhands/gpt-5.6-sol--vQ8QaVm/workflow-characterization.md](runs/openhands/gpt-5.6-sol--vQ8QaVm/workflow-characterization.md) | 1 | 0 | 30 | 0.0 |
| openhands / gpt-5.6-terra / 20260829T215720Z-top-reconstruct__qvptHf2 | [runs/openhands/gpt-5.6-terra--qvptHf2/evaluation-report.md](runs/openhands/gpt-5.6-terra--qvptHf2/evaluation-report.md) | [runs/openhands/gpt-5.6-terra--qvptHf2/workflow-characterization.md](runs/openhands/gpt-5.6-terra--qvptHf2/workflow-characterization.md) | 1 | 0 | 30 | 0.0 |
| openhands / lbl/cborg-coder / 20260902T201605Z-top-reconstruct__cXMdcuS | [runs/openhands/lbl-cborg-coder--cXMdcuS/evaluation-report.md](runs/openhands/lbl-cborg-coder--cXMdcuS/evaluation-report.md) | [runs/openhands/lbl-cborg-coder--cXMdcuS/workflow-characterization.md](runs/openhands/lbl-cborg-coder--cXMdcuS/workflow-characterization.md) | 5 | 0 | 26 | 0.083333 |
| qwen-coder / cborg-coder / 20260902T205011Z-top-reconstruct__nqv9SXY | [runs/qwen-coder/cborg-coder--nqv9SXY/evaluation-report.md](runs/qwen-coder/cborg-coder--nqv9SXY/evaluation-report.md) | [runs/qwen-coder/cborg-coder--nqv9SXY/workflow-characterization.md](runs/qwen-coder/cborg-coder--nqv9SXY/workflow-characterization.md) | 4 | 0 | 27 | 0.166667 |
| qwen-coder / qwen-3 / 20260829T214149Z-top-reconstruct__WZoC7Fw | [runs/qwen-coder/qwen-3--WZoC7Fw/evaluation-report.md](runs/qwen-coder/qwen-3--WZoC7Fw/evaluation-report.md) | [runs/qwen-coder/qwen-3--WZoC7Fw/workflow-characterization.md](runs/qwen-coder/qwen-3--WZoC7Fw/workflow-characterization.md) | 7 | 0 | 24 | 0.833333 |
| qwen-coder / qwen-3 / 20260831T233834Z-top-reconstruct__7vNThUn | [runs/qwen-coder/qwen-3--7vNThUn/evaluation-report.md](runs/qwen-coder/qwen-3--7vNThUn/evaluation-report.md) | [runs/qwen-coder/qwen-3--7vNThUn/workflow-characterization.md](runs/qwen-coder/qwen-3--7vNThUn/workflow-characterization.md) | 6 | 0 | 25 | 0.350805 |
| terminus-2 / gpt-5.6-sol / 20260831T232319Z-top-reconstruct__GewouzN | [runs/terminus-2/gpt-5.6-sol--GewouzN/evaluation-report.md](runs/terminus-2/gpt-5.6-sol--GewouzN/evaluation-report.md) | [runs/terminus-2/gpt-5.6-sol--GewouzN/workflow-characterization.md](runs/terminus-2/gpt-5.6-sol--GewouzN/workflow-characterization.md) | 20 | 2 | 9 | 0.916667 |
| terminus-2 / gpt-5.6-terra / 20260829T211053Z-top-reconstruct__jSysaoA | [runs/terminus-2/gpt-5.6-terra--jSysaoA/evaluation-report.md](runs/terminus-2/gpt-5.6-terra--jSysaoA/evaluation-report.md) | [runs/terminus-2/gpt-5.6-terra--jSysaoA/workflow-characterization.md](runs/terminus-2/gpt-5.6-terra--jSysaoA/workflow-characterization.md) | 19 | 2 | 10 | 0.916667 |
| terminus-2 / lbl/cborg-coder / 20260902T201608Z-top-reconstruct__wPhYzVM | [runs/terminus-2/lbl-cborg-coder--wPhYzVM/evaluation-report.md](runs/terminus-2/lbl-cborg-coder--wPhYzVM/evaluation-report.md) | [runs/terminus-2/lbl-cborg-coder--wPhYzVM/workflow-characterization.md](runs/terminus-2/lbl-cborg-coder--wPhYzVM/workflow-characterization.md) | 5 | 0 | 26 | 0.346174 |

## Audit corrections

This audit recomputed every registry P/F/M count directly from the final per-criterion rows. It replaced prior generic partition claims with explicit event-ID intersection checks, replaced generic selection claims with recorded strategy/constraint fields or evaluator validation, and retained `missing` where a required condition could not be shown from concrete evidence. No preserved run, task, baseline, or grader was changed.

## Every rubric criterion by run

`P` = pass; `F` = fail; `M` = missing. See each linked per-run report for observed value, exact artifact location, and reasoning.

| Criterion | claude-code/cborg-coder/tAwiCUD | claude-code/claude-opus-5/p6Zi8m9 | claude-code/claude-sonnet-5/sw4nasz | codex/cborg-coder/6FYNaKM | codex/gpt-5.6-sol/LzgRW3i | codex/gpt-5.6-terra/Nhn5tZT | openhands/gpt-5.6-sol/vQ8QaVm | openhands/gpt-5.6-terra/qvptHf2 | openhands/lbl/cborg-coder/cXMdcuS | qwen-coder/cborg-coder/nqv9SXY | qwen-coder/qwen-3/WZoC7Fw | qwen-coder/qwen-3/7vNThUn | terminus-2/gpt-5.6-sol/GewouzN | terminus-2/gpt-5.6-terra/jSysaoA | terminus-2/lbl/cborg-coder/wPhYzVM |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Q1. Both trial wall-clock and pure agent execution time established | P | P | P | P | P | P | P | P | P | P | P | P | P | P | P |
| Q2. Total run cost established in USD | P | P | P | M | P | P | M | M | M | M | M | M | P | P | M |
| Q3. Classifier trained and used, with package identified | P | P | P | P | P | P | M | M | P | P | P | P | P | P | P |
| Q4. At least two final input features identified | P | P | P | P | P | P | M | M | M | M | P | M | P | P | M |
| Q5. Additional feature set tested | P | P | M | M | P | P | M | M | M | M | M | M | M | M | M |
| Q6. Nonempty event-disjoint train/validation/test partitions | P | P | P | P | P | P | M | M | P | P | M | P | P | P | P |
| Q7. At least two distinct ML setups tried | M | P | P | M | P | P | M | M | M | M | M | M | P | P | M |
| Q8. Specific final candidate-selection algorithm established | P | P | P | P | P | P | M | M | M | M | P | P | P | P | P |
| Q9. At least two selection configurations compared on common validation data | M | M | M | M | M | M | M | M | M | M | M | M | P | P | M |
| Q10. N_top <= 2 for every event | M | P | P | P | P | P | M | M | P | M | P | P | P | P | M |
| Q11. Score-mass correlation measured and reported | M | M | M | M | M | M | M | M | M | M | M | M | M | M | M |
| Q12. Final selection has no triplet-mass input or hard mass window | M | M | M | M | M | M | M | M | M | M | M | M | M | M | M |
| Q13. At least two pipeline optimization attempts | M | P | P | M | P | P | M | M | M | M | M | M | P | P | M |
| Q14. BDT-score distribution quantity, normalization, and finite values established | M | M | M | M | M | M | M | M | M | M | M | M | M | M | M |
| Q15. Reconstructed-mass comparison quantity, normalization, and finite values established | P | P | P | P | P | P | M | M | P | P | P | P | P | P | P |
| Q16. Zero overlapping selected triplets | M | P | P | P | P | P | M | M | M | M | P | M | P | P | M |
| Q17. Selected-mass bias no worse than mass-greedy/v2-n-top-2 | M | F | F | F | F | F | M | M | M | M | M | M | F | F | M |
| Q18. Selected truth-matched mass resolution strictly better than baseline | M | F | F | P | F | P | M | M | M | M | M | M | F | F | M |
| Q19. Reconstruction efficiency at least baseline | M | P | P | P | P | P | M | M | M | M | M | M | P | P | M |
| Q20. Selected-candidate purity at least baseline | M | P | P | P | P | P | M | M | M | M | M | M | P | P | M |
| Q21. Fake-to-true ratio no greater than baseline | M | P | P | P | P | P | M | M | M | M | M | M | P | P | M |
| Q22. Selected-candidate F1 at least baseline | M | P | P | P | P | P | M | M | M | M | M | M | P | P | M |
| Q23. Candidate-level selection accuracy at least baseline | M | P | P | P | P | P | M | M | M | M | M | M | P | P | M |
| Q24. Balanced selection accuracy at least baseline | M | P | P | P | P | P | M | M | M | M | M | M | P | P | M |
| Q25. Baseline Pareto improvement | M | P | P | P | P | P | M | M | M | M | M | M | P | P | M |
| Q26. Plot quantity, unit, and finite values established | M | M | M | M | M | M | M | M | M | M | M | M | M | M | M |
| Q27. Histogram statistical normalization established | M | M | M | M | M | M | M | M | M | M | M | M | M | M | M |
| Q28. Evaluated partition established for every performance plot | M | M | M | M | M | M | M | M | M | M | M | M | M | M | M |
| Q29. Candidate class-imbalance ratio and treatment established | M | M | P | M | P | M | M | M | M | M | M | M | P | M | M |
| Q30. Final reproducibility configuration complete | M | M | M | M | M | M | M | M | M | M | M | M | M | M | M |
| Q31. Held-out AUC at least frozen classifier baseline | M | M | M | M | M | M | M | M | M | M | M | M | M | M | M |
