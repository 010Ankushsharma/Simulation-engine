"""Factory Model for Digital Twin Simulation"""
import random
from typing import List, Dict
from dataclasses import dataclass, field
from datetime import datetime

@dataclass
class MachineModel:
    """Represents a virtual machine in the simulation"""
    id: int
    name: str
    machine_type: str
    status: str = 'running'
    utilization: float = 0.0
    cycle_time: float = 60.0  # seconds
    current_position: float = 0.0
    last_update: datetime = field(default_factory=datetime.utcnow)
    
    def update_status(self, status: str):
        self.status = status
        self.last_update = datetime.utcnow()
    
    def process(self, duration: float) -> bool:
        """Simulate machine processing"""
        if self.status != 'running':
            return False
        
        self.current_position += duration / self.cycle_time
        self.utilization = min(100.0, self.current_position * 100)
        self.last_update = datetime.utcnow()
        return True
    
    def get_health_score(self) -> float:
        """Calculate machine health score based on various factors"""
        base_score = 100.0
        wear_factor = max(0, 100 - (self.current_position / 10))
        efficiency_factor = self.utilization / 100 * 100
        return (base_score * 0.5 + wear_factor * 0.3 + efficiency_factor * 0.2)

@dataclass
class ProductionLineModel:
    """Represents a production line in the simulation"""
    id: int
    name: str
    machines: List[MachineModel] = field(default_factory=list)
    queue_length: int = 0
    throughput: float = 0.0
    status: str = 'active'
    
    def add_machine(self, machine: MachineModel):
        self.machines.append(machine)
    
    def calculate_throughput(self) -> float:
        """Calculate line throughput based on bottleneck machine"""
        if not self.machines:
            return 0.0
        
        running_machines = [m for m in self.machines if m.status == 'running']
        if not running_machines:
            return 0.0
            
        min_cycle_time = min(m.cycle_time for m in running_machines)
        return 60.0 / min_cycle_time if min_cycle_time > 0 else 0.0
    
    def simulate_step(self, time_step: float):
        """Simulate one time step for the production line"""
        for machine in self.machines:
            if machine.status == 'running':
                machine.process(time_step)
        
        # Update queue
        self.queue_length = max(0, self.queue_length - len(self.machines))
        self.throughput = self.calculate_throughput()

@dataclass
class FactoryModel:
    """Represents an entire factory in the simulation"""
    id: int
    name: str
    production_lines: List[ProductionLineModel] = field(default_factory=list)
    total_machines: int = 0
    overall_utilization: float = 0.0
    status: str = 'active'
    
    def add_production_line(self, line: ProductionLineModel):
        self.production_lines.append(line)
        self.total_machines = sum(len(line.machines) for line in self.production_lines)
    
    def calculate_overall_utilization(self) -> float:
        """Calculate factory-wide utilization"""
        if self.total_machines == 0:
            return 0.0
        
        total_util = sum(m.utilization for line in self.production_lines for m in line.machines)
        return total_util / self.total_machines
    
    def simulate_step(self, time_step: float):
        """Simulate one time step for the entire factory"""
        for line in self.production_lines:
            line.simulate_step(time_step)
        
        self.overall_utilization = self.calculate_overall_utilization()
        self.status = 'active' if self.overall_utilization > 0 else 'idle'
