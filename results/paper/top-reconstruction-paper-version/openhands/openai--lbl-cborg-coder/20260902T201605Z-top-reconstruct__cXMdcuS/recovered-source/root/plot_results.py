import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import json

def main():
    os.makedirs("/root/results/select_triplets/plots", exist_ok=True)
    
    df_selected = pd.read_parquet("/root/results/select_triplets/selected_triplets_with_truth.parquet")
    
    # Mass distribution
    plt.figure(figsize=(8, 6))
    plt.hist(df_selected["triplet_mass"], bins=50, color="blue", alpha=0.7, label="Selected")
    plt.xlabel("Mass [GeV]")
    plt.ylabel("Counts")
    plt.title("Selected Top Candidate Mass")
    plt.legend()
    plt.grid(True)
    plt.savefig("/root/results/select_triplets/plots/mass_distribution.png")
    plt.close()
    
    # PT distribution
    plt.figure(figsize=(8, 6))
    plt.hist(df_selected["triplet_pt"], bins=50, color="green", alpha=0.7, label="Selected")
    plt.xlabel("PT [GeV]")
    plt.ylabel("Counts")
    plt.title("Selected Top Candidate PT")
    plt.legend()
    plt.grid(True)
    plt.savefig("/root/results/select_triplets/plots/pt_distribution.png")
    plt.close()

if __name__ == "__main__":
    main()
