# Event Simulator

Generates factory machine events and publishes them to Kafka.

## Event Schema

Each event contains:

- `timestamp`: ISO format timestamp
- `machine_id`: Unique identifier for the machine
- `machine_type`: Type of machine (PCB, Motor, Tank, Sensor)
- `metric_type`: Type of metric being measured
- `value`: Metric value (number, string, or boolean)
- `severity`: Event severity (info, warning, critical)

## Machine Types

### PCB

- Metrics: temperature, voltage, error_code
- Example: `{"temperature": 65.5, "severity": "info"}`

### Motor

- Metrics: rpm, vibration, current_draw
- Example: `{"rpm": 1450, "severity": "info"}`

### Tank

- Metrics: liquid_level, pressure, overflow_alert
- Example: `{"liquid_level": 75.0, "severity": "info"}`

### Sensor

- Metrics: state, threshold_breach, fault
- Example: `{"state": true, "severity": "info"}`
