"""
Statistical Comparison and Reporting
Aggregates replication results, computes means and standard deviations,
calculates percentage improvements over baseline (fixed_schedule),
and outputs professional markdown and CSV summary reports.
"""

import os
import pandas as pd
import numpy as np
from config.settings import RESULTS_DIR, REPORTS_DIR

def generate_comparative_analysis(results_csv_path: str = None) -> pd.DataFrame:
    if results_csv_path is None:
        results_csv_path = os.path.join(RESULTS_DIR, "simulation_results.csv")
        
    df = pd.read_csv(results_csv_path)
    
    # Group by scenario and algorithm, compute mean and std
    numeric_cols = [
        "Total Passengers Arrived",
        "Total Passengers Boarded",
        "Passengers Left Behind",
        "Avg Waiting Time (min)",
        "Median Waiting Time (min)",
        "Max Waiting Time (min)",
        "STC Avg Queue",
        "STC Max Queue",
        "Main Gate Avg Queue",
        "Main Gate Max Queue",
        "Bus Occupancy (%)",
        "Fleet Utilization (%)",
        "Completed Trips",
        "Avg Journey Time (min)"
    ]
    
    summary = df.groupby(["scenario", "algorithm"])[numeric_cols].agg(["mean", "std"]).reset_index()
    
    # Save aggregated summary CSV
    os.makedirs(REPORTS_DIR, exist_ok=True)
    summary_csv = os.path.join(REPORTS_DIR, "statistical_summary.csv")
    summary.to_csv(summary_csv, index=False)
    
    # Compute percentage improvements relative to fixed_schedule baseline
    means_df = df.groupby(["scenario", "algorithm"])[numeric_cols].mean().reset_index()
    
    comparison_rows = []
    scenarios = df["scenario"].unique()
    
    for sc in scenarios:
        sc_data = means_df[means_df["scenario"] == sc]
        baseline = sc_data[sc_data["algorithm"] == "fixed_schedule"]
        if baseline.empty:
            continue
        base_wait = baseline["Avg Waiting Time (min)"].values[0]
        base_left = baseline["Passengers Left Behind"].values[0]
        base_util = baseline["Fleet Utilization (%)"].values[0]
        base_trips = baseline["Completed Trips"].values[0]
        
        for _, row in sc_data.iterrows():
            algo = row["algorithm"]
            wait = row["Avg Waiting Time (min)"]
            left = row["Passengers Left Behind"]
            util = row["Fleet Utilization (%)"]
            trips = row["Completed Trips"]
            
            # Improvement calculation (% reduction in wait time and left behind; % change in utilization)
            wait_improv = ((base_wait - wait) / base_wait * 100.0) if base_wait > 0 else 0.0
            left_improv = ((base_left - left) / base_left * 100.0) if base_left > 0 else 0.0
            util_delta = util - base_util
            
            comparison_rows.append({
                "Scenario": sc,
                "Algorithm": algo,
                "Mean Wait Time (min)": round(wait, 2),
                "Wait Time Improvement (%)": round(wait_improv, 2),
                "Passengers Left Behind": round(left, 1),
                "Left Behind Reduction (%)": round(left_improv, 2),
                "Fleet Utilization (%)": round(util, 2),
                "Trips Completed": round(trips, 1)
            })
            
    df_comparison = pd.DataFrame(comparison_rows)
    comp_csv = os.path.join(REPORTS_DIR, "algorithm_comparison.csv")
    df_comparison.to_csv(comp_csv, index=False)
    
    # Generate Markdown Summary Table without requiring external tabulate dependency
    md_file = os.path.join(REPORTS_DIR, "comparative_evaluation.md")
    with open(md_file, "w", encoding="utf-8") as f:
        f.write("# MUET Point Scheduling Optimization: Comparative Performance Summary\n\n")
        f.write("Generated from Monte Carlo replications across 7 operational scenarios.\n\n")
        
        # Write clean markdown table
        headers = list(df_comparison.columns)
        f.write("| " + " | ".join(headers) + " |\n")
        f.write("| " + " | ".join(["---"] * len(headers)) + " |\n")
        for _, row in df_comparison.iterrows():
            row_vals = [str(row[h]) for h in headers]
            f.write("| " + " | ".join(row_vals) + " |\n")

        f.write("\n\n### Metric Interpretations:\n")
        f.write("- **Wait Time Improvement (%):** Percentage reduction in average student wait time relative to Baseline.\n")
        f.write("- **Left Behind Reduction (%):** Percentage reduction in students stranded when a bus fills up.\n")
        f.write("- **Fleet Utilization (%):** Proportion of available fleet capacity actively engaged in revenue passenger service.\n")
        
    print(f"Comparative statistical reports generated at:\n- {summary_csv}\n- {comp_csv}\n- {md_file}")
    return df_comparison

if __name__ == "__main__":
    generate_comparative_analysis()
