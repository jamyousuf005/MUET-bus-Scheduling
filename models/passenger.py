"""
Passenger Domain Model
Tracks arrival time, terminal, destination, waiting time, and boarding status.
"""

from dataclasses import dataclass, field
from typing import Optional

@dataclass
class Passenger:
    passenger_id: str
    arrival_time: float             # Simulation time (minutes) of arrival at bus stop
    terminal: str                   # STC or Main Gate
    destination_route: str          # e.g., 'R1_QASIM', 'R2_LATIF', etc.
    boarded_time: Optional[float] = None
    bus_id: Optional[str] = None
    waiting_time: float = 0.0
    is_left_behind: bool = False    # True if a bus arrived and departed while passenger was in queue without boarding
    boarded: bool = False

    def board(self, bus_id: str, current_time: float):
        """Record boarding event and calculate exact waiting time."""
        self.bus_id = bus_id
        self.boarded_time = current_time
        self.waiting_time = max(0.0, current_time - self.arrival_time)
        self.boarded = True

    def mark_left_behind(self):
        """Mark that a bus departed without this passenger boarding due to capacity limit."""
        self.is_left_behind = True

