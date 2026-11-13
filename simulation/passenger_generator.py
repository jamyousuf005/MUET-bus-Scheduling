"""
Passenger Generator Process
Generates passenger arrivals based on a Non-Homogeneous Poisson Process (NHPP).
Arrival rates dynamically switch according to time-of-day peak/off-peak windows.
"""

import simpy
import numpy as np
from typing import Dict, List
from config.settings import TIME_WINDOWS, PASSENGER_DEMAND_PROFILES
from models.passenger import Passenger
from models.bus_stop import BusStop

class PassengerGenerator:
    def __init__(
        self,
        env: simpy.Environment,
        stops: Dict[str, BusStop],
        routes_by_terminal: Dict[str, List[str]],
        demand_profile: str = "normal",
        random_seed: int = 42
    ):
        self.env = env
        self.stops = stops
        self.routes_by_terminal = routes_by_terminal
        self.demand_profile = demand_profile
        self.rng = np.random.default_rng(random_seed)
        self.all_passengers: List[Passenger] = []
        self.passenger_counter = 0

    def get_arrival_rate(self, terminal: str, current_time: float) -> float:
        """Find lambda arrival rate (pax/min) for current time window."""
        profile = PASSENGER_DEMAND_PROFILES.get(self.demand_profile, PASSENGER_DEMAND_PROFILES["normal"])
        terminal_profile = profile.get(terminal, {})
        
        for window_name, (start_t, end_t) in TIME_WINDOWS.items():
            if start_t <= current_time < end_t:
                return terminal_profile.get(window_name, 2.0)
        return 2.0

    def run(self, terminal: str):
        """SimPy process generating passenger arrivals at a specific terminal."""
        while True:
            current_time = self.env.now
            rate_lambda = self.get_arrival_rate(terminal, current_time)
            
            # Inter-arrival time ~ Exponential(rate_lambda)
            if rate_lambda > 0:
                inter_arrival_time = self.rng.exponential(1.0 / rate_lambda)
            else:
                inter_arrival_time = 10.0

            yield self.env.timeout(inter_arrival_time)
            
            # Create passenger
            self.passenger_counter += 1
            available_routes = self.routes_by_terminal.get(terminal, ["R1_QASIM"])
            dest_route = self.rng.choice(available_routes)
            
            pax = Passenger(
                passenger_id=f"PAX_{terminal[:3].upper()}_{self.passenger_counter:05d}",
                arrival_time=self.env.now,
                terminal=terminal,
                destination_route=dest_route
            )
            self.all_passengers.append(pax)
            self.stops[terminal].add_passenger(pax, self.env.now)

