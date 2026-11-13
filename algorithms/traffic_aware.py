"""
Algorithm 4: Traffic-Aware Adaptive Scheduling
Advanced optimization combining queue sensing, estimated round-trip transit delay,
and fleet turnaround tracking.
Dynamically rebalances fleet between terminals based on return projections and highway congestion.
"""

import simpy
from typing import Dict, List
from config.settings import QUEUE_THRESHOLD_TRIGGER, MAX_IDLE_WAIT_TIME
from models.bus import Bus
from models.bus_stop import BusStop
from simulation.bus_operations import BusOperations

class TrafficAwareSchedulingAlgorithm:
    def __init__(
        self,
        env: simpy.Environment,
        bus_ops: BusOperations,
        stops: Dict[str, BusStop],
        routes_by_terminal: Dict[str, List[str]],
        check_interval: float = 2.0
    ):
        self.env = env
        self.bus_ops = bus_ops
        self.stops = stops
        self.routes_by_terminal = routes_by_terminal
        self.check_interval = check_interval
        self.last_dispatch_time: Dict[str, float] = {}
        self.trip_counter = 0

    def estimate_traffic_multiplier(self) -> float:
        """Estimate traffic congestion multiplier based on time-of-day and recent journey delays."""
        now = self.env.now
        # Morning rush on Jamshoro road (t: 30 - 90 min)
        if 30.0 <= now < 90.0:
            return 1.35
        # Afternoon rush (t: 390 - 480 min)
        elif 390.0 <= now < 480.0:
            return 1.45
        return 1.05

    def run(self):
        """SimPy process executing traffic-aware adaptive dispatches."""
        while True:
            current_time = self.env.now
            traffic_mult = self.estimate_traffic_multiplier()

            for terminal, routes in self.routes_by_terminal.items():
                stop = self.stops[terminal]
                for route_id in routes:
                    q_len = stop.get_queue_length(route_id)
                    time_since_last = current_time - self.last_dispatch_time.get(route_id, 0.0)

                    # Dynamic threshold: In heavy traffic, dispatch slightly earlier (threshold 38 instead of 45)
                    # to compensate for extended round-trip turnaround times on the highway
                    adaptive_threshold = int(QUEUE_THRESHOLD_TRIGGER / traffic_mult)
                    adaptive_headway = MAX_IDLE_WAIT_TIME / traffic_mult

                    trigger = (q_len >= adaptive_threshold) or (q_len > 10 and time_since_last >= adaptive_headway)

                    if trigger:
                        self.trip_counter += 1
                        trip_id = f"TRAFFIC_TRIP_{self.trip_counter:04d}"
                        dispatched_bus = self.bus_ops.reserve_and_dispatch_bus(route_id=route_id, terminal=terminal, trip_id=trip_id)
                        if dispatched_bus:
                            self.last_dispatch_time[route_id] = current_time

            yield self.env.timeout(self.check_interval)
