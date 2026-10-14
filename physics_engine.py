"""Physics Engine for Factory Simulations"""
from typing import List, Tuple
import math

class PhysicsEngine:
    """Simulates physical aspects of factory operations"""
    
    @staticmethod
    def calculate_cycle_time(base_time: float, load_factor: float = 1.0) -> float:
        """Calculate actual cycle time considering load factor"""
        return base_time * (1 + (load_factor - 1) * 0.5)
    
    @staticmethod
    def calculate_efficiency(actual_output: float, theoretical_max: float) -> float:
        """Calculate production efficiency"""
        if theoretical_max <= 0:
            return 0.0
        return (actual_output / theoretical_max) * 100
    
    @staticmethod
    def calculate_utilization(active_time: float, available_time: float) -> float:
        """Calculate equipment utilization"""
        if available_time <= 0:
            return 0.0
        return (active_time / available_time) * 100
    
    @staticmethod
    def predict_downtime(consecutive_failures: int, avg_failure_interval: float) -> float:
        """Predict downtime based on failure patterns"""
        return consecutive_failures * (avg_failure_interval / 10)
    
    @staticmethod
    def calculate_queue_delay(queue_size: int, service_rate: float) -> float:
        """Calculate expected queue delay"""
        if service_rate <= 0:
            return float('inf')
        return queue_size / service_rate
    
    @staticmethod
    def simulate_material_flow(inflow_rate: float, outflow_rate: float, 
                              capacity: float, time_period: float) -> float:
        """Simulate material inventory flow"""
        initial_inventory = capacity * 0.5  # Start at 50%
        net_flow = inflow_rate - outflow_rate
        final_inventory = initial_inventory + (net_flow * time_period)
        return max(0, min(capacity, final_inventory))
    
    @staticmethod
    def calculate_energy_consumption(power_rating: float, utilization: float, 
                                    time_hours: float) -> float:
        """Calculate energy consumption"""
        return power_rating * (utilization / 100) * time_hours
    
    @staticmethod
    def analyze_bottleneck(process_times: List[float]) -> Tuple[int, float]:
        """Identify bottleneck process and its impact"""
        if not process_times:
            return -1, 0.0
        
        bottleneck_idx = process_times.index(max(process_times))
        bottleneck_time = max(process_times)
        avg_time = sum(process_times) / len(process_times)
        
        impact = ((bottleneck_time - avg_time) / avg_time) * 100 if avg_time > 0 else 0
        return bottleneck_idx, impact
