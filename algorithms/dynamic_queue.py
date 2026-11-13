"""
Algorithm 3: Dynamic Queue-Based Scheduling
Real-time closed-loop feedback strategy:
Monitors live queue length at terminals. If queue size >= QUEUE_THRESHOLD (e.g. 45 pax),
an available idle bus is immediately dispatched. Also enforces a maximum wait headway
so buses don't wait indefinitely when passenger arrivals are slow.
"""

import simpy
from typing import Dict, List
from config.settings import QUEUE_THRESHOLD_TRIGGER, MAX_IDLE_WAIT_TIME
from models.bus import Bus
from simulation.bus_operations import BusOperations
from models.bus_stop import BusStop

class DynamicQueueSchedulingAlgorithm:
    def __init__(
        self,
        env: simpy.Environment,
        bus_ops: BusOperations,
        stops: Dict[str, BusStop],
        routes_by_terminal: Dict[str, List[str]],
        queue_threshold: int = QUEUE_THRESHOLD_TRIGGER,
        check_interval: float = 2.0
    ):
        self.env = env
        self.bus_ops = bus_ops
        self.stops = stops
        self.routes_by_terminal = routes_by_terminal
        self.queue_threshold = queue_threshold
        self.check_interval = check_interval
        self.last_dispatch_time: Dict[str, float] = {}
        self.trip_counter = 0

    def run(self):
        """SimPy process polling queues and triggering responsive dispatches."""
        while True:
            current_time = self.env.now

            for terminal, routes in self.routes_by_terminal.items():
                stop = self.stops[terminal]
                for route_id in routes:
                    q_len = stop.get_queue_length(route_id)
                    time_since_last = current_time - self.last_dispatch_time.get(route_id, 0.0)

                    # Trigger condition: Queue exceeds capacity threshold OR max headway elapsed with waiting pax
                    trigger_dispatch = (q_len >= self.queue_threshold) or (q_len > 15 and time_since_last >= MAX_IDLE_WAIT_TIME)

                    if trigger_dispatch:
                        self.trip_counter += 1
                        trip_id = f"QUEUE_TRIP_{self.trip_counter:04d}"
                        dispatched_bus = self.bus_ops.reserve_and_dispatch_bus(route_id=route_id, terminal=terminal, trip_id=trip_id)
                        if dispatched_bus:
                            self.last_dispatch_time[route_id] = current_time

            yield self.env.timeout(self.check_interval)
