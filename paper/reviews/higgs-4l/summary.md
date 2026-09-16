# Higgs → 4l manual-review synthesis

**Non-authoritative.** This is a transcription of the 15 completed per-run manual reviews and workflow profiles, not an outcome grade, rescore, or replacement verifier result. `P`/`F`/`M` mean the report's pass/fail/missing status. Harbor status and verifier reward are retained separately.

| Run | Harbor | Verifier | Raw /32 | Equal-category |
|---|---|---:|---:|---:|
| Claude Code / claude-opus-5 | completed | 1.000000 | 28 | .8690 |
| Claude Code / claude-sonnet-5 | completed | 1.000000 | 26 | .8010 |
| Claude Code / lbl/cborg-coder | completed | .950000 | 28 | .837 |
| Codex / gpt-5.6-sol | completed | 1.000000 | 24 | .694 |
| Codex / gpt-5.6-terra | completed | 1.000000 | 28 | .857143 |
| Codex / lbl/cborg-coder | completed | .950000 | 22 | .622449 |
| OpenHands / gpt-5.6-sol | completed | 0 | 2 | .095238 |
| OpenHands / gpt-5.6-terra | completed | 0 | 1 | .047619 |
| OpenHands / openai/lbl/cborg-coder | completed | .950000 | 23 | .658163 |
| Qwen Coder / google--qwen-3--best | completed | .587500 | 20 | .558 |
| Qwen Coder / google--qwen-3--medium | completed | .750000 | 19 | .558 |
| qwen-coder / lbl-cborg-coder | completed | .687500 | 19 | .558 |
| Terminus 2 / gpt-5.6-sol | completed | 1.000000 | 26 | .789116 |
| Terminus 2 / gpt-5.6-terra | completed | 1.000000 | 25 | .741497 |
| Terminus 2 / openai/lbl/cborg-coder | completed | .700000 | 20 | .581633 |

## Every criterion status

Rows encode Q1 through Q32, in that exact order. Thus every run and every criterion is present; P=pass, F=fail, M=missing.

| Run | Q1 | Q2 | Q3 | Q4 | Q5 | Q6 | Q7 | Q8 | Q9 | Q10 | Q11 | Q12 | Q13 | Q14 | Q15 | Q16 | Q17 | Q18 | Q19 | Q20 | Q21 | Q22 | Q23 | Q24 | Q25 | Q26 | Q27 | Q28 | Q29 | Q30 | Q31 | Q32 |
|---|---|
| Claude Code / claude-opus-5 | P | P | P | P | P | P | P | P | P | P | P | P | P | P | P | P | F | P | P | P | P | M | P | M | P | P | P | P | P | P | P | M |
| Claude Code / claude-sonnet-5 | P | P | P | P | P | P | P | P | P | P | P | P | P | M | P | P | F | P | P | P | P | M | P | M | P | P | P | P | P | P | M | M |
| Claude Code / lbl/cborg-coder | P | P | P | P | P | P | P | P | P | P | P | P | P | M | P | P | P | P | P | P | P | P | P | P | P | P | P | P | P | F | M | F |
| Codex / gpt-5.6-sol | M | P | P | P | P | P | P | P | P | P | P | P | P | P | P | M | P | P | P | P | P | P | M | M | M | M | P | P | P | P | M | M |
| Codex / gpt-5.6-terra | P | P | P | P | P | P | P | P | P | P | P | P | P | P | P | P | P | P | P | P | P | P | M | M | M | M | P | P | P | P | P | P |
| Codex / lbl/cborg-coder | P | M | P | P | P | P | P | P | P | P | P | P | P | M | P | P | P | P | P | P | P | M | M | M | M | M | P | P | P | F | M | F |
| OpenHands / gpt-5.6-sol | P | P | F | M | M | M | M | M | M | M | M | M | M | M | M | M | M | M | M | M | M | M | M | M | M | M | F | F | F | M | M | M |
| OpenHands / gpt-5.6-terra | P | M | M | M | M | M | M | M | M | M | M | M | M | M | M | M | M | M | M | M | M | M | M | M | M | M | M | M | M | M | M | M |
| OpenHands / openai/lbl/cborg-coder | P | M | P | P | P | P | P | P | P | P | P | P | P | M | P | P | P | P | P | M | P | M | P | P | P | F | P | M | P | M | M | F |
| Qwen Coder / google--qwen-3--best | P | M | P | P | P | P | P | P | P | P | P | F | M | M | P | P | P | P | P | F | P | M | M | M | M | M | P | P | P | F | M | F |
| Qwen Coder / google--qwen-3--medium | P | M | P | P | P | P | P | P | P | P | P | F | M | M | P | P | P | P | P | M | P | M | M | M | M | M | P | P | P | F | M | F |
| qwen-coder / lbl-cborg-coder | P | M | P | P | P | P | P | P | P | P | P | F | P | M | P | M | P | P | P | M | P | M | M | M | M | M | P | P | P | M | M | M |
| Terminus 2 / gpt-5.6-sol | P | P | P | P | P | P | P | P | P | P | P | P | P | M | P | P | P | P | P | P | P | M | M | M | M | M | P | P | P | P | P | M |
| Terminus 2 / gpt-5.6-terra | P | P | P | P | P | P | P | P | P | P | P | P | P | M | P | P | P | P | P | P | P | P | M | M | M | M | P | P | P | P | M | M |
| Terminus 2 / openai/lbl/cborg-coder | P | M | P | P | P | P | P | P | P | P | P | F | P | M | P | M | P | P | P | P | P | M | M | M | M | M | P | P | P | M | M | M |

Raw totals are each report's binary-reward sum; equal-category rewards are the reports' own seven-category means, neither recomputed nor authoritative.

## Workflow observations

- Profiles are descriptive only. Several preserve completed trials but no countable agent-command ledger; unavailable command, rerun, or stage-duration evidence remains `not established`, not zero.
- Most trace-rich runs record one final iteration and no clean-output reproducibility rerun. Terminus 2 / gpt-5.6-terra records two iterations, superseding an add-one p-value convention with a direct-fraction rerun.
- Terminus 2 / gpt-5.6-sol records a failed `file` command recovered by `find`; Terminus 2 / openai/lbl/cborg-coder records a recovered harness-side extended-attribute artifact-copy error. Neither observation changes Harbor completion or verifier reward.
- Artifact-coverage denominators are profile-local (2/2, 5/5, or 6/6), not a common scientific score.

This file does not inspect or reuse `superseded-invalid` or root-level review files, and modifies no preserved run, task, grader, baseline, or per-run report.
