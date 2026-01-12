"""
Redis State Manager - Handles machine state storage in Redis
"""

import json
import redis
from typing import Dict, Any, Optional


class StateManager:
    """Manages machine state storage in Redis"""
    
    def __init__(self, redis_client: redis.Redis):
        self.redis = redis_client
    
    def update_machine_state(self, event: Dict[str, Any]) -> None:
        """
        Update machine state in Redis
        
        State stored as: machine:{machine_id}:state (JSON hash)
        Also maintains a set of all machine IDs
        """
        machine_id = event.get('machine_id')
        if not machine_id:
            return
        
        # Key for machine state
        state_key = f"machine:{machine_id}:state"
        
        # Prepare state data
        state_data = {
            'machine_id': event.get('machine_id'),
            'machine_type': event.get('machine_type'),
            'last_update': event.get('timestamp'),
            'latest_metric': event.get('metric_type'),
            'latest_value': str(event.get('value')),
            'latest_severity': event.get('severity')
        }
        
        # Store state as JSON
        self.redis.set(state_key, json.dumps(state_data))
        
        # Add machine ID to set of all machines
        self.redis.sadd('machines:all', machine_id)
    
    def get_machine_state(self, machine_id: str) -> Optional[Dict[str, Any]]:
        """Get machine state from Redis"""
        state_key = f"machine:{machine_id}:state"
        state_json = self.redis.get(state_key)
        if state_json:
            return json.loads(state_json)
        return None
    
    def get_all_machines(self) -> list:
        """Get list of all machine IDs"""
        return list(self.redis.smembers('machines:all'))
