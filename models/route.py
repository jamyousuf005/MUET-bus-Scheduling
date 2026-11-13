"""
Route Domain Model
Defines bus route attributes, base travel times, distance, and origin terminal.
"""

from dataclasses import dataclass

@dataclass
class Route:
    route_id: str
    name: str
    origin: str          # STC or Main Gate
    destination: str
    base_time_min: float
    distance_km: float

    def get_round_trip_base_time(self) -> float:
        """Returns base round-trip travel time in minutes."""
        return self.base_time_min * 2.0

