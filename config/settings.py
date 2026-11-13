# Synthetic Data Dictionary and Centralized Assumptions
# Mehran University of Engineering and Technology (MUET), Jamshoro
# Department of Software Engineering - Simulation & Modelling PBL

"""
CENTRALIZED ASSUMPTIONS & DATA CITATION NOTE:
Actual historical dispatch sheets and tap-in/tap-out passenger counts from the MUET Jamshoro 
Transport Section are proprietary internal administrative records not published publicly.
Therefore, in strict accordance with the Academic Honesty guidelines of this project, 
all datasets provided herein are SYNTHETIC, generated based on published academic surveys 
and realistic field operational characteristics of campus transit in Jamshoro/Hyderabad.
Any assumption can be modified directly within this configuration file or corresponding CSVs 
without altering the simulation engine logic.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Tuple
import os

# Base Directories
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
RESULTS_DIR = os.path.join(BASE_DIR, "results")
GRAPHS_DIR = os.path.join(RESULTS_DIR, "graphs")
REPORTS_DIR = os.path.join(RESULTS_DIR, "reports")

# Simulation Horizon Settings
SIMULATION_START_TIME = 7.5 * 60  # 07:30 AM in minutes from midnight (450.0 min)
SIMULATION_END_TIME = 17.0 * 60   # 05:00 PM in minutes from midnight (1020.0 min)
SIMULATION_DURATION = SIMULATION_END_TIME - SIMULATION_START_TIME  # 570 minutes (9.5 hours)

# Fleet Constraints (Fixed fleet size; NO bus purchasing permitted)
DEFAULT_FLEET_SIZE = 25
DEFAULT_BUS_CAPACITY = 55  # Standard single-deck university Point bus seating capacity

# Passenger Boarding & Alighting Dynamics (in minutes)
# Boarding takes approx 1.5 - 3.0 seconds per passenger
BOARDING_TIME_PER_PASSENGER_MIN = 1.5 / 60.0   # ~0.025 min
BOARDING_TIME_PER_PASSENGER_MAX = 3.0 / 60.0   # ~0.050 min
ALIGHTING_TIME_PER_PASSENGER = 1.0 / 60.0      # ~0.0167 min (faster egress)

# Terminals
TERMINAL_STC = "STC"
TERMINAL_MAIN_GATE = "Main Gate"
ALL_TERMINALS = [TERMINAL_STC, TERMINAL_MAIN_GATE]

# Route Definitions: (RouteID, Name, Origin Terminal, Dest, Base Travel Time in minutes, Distance in km)
ROUTE_CONFIGS = [
    {"route_id": "R1_QASIM", "name": "Qasimabad Express", "origin": TERMINAL_STC, "destination": "Qasimabad", "base_time_min": 35.0, "distance_km": 16.5},
    {"route_id": "R2_LATIF", "name": "Latifabad Route", "origin": TERMINAL_STC, "destination": "Latifabad", "base_time_min": 45.0, "distance_km": 22.0},
    {"route_id": "R3_HYD_CITY", "name": "Hyderabad City Station", "origin": TERMINAL_MAIN_GATE, "destination": "Hyder Chowk / City", "base_time_min": 40.0, "distance_km": 19.0},
    {"route_id": "R4_KOTRI", "name": "Kotri Shuttle", "origin": TERMINAL_MAIN_GATE, "destination": "Kotri / Jamshoro Phatak", "base_time_min": 25.0, "distance_km": 11.0},
    {"route_id": "R5_CAMPUS_CIRC", "name": "Internal Campus Circular", "origin": TERMINAL_STC, "destination": "Main Gate Loop", "base_time_min": 15.0, "distance_km": 6.0},
]

# Time Interval Definitions (minutes from start of simulation, t=0 is 07:30 AM)
# 07:30 - 08:00 : Early Inbound (t: 0 - 30)
# 08:00 - 09:00 : Morning Peak (t: 30 - 90)
# 09:00 - 14:00 : Mid-day Inter-peak (t: 90 - 390)
# 14:00 - 15:30 : Afternoon Peak (t: 390 - 480)
# 15:30 - 17:00 : Late Evening Off-peak (t: 480 - 570)

TIME_WINDOWS = {
    "early_morning": (0.0, 30.0),
    "morning_peak": (30.0, 90.0),
    "mid_day": (90.0, 390.0),
    "afternoon_peak": (390.0, 480.0),
    "evening_off_peak": (480.0, 570.0),
}

# Synthetic Demand Rates: Lambda (passengers arriving per minute) by terminal and time window
PASSENGER_DEMAND_PROFILES = {
    "normal": {
        TERMINAL_STC: {
            "early_morning": 3.0,     # 180 pax/hr
            "morning_peak": 12.0,     # 720 pax/hr
            "mid_day": 2.5,          # 150 pax/hr
            "afternoon_peak": 16.0,   # 960 pax/hr
            "evening_off_peak": 2.0   # 120 pax/hr
        },
        TERMINAL_MAIN_GATE: {
            "early_morning": 4.0,     # 240 pax/hr
            "morning_peak": 15.0,     # 900 pax/hr
            "mid_day": 3.0,          # 180 pax/hr
            "afternoon_peak": 14.0,   # 840 pax/hr
            "evening_off_peak": 2.0   # 120 pax/hr
        }
    },
    "high_morning": {
        TERMINAL_STC: {"early_morning": 4.0, "morning_peak": 18.0, "mid_day": 2.5, "afternoon_peak": 16.0, "evening_off_peak": 2.0},
        TERMINAL_MAIN_GATE: {"early_morning": 5.0, "morning_peak": 22.0, "mid_day": 3.0, "afternoon_peak": 14.0, "evening_off_peak": 2.0}
    },
    "high_afternoon": {
        TERMINAL_STC: {"early_morning": 3.0, "morning_peak": 12.0, "mid_day": 2.5, "afternoon_peak": 24.0, "evening_off_peak": 3.0},
        TERMINAL_MAIN_GATE: {"early_morning": 4.0, "morning_peak": 15.0, "mid_day": 3.0, "afternoon_peak": 22.0, "evening_off_peak": 3.0}
    },
    "surge_demand": {
        TERMINAL_STC: {"early_morning": 5.0, "morning_peak": 20.0, "mid_day": 5.0, "afternoon_peak": 25.0, "evening_off_peak": 4.0},
        TERMINAL_MAIN_GATE: {"early_morning": 6.0, "morning_peak": 24.0, "mid_day": 6.0, "afternoon_peak": 25.0, "evening_off_peak": 4.0}
    },
    "uneven_demand": {
        # High pressure on STC, lower on Main Gate
        TERMINAL_STC: {"early_morning": 6.0, "morning_peak": 22.0, "mid_day": 4.0, "afternoon_peak": 26.0, "evening_off_peak": 3.0},
        TERMINAL_MAIN_GATE: {"early_morning": 2.0, "morning_peak": 6.0, "mid_day": 1.5, "afternoon_peak": 7.0, "evening_off_peak": 1.0}
    }
}

# Traffic Delay Model (Lognormal distribution parameters mu, sigma representing delay in minutes)
TRAFFIC_DELAY_PARAMS = {
    "normal": {"mean_delay": 5.0, "std_delay": 2.0},
    "congested": {"mean_delay": 15.0, "std_delay": 6.0},
    "severe": {"mean_delay": 25.0, "std_delay": 10.0}
}

# Algorithm Parameters
QUEUE_THRESHOLD_TRIGGER = 45   # Passengers waiting that triggers an on-demand bus dispatch
DISPATCH_HEADWAY_MIN = 10.0    # Minimum headway between consecutive bus departures on the same route
MAX_IDLE_WAIT_TIME = 20.0      # Maximum minutes an idle bus waits before departure even if below capacity

