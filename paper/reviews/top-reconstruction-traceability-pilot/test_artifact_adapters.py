from __future__ import annotations

import json

import pandas as pd

from artifact_adapters import _inference_event_ids, adapt_labeled_candidates, adapt_selected_candidates


def test_adapts_csv_selection_aliases_without_solver_contract(tmp_path) -> None:
    run = tmp_path / "run"; run.mkdir()
    pd.DataFrame([
        {"event": 4, "jet1": 7, "jet2": 2, "jet3": 5, "keep": 1},
        {"event": 4, "jet1": 1, "jet2": 3, "jet3": 6, "keep": 0},
    ]).to_csv(run / "anything.csv", index=False)
    adapted = adapt_selected_candidates(run, tmp_path / "normalized.parquet")
    assert adapted.status == "computed"
    assert adapted.source == run / "anything.csv"
    assert pd.read_parquet(adapted.canonical).to_dict("records") == [{"event_id": 4, "i": 2, "j": 5, "k": 7}]


def test_adapts_json_labeled_candidates_with_key_aliases(tmp_path) -> None:
    run = tmp_path / "run"; run.mkdir()
    (run / "arbitrary-name.json").write_text(json.dumps({"rows": [
        {"eventid": 9, "j1": 3, "j2": 1, "j3": 2, "m123": 171.2, "is_truth": True}
    ]}))
    adapted = adapt_labeled_candidates(run, tmp_path / "candidates.parquet")
    assert adapted.status == "computed"
    assert pd.read_parquet(adapted.canonical).to_dict("records") == [{"event_id": 9, "i": 1, "j": 2, "k": 3, "triplet_mass": 171.2, "is_truth": True}]


def test_rejects_selected_only_table_as_candidate_universe(tmp_path) -> None:
    run = tmp_path / "run"; run.mkdir()
    pd.DataFrame([{"event_id": 1, "i": 1, "j": 2, "k": 3, "triplet_mass": 172.5, "is_truth": True}]).to_parquet(run / "selected_triplets.parquet")
    adapted = adapt_labeled_candidates(run, tmp_path / "candidates.parquet")
    assert adapted.status == "not_established_after_inventory"


def test_prefers_final_inference_over_tuning_validation(tmp_path) -> None:
    run = tmp_path / "run"; (run / "infer").mkdir(parents=True)
    pd.DataFrame([{"event_id": 1}]).to_parquet(run / "infer" / "_tuning_val_xgb.parquet")
    pd.DataFrame([{"event_id": 7}, {"event_id": 8}]).to_parquet(run / "infer" / "inference_test_xgb.parquet")
    events, source = _inference_event_ids(run)
    assert events == {7, 8}
    assert source == run / "infer" / "inference_test_xgb.parquet"
