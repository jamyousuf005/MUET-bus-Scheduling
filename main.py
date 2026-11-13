"""
Main Orchestration Script for MUET Point Bus Simulation
Usage:
  python main.py --mode full         # Runs data generation, scenario analysis, stats, and plots
  python main.py --mode simulate     # Runs single day simulation for all 4 algorithms and prints summary
  python main.py --mode test         # Runs pytest suite
"""

import argparse
import sys
import os
import pandas as pd

from data.generate_data import generate_csv_data
from analysis.scenario_analysis import run_experiment_replications
from analysis.comparison import generate_comparative_analysis
from visualization.plots import plot_all_visualizations
from simulation.environment import SimulationEnvironment
from analysis.scenario_analysis import load_baseline_schedules

def run_single_simulation():
    print("================================================================================")
    print("  MUET JAMSHORO - POINT BUS SCHEDULING DISCRETE EVENT SIMULATION (SimPy)")
    print("================================================================================")
    print("Simulating full operating day (07:30 AM - 05:00 PM = 570 simulation minutes)...")
    
    schedules = load_baseline_schedules()
    algorithms = ["fixed_schedule", "demand_based", "dynamic_queue", "traffic_aware"]
    results = []

    for algo in algorithms:
        print(f"\nExecuting Simulation: [{algo.upper()}] ...")
        sim = SimulationEnvironment(
            algorithm_name=algo,
            demand_profile="normal",
            traffic_scenario="normal",
            random_seed=42,
            schedules_data=schedules
        )
        m = sim.run(until=570.0)
        res = {"Algorithm": algo, **m.to_dict()}
        results.append(res)

    df = pd.DataFrame(results)
    print("\n--------------------------------------------------------------------------------")
    print("  COMPARATIVE PERFORMANCE RESULTS (Full Operating Day)")
    print("--------------------------------------------------------------------------------")
    # Print formatted table
    key_cols = [
        "Algorithm",
        "Total Passengers Arrived",
        "Total Passengers Boarded",
        "Passengers Left Behind",
        "Avg Waiting Time (min)",
        "Max Waiting Time (min)",
        "Bus Occupancy (%)",
        "Fleet Utilization (%)",
        "Completed Trips"
    ]
    print(df[key_cols].to_string(index=False))
    print("================================================================================\n")

def main():
    parser = argparse.ArgumentParser(description="MUET Point Bus Simulation Optimization Engine")
    parser.add_argument(
        "--mode",
        choices=["full", "simulate", "test", "data", "plots"],
        default="full",
        help="Execution mode"
    )
    parser.add_argument(
        "--replications",
        type=int,
        default=5,
        help="Number of Monte Carlo replications per scenario for full analysis"
    )
    args = parser.parse_args()

    if args.mode == "data":
        print("Generating synthetic datasets...")
        generate_csv_data()
    elif args.mode == "simulate":
        run_single_simulation()
    elif args.mode == "test":
        import pytest
        pytest.main(["tests/"])
    elif args.mode == "plots":
        print("Rendering visualizations...")
        plot_all_visualizations()
    elif args.mode == "full":
        print("[Step 1/5] Generating Synthetic Datasets...")
        generate_csv_data()
        
        print("\n[Step 2/5] Executing Monte Carlo Scenario Analysis...")
        run_experiment_replications(num_replications=args.replications)
        
        print("\n[Step 3/5] Computing Comparative Statistics & Improvements...")
        generate_comparative_analysis()
        
        print("\n[Step 4/5] Rendering 9 Publication-Grade Plots...")
        plot_all_visualizations()

        print("\n[Step 5/5] Compiling IEEE-Style Academic PDF Report...")
        from results.reports.generate_pdf import build_pdf
        build_pdf()
        
        print("\n================================================================================")
        print("  MUET SIMULATION PIPELINE COMPLETED SUCCESSFULLY!")
        print("  - Results CSV: results/simulation_results.csv")
        print("  - Statistical Summary: results/reports/statistical_summary.csv")
        print("  - Comparison Report: results/reports/comparative_evaluation.md")
        print("  - Visualization Graphs: results/graphs/*.png")
        print("================================================================================")

if __name__ == "__main__":
    main()
