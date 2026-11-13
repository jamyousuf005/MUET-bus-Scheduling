"""
Bus Domain Model
Represents individual Point buses, tracking location, status, trips, active/idle time, and passenger boarding.
"""

from dataclasses import dataclass, field
from typing import List, Optional
from models.passenger import Passenger

@dataclass
class Bus:
    bus_id: str
    seating_capacity: int
    current_location: str                  # STC, Main Gate, or 'IN_TRANSIT'
    status: str = "IDLE"                   # 'IDLE', 'BOARDING', 'IN_TRANSIT', 'MAINTENANCE'
    assigned_route: Optional[str] = None
    current_trip_id: Optional[str] = None
    passengers_onboard: List[Passenger] = field(default_factory=list)
    
    # Operational metrics tracking
    total_trips_completed: int = 0
    total_passengers_transported: int = 0
    total_active_time: float = 0.0         # Minutes spent boarding or in transit
    total_idle_time: float = 0.0           # Minutes spent waiting at terminal
    last_status_change_time: float = 0.0

    def get_occupancy_percentage(self) -> float:
        if self.seating_capacity <= 0:
            return 0.0
        return (len(self.passengers_onboard) / self.seating_capacity) * 100.0

    def can_accept_trip(self) -> bool:
        """A bus can only accept a trip if it is IDLE and not in transit or maintenance."""
        return self.status == "IDLE" and len(self.passengers_onboard) == 0

    def start_boarding(self, route_id: str, trip_id: str, current_time: float):
        if not self.can_accept_trip():
            raise ValueError(f"Bus {self.bus_id} cannot start boarding: currently {self.status}")
        self.total_idle_time += max(0.0, current_time - self.last_status_change_time)
        self.last_status_change_time = current_time
        self.status = "BOARDING"
        self.assigned_route = route_id
        self.current_trip_id = trip_id

    def board_passengers(self, passengers: List[Passenger], current_time: float):
        for p in passengers:
            if len(self.passengers_onboard) >= self.seating_capacity:
                raise OverflowError(f"Bus {self.bus_id} seating capacity {self.seating_capacity} exceeded!")
            p.board(self.bus_id, current_time)
            self.passengers_onboard.append(p)

    def depart(self, current_time: float):
        if self.status != "BOARDING":
            raise ValueError(f"Bus {self.bus_id} must be in BOARDING status to depart, currently {self.status}")
        self.status = "IN_TRANSIT"
        self.current_location = "IN_TRANSIT"

    def complete_trip(self, return_terminal: str, current_time: float):
        if self.status != "IN_TRANSIT":
            raise ValueError(f"Bus {self.bus_id} must be IN_TRANSIT to complete trip, currently {self.status}")
        duration = max(0.0, current_time - self.last_status_change_time)
        self.total_active_time += duration
        self.last_status_change_time = current_time
        
        self.total_passengers_transported += len(self.passengers_onboard)
        self.total_trips_completed += 1
        self.passengers_onboard.clear()
        self.assigned_route = None
        self.current_trip_id = None
        self.current_location = return_terminal
        self.status = "IDLE"

