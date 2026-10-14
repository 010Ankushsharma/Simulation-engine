"""Discrete Event Simulation Engine"""
import simpy
from typing import List, Optional
from datetime import datetime
import logging
import random

logger = logging.getLogger(__name__)

class DiscreteEventSimulation:
    def __init__(self, factory_model):
        self.factory_model = factory_model
        self.env = simpy.Environment()
        self.events_log: List[dict] = []
        self.metrics = {
            'total_events': 0,
            'machine_downtime': 0,
            'production_output': 0
        }
    
    def add_event(self, event_type: str, timestamp: datetime, details: dict):
        """Log a discrete event"""
        event = {
            'type': event_type,
            'timestamp': timestamp.isoformat(),
            'details': details,
            'sequence_id': len(self.events_log)
        }
        self.events_log.append(event)
        self.metrics['total_events'] += 1
    
    def run_simulation(self, duration: float, tick_rate: float = 1.0):
        """Run the discrete event simulation"""
        logger.info(f"Starting simulation for {duration} seconds")
        
        time_elapsed = 0
        while time_elapsed < duration:
            current_time = self.env.now
            
            # Process events for this time step
            self._process_events(current_time)
            
            # Advance simulation time
            self.env.step()
            time_elapsed += tick_rate
        
        logger.info(f"Simulation completed. Events logged: {len(self.events_log)}")
        return self.get_results()
    
    def _process_events(self, current_time: float):
        """Process all events for current time step"""
        # Trigger production processes
        for line in self.factory_model.production_lines:
            for machine in line.machines:
                if machine.status == 'running':
                    # Simulate machine operation
                    self._simulate_machine_operation(machine, current_time)
                
                # Check for failure conditions
                if random.random() < 0.001:  # 0.1% failure probability per tick
                    self._trigger_failure(machine, current_time)
    
    def _simulate_machine_operation(self, machine, current_time: float):
        """Simulate machine processing operation"""
        if machine.status == 'running':
            machine.process(1.0)  # Process for 1 time unit
            
            if machine.current_position >= 100:
                # Complete production batch
                self.add_event('production_complete', datetime.utcnow(), {
                    'machine_id': machine.id,
                    'batch_id': f"batch_{machine.id}_{int(current_time)}"
                })
                
                # Reset machine
                machine.current_position = 0
                self.metrics['production_output'] += 1
    
    def _trigger_failure(self, machine, current_time: float):
        """Trigger a random failure event"""
        old_status = machine.status
        machine.update_status('error')
        
        self.add_event('machine_failure', datetime.utcnow(), {
            'machine_id': machine.id,
            'machine_name': machine.name,
            'failure_type': 'random_failure',
            'severity': 'medium'
        })
        
        self.metrics['machine_downtime'] += 1
        
        # Schedule recovery
        self.env.timeout(random.uniform(5, 15))  # Random recovery time
        machine.update_status('running')
        
        self.add_event('machine_recovered', datetime.utcnow(), {
            'machine_id': machine.id
        })
    
    def get_results(self) -> dict:
        """Get simulation results"""
        return {
            'simulation_duration': self.env.now,
            'events_count': len(self.events_log),
            'metrics': self.metrics.copy(),
            'factory_utilization': self.factory_model.overall_utilization,
            'lines_status': [
                {
                    'line_id': line.id,
                    'name': line.name,
                    'throughput': line.throughput,
                    'status': line.status
                }
                for line in self.factory_model.production_lines
            ]
        }
