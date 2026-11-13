"""
Bus Operations Engine
Manages bus lifecycles: dispatching, passenger boarding, transit delays, and turnaround.
Strictly enforces:
1. No bus exceeds its seating capacity.
2. A bus cannot be assigned to multiple concurrent trips.
3. Fleet size is conserved.
4. Passengers board in FIFO queue order.
"""

import simpy
import numpy as np
from typing import List, Dict, Optional
from models.bus import Bus
from models.route import Route
from models.bus_stop import BusStop
from models.passenger import Passenger
from config.settings import (
    BOARDING_TIME_PER_PASSENGER_MIN,
    BOARDING_TIME_PER_PASSENGER_MAX,
    ALIGHTING_TIME_PER_PASSENGER,
    TRAFFIC_DELAY_PARAMS
)

class BusOperations:
    def __init__(
        self,
        env: simpy.Environment,
        buses: List[Bus],
        routes: Dict[str, Route],
        stops: Dict[str, BusStop],
        traffic_scenario: str = "normal",
        random_seed: int = 42
    ):
        self.env = env
        self.buses = buses
        self.routes = routes
        self.stops = stops
        self.traffic_scenario = traffic_scenario
        self.rng = np.random.default_rng(random_seed)
        self.journey_durations: List[float] = []

    def get_idle_bus(self, terminal: str) -> Optional[Bus]:
        """Find an idle bus currently stationed at this terminal."""
        for bus in self.buses:
            if bus.status == "IDLE" and bus.current_location == terminal:
                return bus
        return None

    def reserve_and_dispatch_bus(self, route_id: str, terminal: str, trip_id: str):
        """Find an idle bus, reserve it synchronously, and launch dispatch process."""
        bus = self.get_idle_bus(terminal)
        if not bus:
            return None
        # Synchronously lock the bus
        bus.start_boarding(route_id=route_id, trip_id=trip_id, current_time=self.env.now)
        # Launch SimPy async boarding and transit lifecycle
        self.env.process(self._trip_lifecycle(bus, route_id))
        return bus

    def sample_traffic_delay(self) -> float:
        """Sample random traffic delay in minutes using lognormal distribution."""
        params = TRAFFIC_DELAY_PARAMS.get(self.traffic_scenario, TRAFFIC_DELAY_PARAMS["normal"])
        mean_delay = params["mean_delay"]
        std_delay = params["std_delay"]
        mu = np.log((mean_delay ** 2) / np.sqrt(std_delay ** 2 + mean_delay ** 2))
        sigma = np.sqrt(np.log(1.0 + (std_delay ** 2) / (mean_delay ** 2)))
        delay = self.rng.lognormal(mean=mu, sigma=sigma)
        return float(max(0.0, delay))

    def _trip_lifecycle(self, bus: Bus, route_id: str):
        """SimPy process executing passenger boarding, transit, and turnaround."""
        route = self.routes[route_id]
        terminal_stop = self.stops[bus.current_location]
        
        # Board waiting passengers up to seating capacity
        passengers_to_board = terminal_stop.pop_passengers(
            route_id=route_id,
            max_count=bus.seating_capacity,
            current_time=self.env.now
        )
        
        # Time required for boarding
        boarding_time = 0.0
        if passengers_to_board:
            boarding_rates = self.rng.uniform(
                BOARDING_TIME_PER_PASSENGER_MIN,
                BOARDING_TIME_PER_PASSENGER_MAX,
                len(passengers_to_board)
            )
            boarding_time = float(np.sum(boarding_rates))
            
        yield self.env.timeout(boarding_time)
        bus.board_passengers(passengers_to_board, self.env.now)

        # 2. Depart Terminal
        bus.depart(current_time=self.env.now)
        trip_start_time = self.env.now

        # 3. Travel to destination and back (Round Trip + Traffic Delay)
        traffic_delay = self.sample_traffic_delay()
        round_trip_time = route.get_round_trip_base_time() + traffic_delay
        
        # Add alighting time at destination
        alight_time = len(bus.passengers_onboard) * ALIGHTING_TIME_PER_PASSENGER
        total_trip_duration = round_trip_time + alight_time
        
        yield self.env.timeout(total_trip_duration)

        # 4. Return and Complete Trip
        actual_duration = self.env.now - trip_start_time
        self.journey_durations.append(actual_duration)
        
        # Bus returns to origin terminal and becomes IDLE again
        bus.complete_trip(return_terminal=route.origin, current_time=self.env.now)
