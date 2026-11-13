"""
Algorithm 2: Demand-Based Scheduling
Allocates bus departures dynamically based on historical and predicted time-of-day demand.
Dispatches more frequently during peak hours (8-9 AM and 2-3:30 PM) and scales back during mid-day.
"""

import simpy
from typing import Dict, List
from config.settings import TIME_WINDOWS
from models.bus import Bus
from simulation.bus_operations import BusOperations

class DemandBasedSchedulingAlgorithm:
    def __init__(
        self,
        env: simpy.Environment,
        bus_ops: BusOperations,
        routes_by_terminal: Dict[str, List[str]]
    ):
        self.env = env
        self.bus_ops = bus_ops
        self.routes_by_terminal = routes_by_terminal
        self.trip_counter = 0

    def get_headway(self, current_time: float) -> float:
        """Dynamically compute departure headway (minutes) based on current time window."""
        # Morning peak (t: 30 - 90 min) -> frequent departures (every 8 min)
        if 30.0 <= current_time < 90.0:
            return 8.0
        # Afternoon peak (t: 390 - 480 min) -> frequent departures (every 7 min)
        elif 390.0 <= current_time < 480.0:
            return 7.0
        # Early morning (t: 0 - 30 min)
        elif current_time < 30.0:
            return 15.0
        # Mid-day (t: 90 - 390 min) -> lower frequency (every 25 min)
        else:
            return 25.0

    def run(self):
        """SimPy process managing demand-responsive dispatching."""
        while True:
            current_time = self.env.now
            headway = self.get_headway(current_time)
            
            # Dispatch buses from both terminals
            for terminal, routes in self.routes_by_terminal.items():
                for route_id in routes:
                    self.trip_counter += 1
                    trip_id = f"DEMAND_TRIP_{self.trip_counter:04d}"
                    self.bus_ops.reserve_and_dispatch_bus(route_id=route_id, terminal=terminal, trip_id=trip_id)

            yield self.env.timeout(headway)
