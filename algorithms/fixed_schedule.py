"""
Algorithm 1: Fixed Schedule (Baseline)
Implements static timetable departure logic as currently practiced at MUET.
Buses depart at predefined clock times regardless of whether queue is long or short.
"""

import simpy
from typing import List, Dict
from models.bus import Bus
from models.route import Route
from models.bus_stop import BusStop
from simulation.bus_operations import BusOperations

class FixedScheduleAlgorithm:
    def __init__(
        self,
        env: simpy.Environment,
        bus_ops: BusOperations,
        schedules: List[Dict[str, any]]
    ):
        self.env = env
        self.bus_ops = bus_ops
        # Sorted static departure schedules
        self.schedules = sorted(schedules, key=lambda x: x["scheduled_departure_min"])

    def run(self):
        """SimPy process executing static timetable departures."""
        for sched in self.schedules:
            dept_time = sched["scheduled_departure_min"]
            route_id = sched["route_id"]
            terminal = sched["terminal"]
            trip_id = sched["trip_id"]

            # Wait until scheduled time
            if dept_time > self.env.now:
                yield self.env.timeout(dept_time - self.env.now)

            # Check if an idle bus is available at the terminal
            self.bus_ops.reserve_and_dispatch_bus(route_id=route_id, terminal=terminal, trip_id=trip_id)
