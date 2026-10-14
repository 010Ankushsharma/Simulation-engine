"""Event Simulator for Factory Operations"""
from typing import List, Dict, Any
from datetime import datetime
import random
import logging

logger = logging.getLogger(__name__)

class EventSimulator:
    def __init__(self):
        self.event_types = ['start', 'stop', 'maintenance', 'error', 'warning', 'complete']
        self.severity_levels = ['info', 'warning', 'critical']
        self.factories = {}
    
    def create_event(self, event_type: str, factory_id: int, machine_id: int = None, 
                     extra_data: Dict[str, Any] = None) -> Dict[str, Any]:
        """Create a standardized event"""
        event = {
            'id': f"evt_{datetime.utcnow().timestamp()}",
            'type': event_type,
            'timestamp': datetime.utcnow().isoformat(),
            'factory_id': factory_id,
            'machine_id': machine_id,
            'severity': random.choice(self.severity_levels),
            'data': extra_data or {},
            'source': 'simulator'
        }
        return event
    
    def simulate_sensor_readings(self, factory_id: int, machine_ids: List[int]) -> List[Dict]:
        """Generate simulated sensor readings"""
        readings = []
        
        sensor_types = ['temperature', 'vibration', 'pressure', 'speed', 'energy']
        
        for machine_id in machine_ids:
            for sensor_type in sensor_types:
                reading = {
                    'sensor_id': f"sensor_{machine_id}_{sensor_type}",
                    'machine_id': machine_id,
                    'factory_id': factory_id,
                    'type': sensor_type,
                    'value': self._generate_sensor_value(sensor_type),
                    'unit': self._get_sensor_unit(sensor_type),
                    'timestamp': datetime.utcnow().isoformat(),
                    'quality': random.choice(['good', 'good', 'good', 'fair', 'poor'])
                }
                readings.append(reading)
        
        return readings
    
    def _generate_sensor_value(self, sensor_type: str) -> float:
        """Generate realistic sensor value"""
        if sensor_type == 'temperature':
            return round(random.uniform(40, 80), 2)  # Celsius
        elif sensor_type == 'vibration':
            return round(random.uniform(0.1, 5.0), 3)  # mm/s
        elif sensor_type == 'pressure':
            return round(random.uniform(90, 110), 2)  # bar
        elif sensor_type == 'speed':
            return round(random.uniform(50, 200), 1)  # RPM
        elif sensor_type == 'energy':
            return round(random.uniform(10, 50), 2)  # kWh
        return 0.0
    
    def _get_sensor_unit(self, sensor_type: str) -> str:
        """Get unit for sensor type"""
        units = {
            'temperature': '°C',
            'vibration': 'mm/s',
            'pressure': 'bar',
            'speed': 'RPM',
            'energy': 'kWh'
        }
        return units.get(sensor_type, 'units')
    
    def generate_event_stream(self, factory_id: int, machine_ids: List[int], 
                             events_per_second: int = 100) -> List[Dict]:
        """Generate continuous event stream"""
        events = []
        
        # Generate machine state change events
        for _ in range(events_per_second // 2):
            if machine_ids:
                machine_id = random.choice(machine_ids)
                event = self.create_event(
                    event_type=random.choice(self.event_types),
                    factory_id=factory_id,
                    machine_id=machine_id
                )
                events.append(event)
        
        # Generate sensor readings
        sensor_readings = self.simulate_sensor_readings(factory_id, machine_ids)
        events.extend(sensor_readings)
        
        return events
