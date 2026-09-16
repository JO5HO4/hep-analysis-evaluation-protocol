from __future__ import annotations

import pandas as pd

from baseline import CATEGORY, evaluate


def _row(**overrides: object) -> dict[str, object]:
    row: dict[str, object] = {
        "m_gammagamma": 125.0,
        "passes_hadronic_preselection": True,
        "model_component": "signal_ttH_tH",
        "significance_model_weight_36fb": 1.0,
        "is_data": False,
        "photon_ti": True,
        "observed_data_weight": 0.0,
    }
    row.update(overrides)
    return row


def test_inclusive_baseline_ignores_bdt_and_agent_categories() -> None:
    rows = [
        _row(m_gammagamma=124.0, significance_model_weight_36fb=4.0, bdt_score=0.99, category="ttH_had_BDT1"),
        _row(m_gammagamma=126.0, significance_model_weight_36fb=2.0, bdt_score=0.01, category="unassigned"),
        _row(m_gammagamma=125.0, model_component="resonant_higgs_bkg", significance_model_weight_36fb=3.0),
        _row(m_gammagamma=110.0, model_component="not_in_model", significance_model_weight_36fb=0.0, is_data=True, observed_data_weight=1.0),
        _row(m_gammagamma=135.0, model_component="not_in_model", significance_model_weight_36fb=0.0, is_data=True, observed_data_weight=1.0),
        _row(m_gammagamma=125.0, passes_hadronic_preselection=False, significance_model_weight_36fb=100.0),
    ]
    selected, report = evaluate(pd.DataFrame(rows))
    assert set(selected["baseline_category"]) == {CATEGORY}
    assert report["sample"]["inclusive_hadronic_event_count"] == 5
    assert report["yields_36fb"]["signal_ttH_tH"] == 6.0
    assert report["fit"]["expected_Z"] > 0.0
    assert report["baseline"]["uses_bdt_score"] is False
    assert report["baseline"]["uses_agent_category"] is False


def test_requires_observed_ti_sideband_yield() -> None:
    rows = [_row()]
    try:
        evaluate(pd.DataFrame(rows))
    except ValueError as error:
        assert "sideband" in str(error)
    else:
        raise AssertionError("expected a sideband validation error")
