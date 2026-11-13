"""
Scenario Analysis and Monte Carlo Replications
Runs multiple independent replications of all 4 scheduling strategies across scenarios:
1. Normal passenger demand
2. High morning passenger demand
3. High afternoon passenger demand
4. Unexpected traffic congestion
5. Sudden surge in passenger arrivals
6. Uneven demand between STC and Main Gate
7. Reduced bus fleet (e.g. 18 buses due to maintenance)
"""

import os
import csv
import pandas as pd
import numpy as np
from typing import List, Dict, Any
from config.settings import (
    DATA_DIR,
    RESULTS_DIR,
    DEFAULT_FLEET_SIZE,
    DEFAULT_BUS_CAPACITY,
    SIMULATION_DURATION
)
from simulation.environment import SimulationEnvironment

SCENARIOS = {
    "1_Normal_Demand": {
        "demand_profile": "normal",
        "traffic_scenario": "normal",
        "fleet_size": DEFAULT_FLEET_SIZE,
        "description": "Baseline typical operating day with standard traffic."
    },
    "2_High_Morning_Demand": {
        "demand_profile": "high_morning",
        "traffic_scenario": "normal",
        "fleet_size": DEFAULT_FLEET_SIZE,
        "description": "Heavy morning convergence of students arriving at campus."
    },
    "3_High_Afternoon_Demand": {
        "demand_profile": "high_afternoon",
        "traffic_scenario": "normal",
        "fleet_size": DEFAULT_FLEET_SIZE,
        "description": "Massive afternoon peak outbound surge after classes end."
    },
    "4_Unexpected_Traffic_Congestion": {
        "demand_profile": "normal",
        "traffic_scenario": "severe",
        "fleet_size": DEFAULT_FLEET_SIZE,
        "description": "Severe highway delays (e.g. Jamshoro toll bottleneck / roadwork)."
    },
    "5_Sudden_Surge_Demand": {
        "demand_profile": "surge_demand",
        "traffic_scenario": "congested",
        "fleet_size": DEFAULT_FLEET_SIZE,
        "description": "High simultaneous arrivals across both peaks with congestion."
    },
    "6_Uneven_Terminal_Demand": {
        "demand_profile": "uneven_demand",
        "traffic_scenario": "normal",
        "fleet_size": DEFAULT_FLEET_SIZE,
        "description": "Severe crowding at STC terminal while Main Gate experiences low volume."
    },
    "7_Reduced_Fleet_Maintenance": {
        "demand_profile": "normal",
        "traffic_scenario": "normal",
        "fleet_size": 18,
        "description": "Reduced available fleet (18 buses instead of 25) due to mechanical breakdown."
    }
}

ALGORITHMS = [
    "fixed_schedule",
    "demand_based",
    "dynamic_queue",
    "traffic_aware"
]

def load_baseline_schedules() -> List[Dict[str, Any]]:
    schedules = []
    sched_file = os.path.join(DATA_DIR, "schedules.csv")
    if os.path.exists(sched_file):
        with open(sched_file, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                schedules.append({
                    "trip_id": row["trip_id"],
                    "route_id": row["route_id"],
                    "terminal": row["terminal"],
                    "scheduled_departure_min": float(row["scheduled_departure_min"])
                })
    return schedules

def run_experiment_replications(num_replications: int = 5) -> pd.DataFrame:
    """Run replications across all scenarios and algorithms, returning consolidated results dataframe."""
    schedules_data = load_baseline_schedules()
    records = []

    print(f"Starting Scenario Analysis: {len(SCENARIOS)} scenarios x {len(ALGORITHMS)} algorithms x {num_replications} replications...")
    
    for sc_name, sc_config in SCENARIOS.items():
        print(f"\n---> Running Scenario: {sc_name}")
        for algo in ALGORITHMS:
            rep_metrics = []
            for rep in range(num_replications):
                seed = 100 * (rep + 1) + 42
                sim = SimulationEnvironment(
                    algorithm_name=algo,
                    demand_profile=sc_config["demand_profile"],
                    traffic_scenario=sc_config["traffic_scenario"],
                    fleet_size=sc_config["fleet_size"],
                    random_seed=seed,
                    schedules_data=schedules_data
                )
                m = sim.run(until=SIMULATION_DURATION)
                
                rec = {
                    "scenario": sc_name,
                    "algorithm": algo,
                    "replication": rep + 1,
                    "seed": seed,
                    **m.to_dict()
                }
                records.append(rec)

    df_results = pd.DataFrame(records)
    os.makedirs(RESULTS_DIR, exist_ok=True)
    out_csv = os.path.join(RESULTS_DIR, "simulation_results.csv")
    df_results.to_csv(out_csv, index=False)
    print(f"\nAll experiments completed! Results saved to {out_csv}")
    return df_results

if __name__ == "__main__":
    run_experiment_replications(num_replications=5)

