import pandas as pd
import numpy as np
import uproot
import os
import json
import matplotlib.pyplot as plt
_def calculate_mass(pt, eta, phi, ids):
    # pt, eta, phi are np.arrays
    px = np.array([pt[i] * np.cos(phi[i]) for i in ids])
    py = np.array([pt[i] * np.sin(phi[i]) for i in ids])
    pz = np.array([pt[i] * np.sinh(eta[i]) for i in ids])
    e = np.sqrt(px**2 + py**2 + pz**2)
    sum_px = np.sum(px)
    sum_py = np.sum(py)
    sum_pz = np.sum(pz)
    sum_e = np.sum(e)
    m2 = sum_e**2 - (sum_px**2 + sum_py**2 + sum_pz**2)
    return np.sqrt(max(0, m2))
sdef main():
    score_threshold = 0.7
    max_tops_per_event = 2

    infer_df = pd.read_parquet("/root/results/infer/inference_test_xgb.parquet")
    file = uproot.open("/root/data/ttbar.root")
    tree = file["output;1"]
    # We use library="pd" but we must be careful with indices
    data = tree.arrays(["Number", "genjet_pt", "genjet_eta", "genjet_phi"], library="pd")

    # Correct way to map Number (the branch) to the row index in 'data'
    event_to_idx = {num: idx for idx, num in enumerate(data["Number"])}

    candidates = infer_df[infer_df["score_xgb"] >= score_threshold].copy()
    candidates = candidates.sort_values("score_xgb", ascending=False)

    selected_triplets = []
    event_selection = []

    test_event_ids = infer_df["event_id"].unique()

    for event_id in test_event_ids:
        group = candidates[candidates["event_id"] == event_id]
        used_jets = set()
        selected_in_event = []

        for idx, row in group.iterrows():
            if len(selected_in_event) >= max_tops_per_event:
                break

            triplet_jets = {row["i"], row["j"], row["k"]}
            if triplet_jets.isdisjoint(used_jets):
                used_jets.update(triplet_jets)

                if event_id in event_to_idx:
                    tree_idx = event_to_idx[event_id]
                    # Explicitly convert to numpy arrays
                    pts = np.asarray(data["genjet_pt"].iloc[tree_idx])
                    etas = np.asarray(data["genjet_eta"].iloc[tree_idx])
                    phis = np.asarray(data["genjet_phi"].iloc[tree_idx])

                    ids = [int(row["i"]), int(row["j"]), int(row["k"])]
                    triplet_mass = calculate_mass(pts, etas, phis, ids)

                    px = np.sum([pts[i] * np.cos(phis[i]) for i in ids])
                    py = np.sum([pts[i] * np.sin(phis[i]) for i in ids])
                    pz = np.sum([pts[i] * np.sinh(etas[i]) for i in ids])
                    triplet_pt = np.sqrt(px**2 + py**2)
                    triplet_eta = np.arctanh(pz / np.sqrt(px**2 + py**2 + pz**2)) if np.sqrt(px**2 + py**2 + pz**2) > 0 else 0
                    triplet_phi = np.arctan2(py, px)

                    selected_in_event.append({
                        "event_id": event_id,
                        "selected_rank": len(selected_in_event) + 1,
                        "i": row["i"], "j": row["j"], "k": row["k"],
                        "score": row["score_xgb"],
                        "triplet_pt": triplet_pt, "triplet_eta": triplet_eta, "triplet_phi": triplet_phi,
                        "triplet_mass": triplet_mass,
                        "is_truth": row["is_truth"]
                    })

        selected_triplets.extend(selected_in_event)

        if len(selected_in_event) > 0:
            top1 = selected_in_event[0]
            event_selection.append({
                "event_id": event_id,
                "n_top_selected": len(selected_in_event),
                "top1_pt": top1["triplet_pt"],
                "top1_eta": top1["triplet_eta"],
                "top1_phi": top1["triplet_phi"],
                "top1_mass": top1["triplet_mass"]
            })
        else:
            event_selection.append({
                "event_id": event_id,
                "n_top_selected": 0,
                "top1_pt": 0, "top1_eta": 0, "top1_phi": 0, "top1_mass": 0
            })

    df_selected = pd.DataFrame(selected_triplets)
    df_event = pd.DataFrame(event_selection)

    os.makedirs("/root/results/select_triplets", exist_ok=True)
    if not df_selected.empty:
        df_selected[["event_id", "selected_rank", "i", "j", "k", "score", "triplet_pt", "triplet_eta", "triplet_phi", "triplet_mass"]].to_parquet("/root/results/select_triplets/selected_triplets.parquet")
        df_selected.to_parquet("/root/results/select_triplets/selected_triplets_with_truth.parquet")
    else:
        empty_df = pd.DataFrame(columns=["event_id", "selected_rank", "i", "j", "k", "score", "triplet_pt", "triplet_eta", "triplet_phi", "triplet_mass"])
        empty_df.to_parquet("/root/results/select_triplets/selected_triplets.parquet")

    df_event.to_parquet("/root/results/select_triplets/event_selection.parquet")

    num_selected_truth = df_selected["is_truth"].sum() if not df_selected.empty else 0
    total_truth_in_test = infer_df["is_truth"].sum()
    efficiency = float(num_selected_truth / total_truth_in_test) if total_truth_in_test > 0 else 0

    report = {
        "triplet_reconstruction_efficiency": efficiency,
        "score_threshold": score_threshold,
        "max_tops_per_event": max_tops_per_event,
        "num_selected_triplets": len(df_selected),
        "num_selected_truth": int(num_selected_truth)
    }
    with open("/root/results/select_triplets/selection_report.json", "w") as f:
        json.dump(report, f, indent=4)

    print(f"Selection completed. Efficiency: {efficiency:.4f}")
if __name__ == "__main__":
    main()
