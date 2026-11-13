"""
Simulation Environment & Orchestrator
Initializes models, wires components, executes SimPy discrete event loop,
and returns computed performance metrics.
"""

import simpy
from typing import Dict, List, Optional
from config.settings import (
    DEFAULT_FLEET_SIZE,
    DEFAULT_BUS_CAPACITY,
    ROUTE_CONFIGS,
    SIMULATION_DURATION
)
from models.bus import Bus
from models.route import Route
from models.bus_stop import BusStop
from simulation.passenger_generator import PassengerGenerator
from simulation.bus_operations import BusOperations
from simulation.metrics import SimulationMetrics

from algorithms.fixed_schedule import FixedScheduleAlgorithm
from algorithms.demand_based import DemandBasedSchedulingAlgorithm
from algorithms.dynamic_queue import DynamicQueueSchedulingAlgorithm
from algorithms.traffic_aware import TrafficAwareSchedulingAlgorithm

class SimulationEnvironment:
    def __init__(
        self,
        algorithm_name: str = "fixed_schedule",
        demand_profile: str = "normal",
        traffic_scenario: str = "normal",
        fleet_size: int = DEFAULT_FLEET_SIZE,
        bus_capacity: int = DEFAULT_BUS_CAPACITY,
        random_seed: int = 42,
        schedules_data: Optional[List[Dict[str, any]]] = None
    ):
        self.algorithm_name = algorithm_name
        self.demand_profile = demand_profile
        self.traffic_scenario = traffic_scenario
        self.fleet_size = fleet_size
        self.bus_capacity = bus_capacity
        self.random_seed = random_seed
        self.schedules_data = schedules_data or []

        self.env = simpy.Environment()
        self._init_models()

    def _init_models(self):
        # 1. Stops
        self.stops = {
            "STC": BusStop("STC"),
            "Main Gate": BusStop("Main Gate")
        }

        # 2. Routes
        self.routes: Dict[str, Route] = {}
        self.routes_by_terminal: Dict[str, List[str]] = {"STC": [], "Main Gate": []}
        for r in ROUTE_CONFIGS:
            route = Route(
                route_id=r["route_id"],
                name=r["name"],
                origin=r["origin"],
                destination=r["destination"],
                base_time_min=r["base_time_min"],
                distance_km=r["distance_km"]
            )
            self.routes[route.route_id] = route
            self.routes_by_terminal[route.origin].append(route.route_id)

        # 3. Fleet Initialization (Strict Conservation of Fleet Size)
        self.buses: List[Bus] = []
        for i in range(1, self.fleet_size + 1):
            bus_id = f"POINT_{i:02d}"
            home_terminal = "STC" if i % 2 != 0 else "Main Gate"
            bus = Bus(
                bus_id=bus_id,
                seating_capacity=self.bus_capacity,
                current_location=home_terminal,
                status="IDLE"
            )
            self.buses.append(bus)

        # 4. Bus Operations Engine
        self.bus_ops = BusOperations(
            env=self.env,
            buses=self.buses,
            routes=self.routes,
            stops=self.stops,
            traffic_scenario=self.traffic_scenario,
            random_seed=self.random_seed
        )

        # 5. Passenger Generator
        self.passenger_gen = PassengerGenerator(
            env=self.env,
            stops=self.stops,
            routes_by_terminal=self.routes_by_terminal,
            demand_profile=self.demand_profile,
            random_seed=self.random_seed
        )

    def run(self, until: float = SIMULATION_DURATION) -> SimulationMetrics:
        # Start passenger generators for both terminals
        self.env.process(self.passenger_gen.run("STC"))
        self.env.process(self.passenger_gen.run("Main Gate"))

        # Attach chosen scheduling algorithm
        if self.algorithm_name == "fixed_schedule":
            algo = FixedScheduleAlgorithm(self.env, self.bus_ops, self.schedules_data)
            self.env.process(algo.run())
        elif self.algorithm_name == "demand_based":
            algo = DemandBasedSchedulingAlgorithm(self.env, self.bus_ops, self.routes_by_terminal)
            self.env.process(algo.run())
        elif self.algorithm_name == "dynamic_queue":
            algo = DynamicQueueSchedulingAlgorithm(self.env, self.bus_ops, self.stops, self.routes_by_terminal)
            self.env.process(algo.run())
        elif self.algorithm_name == "traffic_aware":
            algo = TrafficAwareSchedulingAlgorithm(self.env, self.bus_ops, self.stops, self.routes_by_terminal)
            self.env.process(algo.run())
        else:
            raise ValueError(f"Unknown scheduling algorithm: {self.algorithm_name}")

        # Run SimPy DES until simulation end
        self.env.run(until=until)

        # Compute and return comprehensive metrics
        return SimulationMetrics.calculate(
            all_passengers=self.passenger_gen.all_passengers,
            buses=self.buses,
            stops=self.stops,
            journey_durations=self.bus_ops.journey_durations,
            simulation_duration=until
        )

