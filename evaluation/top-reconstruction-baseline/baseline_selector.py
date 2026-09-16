"""Deterministic mass-only baseline for top-triplet selection."""

from __future__ import annotations

import pandas as pd


TOP_MASS_GEV = 172.5
MAX_SELECTED_PER_EVENT = 2
SELECTOR_VERSION = "mass-greedy/v2-n-top-2"
REQUIRED_COLUMNS = ("event_id", "i", "j", "k", "triplet_mass")


def select_mass_greedy(candidates: pd.DataFrame) -> pd.DataFrame:
    """Select up to two mutually jet-disjoint, mass-nearest triplets/event.

    Ranking does not depend on input row order. Candidate scores and labels are
    preserved in the output but never consulted by the selector.
    """
    missing = sorted(set(REQUIRED_COLUMNS) - set(candidates.columns))
    if missing:
        raise ValueError(f"missing required columns: {', '.join(missing)}")

    ranked = candidates.copy()
    ranked["_jet_1"] = ranked[["i", "j", "k"]].min(axis=1)
    ranked["_jet_3"] = ranked[["i", "j", "k"]].max(axis=1)
    ranked["_jet_2"] = ranked[["i", "j", "k"]].sum(axis=1) - ranked["_jet_1"] - ranked["_jet_3"]
    ranked["_mass_distance"] = (ranked["triplet_mass"] - TOP_MASS_GEV).abs()
    ranked = ranked.sort_values(
        ["event_id", "_mass_distance", "_jet_1", "_jet_2", "_jet_3"],
        kind="mergesort",
    )

    selected_rows: list[pd.Series] = []
    for _, event in ranked.groupby("event_id", sort=False):
        used_jets: set[int] = set()
        selected_count = 0
        for _, candidate in event.iterrows():
            jets = {int(candidate["i"]), int(candidate["j"]), int(candidate["k"])}
            if len(jets) != 3 or used_jets.intersection(jets):
                continue
            selected_count += 1
            candidate = candidate.copy()
            candidate["selected_rank"] = selected_count
            selected_rows.append(candidate)
            used_jets.update(jets)
            if selected_count == MAX_SELECTED_PER_EVENT:
                break

    output_columns = list(candidates.columns) + ["selected_rank"]
    if not selected_rows:
        return pd.DataFrame(columns=output_columns)
    return pd.DataFrame(selected_rows)[output_columns].reset_index(drop=True)
