"""Production Line Models"""
from typing import List
from dataclasses import dataclass, field
from datetime import datetime

@dataclass
class StationModel:
    """Represents a workstation in a production line"""
    id: int
    name: str
    station_type: str
    processing_time: float
    capacity: int
    status: str = 'active'
    current_queue: int = 0
    
    def process_item(self) -> bool:
        if self.status != 'active' or self.current_queue <= 0:
            return False
        self.current_queue -= 1
        return True

@dataclass
class ProductionLineModel:
    """Complete production line configuration"""
    id: int
    name: str
    stations: List[StationModel] = field(default_factory=list)
    total_capacity: int = 0
    current_throughput: float = 0.0
    status: str = 'active'
    last_update: datetime = field(default_factory=datetime.utcnow)
    
    def add_station(self, station: StationModel):
        self.stations.append(station)
        self.total_capacity += station.capacity
    
    def calculate_theoretical_capacity(self) -> float:
        """Calculate line capacity based on bottleneck station"""
        if not self.stations:
            return 0.0
        
        # Bottleneck is the slowest station
        min_rate = min(s.capacity / s.processing_time for s in self.stations)
        return min_rate
    
    def optimize_layout(self) -> float:
        """Optimize station arrangement for maximum throughput"""
        # Sort stations by processing time
        sorted_stations = sorted(self.stations, key=lambda s: s.processing_time)
        
        # Reconfigure line order
        self.stations = sorted_stations
        return self.calculate_theoretical_capacity()
