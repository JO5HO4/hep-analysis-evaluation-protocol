# ttH diphoton paper-evidence manual review

Non-authoritative manual review under `evaluation/ttH.md`; no outcome grade is
created. Included completed logical trials (one nested `result.json` each) are
R1 Opus/UezeyUP, R2 Sonnet/mmgsDbk, R3 Claude-CBORG/MqqLxno, R4 Codex-sol/MPttiyG,
R5 Codex-terra/zWiAt8N, R6 Codex-CBORG/CwT2jxX, R7 OpenHands-sol/cMU3hZC,
R8 OpenHands-terra/E6LHpiw, R9 OpenHands-CBORG/fm8URtk, R10 Qwen-best/JmY5P4p,
R11 Qwen-medium/3FYYT6o, R12 Qwen-CBORG/2Jw5SMu, R13 Terminus-sol/u5KdDyp,
R14 Terminus-terra/sfftAQT, R15 Terminus-CBORG/st37ant. All are completed with
Harbor verifier reward 0.000000. Enclosing job summaries and links are excluded
as duplicates.

## Corrected evidence findings

The former blanket-missing review was invalid. R1, R2, R4, R5, R11, R12, R13
and R14 have readable outputs and reports; R3, R6--R10 and R15 are sparse or
partial and are evaluated criterion-by-criterion, not discarded by verifier
reward. Q28--30 and Q38 are missing for every run: the baseline README requires
a common trusted evaluator-owned table, and only a development proxy exists.

| Criterion(s) | Pass evidence | Direct fail evidence | Missing evidence trail |
|---|---|---|---|
| Q1 | none | none | all `result.json`, `run_manifest.json`, trial logs: no both trial-wall and pure-agent times |
| Q2 | R1,R2,R3,R4,R5,R13,R14 enclosing `result.json:stats.cost_usd` | none | other enclosing results give null cost |
| Q3--8 | R1/R4/R13 `report.md`, object/preselection/cutflow outputs; R2/R5/R11/R12/R14 where report establishes the named clause | R11 Q6: `report.md` photon pT>20 GeV | sparse runs: report, source, outputs and log searched |
| Q9 | none | R1,R2,R4--R6,R11--R14 `verifier/score_report.json:selection_api.errors` names incompatible BDT features | sparse R3,R7--R10,R15: no final feature evidence |
| Q10--18 | R1/R4/R13 metrics, training metadata, category yields and accepted splits; R2 where matching output establishes values | none | remaining report/source/output audits do not establish each required value |
| Q19--27 | R1/R4/R13 workspace and `fit/FIT1/{results,significance,significance_asimov}.json`; R2/R5/R11/R12/R14 only where their saved output supports the exact condition | none | sparse roots lack finite result/workspace evidence |
| Q31--33,Q36--37 | R1/R4/R13 plots/histograms, balance metadata and resolved config; only directly documented counterparts in other full roots | none | searched plots, report, metadata and source where not marked pass |
| Q34--35 | none | none | reports, metrics, optimization and source contain no finite mass-correlation result or two common-validation attempts |

Representative exact values demonstrating the corrected treatment: R4
`metrics.json:training.test_weighted_roc_auc=0.817605`; R4
`fit/FIT1/significance.json:muhat=0.993881,mu_uncertainty=0.765066,q0=2.069013`;
R13 `report.md` gives muhat=1.000±0.803,q0=1.8997,Z=1.378; R1
`report.md` records 80,585 hadronic rows, stable 60/20/20 split, explicit
no-ID/isolation policy, the five features, and accepted 5% threshold sequence.
These direct evidence sources—not Harbor reward—govern their individual rows.
