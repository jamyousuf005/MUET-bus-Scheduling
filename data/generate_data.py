"""
Synthetic Data Generator for MUET Point Bus Scheduling.
Generates standard CSV files in data/ directory:
1. buses.csv
2. routes.csv
3. schedules.csv (Baseline static timetable)
4. passenger_demand.csv
"""

import os
import csv
from config.settings import DATA_DIR, DEFAULT_FLEET_SIZE, DEFAULT_BUS_CAPACITY, ROUTE_CONFIGS, PASSENGER_DEMAND_PROFILES

def generate_csv_data():
    os.makedirs(DATA_DIR, exist_ok=True)

    # 1. buses.csv
    buses_file = os.path.join(DATA_DIR, "buses.csv")
    with open(buses_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["bus_id", "bus_name", "seating_capacity", "home_terminal", "status"])
        for i in range(1, DEFAULT_FLEET_SIZE + 1):
            bus_id = f"POINT_{i:02d}"
            # Alternate initial terminal assignment
            home_terminal = "STC" if i % 2 != 0 else "Main Gate"
            writer.writerow([bus_id, f"MUET Point #{i:02d}", DEFAULT_BUS_CAPACITY, home_terminal, "AVAILABLE"])

    # 2. routes.csv
    routes_file = os.path.join(DATA_DIR, "routes.csv")
    with open(routes_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["route_id", "name", "origin", "destination", "base_time_min", "distance_km"])
        for r in ROUTE_CONFIGS:
            writer.writerow([r["route_id"], r["name"], r["origin"], r["destination"], r["base_time_min"], r["distance_km"]])

    # 3. schedules.csv (Baseline Static Schedule for the entire day)
    # Fixed schedule dispatches buses at rigid time intervals (every 20-30 min)
    schedules_file = os.path.join(DATA_DIR, "schedules.csv")
    with open(schedules_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["trip_id", "route_id", "terminal", "scheduled_departure_min"])
        trip_counter = 1
        # Fixed departures every 20-30 mins from t=15 to t=540
        for t in range(20, 540, 25):
            # Dispatch from STC
            writer.writerow([f"TRIP_{trip_counter:03d}", "R1_QASIM", "STC", float(t)])
            trip_counter += 1
            writer.writerow([f"TRIP_{trip_counter:03d}", "R2_LATIF", "STC", float(t + 5)])
            trip_counter += 1
            # Dispatch from Main Gate
            writer.writerow([f"TRIP_{trip_counter:03d}", "R3_HYD_CITY", "Main Gate", float(t)])
            trip_counter += 1
            writer.writerow([f"TRIP_{trip_counter:03d}", "R4_KOTRI", "Main Gate", float(t + 5)])
            trip_counter += 1

    # 4. passenger_demand.csv
    demand_file = os.path.join(DATA_DIR, "passenger_demand.csv")
    with open(demand_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["profile", "terminal", "time_window", "arrival_rate_per_min"])
        for profile_name, terminals in PASSENGER_DEMAND_PROFILES.items():
            for terminal, windows in terminals.items():
                for window_name, rate in windows.items():
                    writer.writerow([profile_name, terminal, window_name, rate])

    print("Synthetic datasets successfully created in data/ directory.")

if __name__ == "__main__":
    generate_csv_data()

