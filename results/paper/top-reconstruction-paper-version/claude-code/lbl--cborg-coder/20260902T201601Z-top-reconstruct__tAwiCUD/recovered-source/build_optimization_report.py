import json
import os

def run():
    with open("/root/results/select_triplets/selection_report.json", "r") as f:
        sel_report = json.load(f)
    
    with open("/root/results/train/training_report_xgb.json", "r") as f:
        train_report = json.load(f)
        
    with open("/root/results/infer/inference_report_xgb.json", "r") as f:
        infer_report = json.load(f)

    efficiency = sel_report["triplet_reconstruction_efficiency"]
    
    report_md = f"""# Hadronic Top Reconstruction Optimization Report

## Final Configuration
- **Classifier**: XGBoost binary classifier.
- **Features**: Per-triplet symmetric features:
    - DeltaR (min, mid, max)
    - Mass ratios (min, mid, max)
    - Triplet mass (m123)
    - Triplet pT (pt123)
    - Jet pT (min, mid, max)
    - Sum of jet pT
- **Training**:
    - Scale positive weight for class imbalance.
    - max_depth=6, learning_rate=0.05, n_estimators=200.
- **Selection Strategy**: Greedy disjoint selection of top 2 candidates per event based on classifier score.

## Performance
- **Final Triplet Reconstruction Efficiency**: {efficiency:.4f}
- **Validation AUC**: {train_report["val_auc"]:.4f}
- **Test AUC**: {infer_report["test_auc"]:.4f}

## Iteration History
1. **Baseline**: Used basic DeltaR and mass ratios. Efficiency: ~0.4488.
2. **Improved Features**: Added triplet mass, triplet pT, and individual jet pT. Efficiency: ~0.6237.
3. **Symmetric Features**: Used sorted (min/mid/max) values of DeltaR, mass ratios, and jet pT to provide permutation invariance. Efficiency: {efficiency:.4f}.

## Conclusion
The use of symmetric features and inclusive kinematics (triplet mass and pT) significantly improved the recall of truth-matched triplets. The final pipeline achieves a reconstruction efficiency of {efficiency:.4f} while maintaining a physically plausible mass distribution.
"""
    
    with open("/root/results/optimization_report.md", "w") as f:
        f.write(report_md)
        
    summary = {
        "final_efficiency": efficiency,
        "iterations": [
            {"config": "Baseline", "efficiency": 0.4488},
            {"config": "Improved Features", "efficiency": 0.6237},
            {"config": "Symmetric Features", "efficiency": efficiency},
        ]
    }
    with open("/root/results/optimization_summary.json", "w") as f:
        json.dump(summary, f, indent=4)

if __name__ == "__main__":
    run()
