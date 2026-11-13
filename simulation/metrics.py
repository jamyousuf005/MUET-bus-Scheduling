"""
Simulation Metrics Collector
Captures and calculates all performance metrics:
- Average, median, max waiting time
- Average and max queue length
- Passengers transported vs left behind
- Bus occupancy %
- Fleet utilization %
- Idle times, trip counts, journey times
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any
import numpy as np
from models.passenger import Passenger
from models.bus import Bus
from models.bus_stop import BusStop

@dataclass
class SimulationMetrics:
    total_generated_passengers: int = 0
    total_boarded_passengers: int = 0
    total_left_behind_passengers: int = 0
    
    avg_waiting_time: float = 0.0
    median_waiting_time: float = 0.0
    max_waiting_time: float = 0.0
    
    avg_queue_length_stc: float = 0.0
    max_queue_length_stc: int = 0
    avg_queue_length_mg: float = 0.0
    max_queue_length_mg: int = 0
    
    avg_bus_occupancy_pct: float = 0.0
    fleet_utilization_pct: float = 0.0
    total_completed_trips: int = 0
    total_bus_idle_hours: float = 0.0
    avg_journey_time_min: float = 0.0
    
    # Raw metrics for plotting
    waiting_times: List[float] = field(default_factory=list)
    journey_times: List[float] = field(default_factory=list)
    occupancy_rates: List[float] = field(default_factory=list)
    queue_timeseries_stc: List[tuple[float, int]] = field(default_factory=list)
    queue_timeseries_mg: List[tuple[float, int]] = field(default_factory=list)

    @classmethod
    def calculate(
        cls,
        all_passengers: List[Passenger],
        buses: List[Bus],
        stops: Dict[str, BusStop],
        journey_durations: List[float],
        simulation_duration: float
    ) -> "SimulationMetrics":
        metrics = cls()
        metrics.total_generated_passengers = len(all_passengers)
        
        boarded = [p for p in all_passengers if p.boarded]
        metrics.total_boarded_passengers = len(boarded)
        metrics.total_left_behind_passengers = len([p for p in all_passengers if p.is_left_behind])
        
        if boarded:
            w_times = [p.waiting_time for p in boarded]
            metrics.waiting_times = w_times
            metrics.avg_waiting_time = float(np.mean(w_times))
            metrics.median_waiting_time = float(np.median(w_times))
            metrics.max_waiting_time = float(np.max(w_times))
        else:
            metrics.avg_waiting_time = 0.0
            metrics.median_waiting_time = 0.0
            metrics.max_waiting_time = 0.0

        # Queue metrics for STC
        stc_stop = stops.get("STC")
        if stc_stop and stc_stop.total_queue_history:
            stc_lens = [q[1] for q in stc_stop.total_queue_history]
            metrics.avg_queue_length_stc = float(np.mean(stc_lens))
            metrics.max_queue_length_stc = int(np.max(stc_lens))
            metrics.queue_timeseries_stc = stc_stop.total_queue_history

        # Queue metrics for Main Gate
        mg_stop = stops.get("Main Gate")
        if mg_stop and mg_stop.total_queue_history:
            mg_lens = [q[1] for q in mg_stop.total_queue_history]
            metrics.avg_queue_length_mg = float(np.mean(mg_lens))
            metrics.max_queue_length_mg = int(np.max(mg_lens))
            metrics.queue_timeseries_mg = mg_stop.total_queue_history

        # Fleet and Trip metrics
        total_trips = sum(b.total_trips_completed for b in buses)
        metrics.total_completed_trips = total_trips
        
        total_idle_min = sum(b.total_idle_time for b in buses)
        metrics.total_bus_idle_hours = total_idle_min / 60.0
        
        # Fleet utilization = total active time / (num_buses * total_simulation_duration)
        total_active_min = sum(b.total_active_time for b in buses)
        total_available_fleet_min = len(buses) * simulation_duration
        if total_available_fleet_min > 0:
            metrics.fleet_utilization_pct = (total_active_min / total_available_fleet_min) * 100.0

        if journey_durations:
            metrics.journey_times = journey_durations
            metrics.avg_journey_time_min = float(np.mean(journey_durations))

        # Bus Occupancy average across all completed trips
        # Approximated by total passengers boarded / (total_trips * capacity)
        total_capacity_offered = sum(b.total_trips_completed * b.seating_capacity for b in buses)
        if total_capacity_offered > 0:
            metrics.avg_bus_occupancy_pct = (metrics.total_boarded_passengers / total_capacity_offered) * 100.0
            
        return metrics

    def to_dict(self) -> Dict[str, Any]:
        return {
            "Total Passengers Arrived": self.total_generated_passengers,
            "Total Passengers Boarded": self.total_boarded_passengers,
            "Passengers Left Behind": self.total_left_behind_passengers,
            "Avg Waiting Time (min)": round(self.avg_waiting_time, 2),
            "Median Waiting Time (min)": round(self.median_waiting_time, 2),
            "Max Waiting Time (min)": round(self.max_waiting_time, 2),
            "STC Avg Queue": round(self.avg_queue_length_stc, 2),
            "STC Max Queue": self.max_queue_length_stc,
            "Main Gate Avg Queue": round(self.avg_queue_length_mg, 2),
            "Main Gate Max Queue": self.max_queue_length_mg,
            "Bus Occupancy (%)": round(self.avg_bus_occupancy_pct, 2),
            "Fleet Utilization (%)": round(self.fleet_utilization_pct, 2),
            "Completed Trips": self.total_completed_trips,
            "Total Bus Idle Hours": round(self.total_bus_idle_hours, 2),
            "Avg Journey Time (min)": round(self.avg_journey_time_min, 2)
        }

