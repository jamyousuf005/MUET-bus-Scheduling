"""
Bus Stop / Terminal Domain Model
Maintains FIFO queues of waiting passengers per destination route.
"""

from typing import List, Dict, Optional
from collections import deque
from models.passenger import Passenger

class BusStop:
    def __init__(self, name: str):
        self.name: str = name
        # FIFO Queue of passengers waiting at this terminal: mapping route_id -> deque of Passengers
        self.queues: Dict[str, deque[Passenger]] = {}
        # Historical queue length tracking: list of tuples (time, route_id, queue_length)
        self.queue_history: List[tuple[float, str, int]] = []
        # Overall queue tracking: (time, total_queue_length)
        self.total_queue_history: List[tuple[float, int]] = []

    def get_queue(self, route_id: str) -> deque[Passenger]:
        if route_id not in self.queues:
            self.queues[route_id] = deque()
        return self.queues[route_id]

    def add_passenger(self, passenger: Passenger, current_time: float):
        """Enqueue passenger in FIFO order."""
        q = self.get_queue(passenger.destination_route)
        q.append(passenger)
        self.record_queue_state(current_time, passenger.destination_route)

    def get_queue_length(self, route_id: Optional[str] = None) -> int:
        """Returns queue length for a specific route, or total terminal queue."""
        if route_id:
            return len(self.queues.get(route_id, []))
        return sum(len(q) for q in self.queues.values())

    def record_queue_state(self, current_time: float, route_id: Optional[str] = None):
        """Log queue length snapshot for time-series analysis."""
        if route_id:
            self.queue_history.append((current_time, route_id, len(self.queues[route_id])))
        self.total_queue_history.append((current_time, self.get_queue_length()))

    def pop_passengers(self, route_id: str, max_count: int, current_time: float) -> List[Passenger]:
        """
        Pop up to max_count passengers in strict FIFO order.
        Any passengers remaining in queue when a bus fills up are marked as left behind.
        """
        q = self.get_queue(route_id)
        boarded: List[Passenger] = []
        
        while q and len(boarded) < max_count:
            boarded.append(q.popleft())
            
        # Mark remaining waiting passengers in this route queue as left behind (if queue was not emptied)
        if q:
            for remaining_pax in q:
                remaining_pax.mark_left_behind()

        self.record_queue_state(current_time, route_id)
        return boarded

