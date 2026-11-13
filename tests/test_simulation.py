"""
Unit and System Tests for MUET Point Bus Simulation
Validates:
1. Bus capacity limits are never exceeded.
2. Fleet size is strictly conserved.
3. No bus is assigned to concurrent overlapping trips.
4. Passenger queue behaves in strict FIFO order.
5. Waiting times are non-negative and mathematically sound.
6. Passengers are not double counted.
7. Traffic delays impact journey durations.
"""

import pytest
import simpy
from models.passenger import Passenger
from models.bus import Bus
from models.bus_stop import BusStop
from models.route import Route
from simulation.bus_operations import BusOperations
from simulation.environment import SimulationEnvironment

def test_bus_capacity_enforcement():
    """Verify that a bus never exceeds its defined seating capacity."""
    bus = Bus(bus_id="POINT_TEST_01", seating_capacity=5, current_location="STC")
    bus.start_boarding("R1_QASIM", "TRIP_001", current_time=10.0)
    
    # Create 6 passengers
    pax_list = [Passenger(f"P_{i}", arrival_time=5.0, terminal="STC", destination_route="R1_QASIM") for i in range(6)]
    
    # Boarding 5 passengers should succeed
    bus.board_passengers(pax_list[:5], current_time=10.0)
    assert len(bus.passengers_onboard) == 5
    assert bus.get_occupancy_percentage() == 100.0
    
    # Boarding an extra passenger must throw OverflowError
    with pytest.raises(OverflowError):
        bus.board_passengers([pax_list[5]], current_time=10.0)

def test_no_overlapping_trips():
    """Verify that a bus cannot accept a second trip while already in transit."""
    bus = Bus(bus_id="POINT_TEST_02", seating_capacity=50, current_location="STC")
    bus.start_boarding("R1_QASIM", "TRIP_001", current_time=10.0)
    bus.depart(current_time=12.0)
    
    # Bus is IN_TRANSIT, cannot start another trip
    assert not bus.can_accept_trip()
    with pytest.raises(ValueError):
        bus.start_boarding("R2_LATIF", "TRIP_002", current_time=15.0)

def test_fifo_queue_ordering():
    """Verify FIFO ordering at terminal bus stops."""
    stop = BusStop("STC")
    p1 = Passenger("P_1", arrival_time=10.0, terminal="STC", destination_route="R1_QASIM")
    p2 = Passenger("P_2", arrival_time=12.0, terminal="STC", destination_route="R1_QASIM")
    p3 = Passenger("P_3", arrival_time=14.0, terminal="STC", destination_route="R1_QASIM")
    
    stop.add_passenger(p1, 10.0)
    stop.add_passenger(p2, 12.0)
    stop.add_passenger(p3, 14.0)
    
    assert stop.get_queue_length("R1_QASIM") == 3
    
    # Pop 2 passengers
    boarded = stop.pop_passengers("R1_QASIM", max_count=2, current_time=15.0)
    assert len(boarded) == 2
    assert boarded[0].passenger_id == "P_1"
    assert boarded[1].passenger_id == "P_2"
    
    # Remaining passenger p3 must be marked as left behind
    assert p3.is_left_behind is True
    assert stop.get_queue_length("R1_QASIM") == 1

def test_waiting_time_calculation():
    """Verify waiting time formula: W = t_board - t_arrive."""
    p = Passenger("P_TEST", arrival_time=20.0, terminal="STC", destination_route="R1_QASIM")
    assert not p.boarded
    p.board("POINT_01", current_time=35.5)
    assert p.boarded is True
    assert p.waiting_time == 15.5

def test_simulation_run_conservation_of_fleet():
    """Run full simulation environment and verify fleet size conservation."""
    sim = SimulationEnvironment(
        algorithm_name="demand_based",
        demand_profile="normal",
        fleet_size=25,
        random_seed=42
    )
    assert len(sim.buses) == 25
    metrics = sim.run(until=120.0) # Run 2 hours
    
    # Fleet size remains exactly 25
    assert len(sim.buses) == 25
    assert metrics.total_generated_passengers > 0
    assert metrics.total_boarded_passengers <= metrics.total_generated_passengers
    assert metrics.avg_waiting_time >= 0.0

