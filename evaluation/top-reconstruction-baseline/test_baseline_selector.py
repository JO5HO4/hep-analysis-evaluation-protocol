from __future__ import annotations

import pandas as pd

from baseline_selector import select_mass_greedy
from compare import fake_mass_sculpting, fake_mass_sculpting_comparison


def test_selects_by_mass_then_canonical_jet_indices() -> None:
    candidates = pd.DataFrame(
        [
            {"event_id": 1, "i": 4, "j": 5, "k": 6, "triplet_mass": 173.5},
            {"event_id": 1, "i": 1, "j": 2, "k": 3, "triplet_mass": 171.5},
            {"event_id": 1, "i": 1, "j": 7, "k": 8, "triplet_mass": 172.6},
        ]
    )
    selected = select_mass_greedy(candidates)
    assert selected[["i", "j", "k"]].values.tolist() == [[1, 7, 8], [4, 5, 6]]
    assert selected["selected_rank"].tolist() == [1, 2]


def test_never_selects_overlapping_triplets() -> None:
    candidates = pd.DataFrame(
        [
            {"event_id": 1, "i": 1, "j": 2, "k": 3, "triplet_mass": 172.5},
            {"event_id": 1, "i": 1, "j": 4, "k": 5, "triplet_mass": 172.6},
            {"event_id": 1, "i": 6, "j": 7, "k": 8, "triplet_mass": 175.0},
        ]
    )
    selected = select_mass_greedy(candidates)
    assert selected[["i", "j", "k"]].values.tolist() == [[1, 2, 3], [6, 7, 8]]


def test_limits_each_event_to_two_candidates() -> None:
    candidates = pd.DataFrame(
        [
            {"event_id": 1, "i": 1, "j": 2, "k": 3, "triplet_mass": 172.5},
            {"event_id": 1, "i": 4, "j": 5, "k": 6, "triplet_mass": 172.6},
            {"event_id": 1, "i": 7, "j": 8, "k": 9, "triplet_mass": 172.7},
        ]
    )
    selected = select_mass_greedy(candidates)
    assert len(selected) == 2
    assert selected["selected_rank"].tolist() == [1, 2]


def test_fake_mass_sculpting_prefers_unshifted_wider_selection() -> None:
    # The reference's mode is 105 GeV for the fixed 10-GeV bins.  The first
    # selection stays at that mode and retains more width than the narrow,
    # displaced alternative.
    reference = pd.Series([101, 102, 103, 104, 105, 106, 107, 108, 109, 150, 160, 170])
    unshifted_wider = pd.Series([101, 102, 103, 104, 105, 106, 107, 108, 109, 150])
    shifted_narrow = pd.Series([151, 152, 153, 154, 155, 156])
    good = fake_mass_sculpting(reference, unshifted_wider)
    bad = fake_mass_sculpting(reference, shifted_narrow)
    assert good is not None and bad is not None
    comparison = fake_mass_sculpting_comparison(
        {"fake_mass_sculpting": good}, {"fake_mass_sculpting": bad}
    )
    assert comparison is not None
    assert comparison["agent_better_than_baseline"] is True
    assert good["selected_fake_modal_bin_center_shift_GeV"] < bad["selected_fake_modal_bin_center_shift_GeV"]
    assert good["selected_fake_width_retention"] > bad["selected_fake_width_retention"]
