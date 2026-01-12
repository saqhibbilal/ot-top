"""
Event Schema Definition for OT Analytics Platform
"""

from typing import Literal
from dataclasses import dataclass, asdict
from datetime import datetime
import json

# Machine Types
MachineType = Literal["PCB", "Motor", "Tank", "Sensor"]

# Metric Types by Machine
METRIC_TYPES = {
    "PCB": ["temperature", "voltage", "error_code"],
    "Motor": ["rpm", "vibration", "current_draw"],
    "Tank": ["liquid_level", "pressure", "overflow_alert"],
    "Sensor": ["state", "threshold_breach", "fault"]
}

# Severity Levels
Severity = Literal["info", "warning", "critical"]


@dataclass
class FactoryEvent:
    """
    Standard factory machine event structure
    """
    timestamp: str
    machine_id: str
    machine_type: MachineType
    metric_type: str
    value: float | int | str | bool
    severity: Severity

    def to_dict(self) -> dict:
        """Convert event to dictionary"""
        return asdict(self)

    def to_json(self) -> str:
        """Convert event to JSON string"""
        return json.dumps(self.to_dict(), indent=2)

    @classmethod
    def from_dict(cls, data: dict) -> "FactoryEvent":
        """Create event from dictionary"""
        return cls(**data)


# Example events for each machine type
EXAMPLE_EVENTS = {
    "PCB": {
        "temperature": {"value": 65.5, "severity": "info"},
        "voltage": {"value": 12.3, "severity": "info"},
        "error_code": {"value": "E001", "severity": "warning"}
    },
    "Motor": {
        "rpm": {"value": 1450, "severity": "info"},
        "vibration": {"value": 0.15, "severity": "info"},
        "current_draw": {"value": 8.2, "severity": "warning"}
    },
    "Tank": {
        "liquid_level": {"value": 75.0, "severity": "info"},
        "pressure": {"value": 2.5, "severity": "info"},
        "overflow_alert": {"value": False, "severity": "info"}
    },
    "Sensor": {
        "state": {"value": True, "severity": "info"},
        "threshold_breach": {"value": False, "severity": "info"},
        "fault": {"value": "NONE", "severity": "info"}
    }
}
