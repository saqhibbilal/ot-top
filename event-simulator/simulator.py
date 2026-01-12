"""
Event Simulator - Generates factory machine events and publishes to Kafka
"""

import os
import time
import random
import json
from datetime import datetime
from kafka import KafkaProducer
from kafka.errors import KafkaError
from schema import FactoryEvent, MachineType, METRIC_TYPES, EXAMPLE_EVENTS, Severity

# Configuration
KAFKA_BROKER = os.getenv("KAFKA_BROKER", "localhost:9092")
KAFKA_TOPIC = os.getenv("KAFKA_TOPIC", "factory-events")
EVENT_RATE = int(os.getenv("EVENT_RATE", "5"))  # events per second
INTERVAL = 1.0 / EVENT_RATE

# Machine IDs
MACHINE_IDS = {
    "PCB": [f"PCB-{i:03d}" for i in range(1, 6)],
    "Motor": [f"MOTOR-{i:03d}" for i in range(1, 6)],
    "Tank": [f"TANK-{i:03d}" for i in range(1, 6)],
    "Sensor": [f"SENSOR-{i:03d}" for i in range(1, 6)]
}


def generate_value(machine_type: MachineType, metric_type: str) -> tuple:
    """
    Generate a realistic value for a given metric type
    Returns: (value, severity)
    """
    examples = EXAMPLE_EVENTS[machine_type][metric_type]
    base_value = examples["value"]
    base_severity = examples["severity"]

    # Add randomness to values
    if isinstance(base_value, (int, float)):
        if metric_type == "temperature":
            value = round(base_value + random.uniform(-10, 10), 1)
            severity = "critical" if value > 80 else "warning" if value > 70 else "info"
        elif metric_type == "voltage":
            value = round(base_value + random.uniform(-1, 1), 1)
            severity = "critical" if value < 10 or value > 15 else "warning" if value < 11 or value > 14 else "info"
        elif metric_type == "rpm":
            value = int(base_value + random.uniform(-100, 100))
            severity = "critical" if value > 2000 or value < 500 else "warning" if value > 1800 or value < 800 else "info"
        elif metric_type == "vibration":
            value = round(base_value + random.uniform(-0.05, 0.05), 2)
            severity = "critical" if value > 0.3 else "warning" if value > 0.2 else "info"
        elif metric_type == "current_draw":
            value = round(base_value + random.uniform(-1, 1), 1)
            severity = "critical" if value > 12 else "warning" if value > 10 else "info"
        elif metric_type == "liquid_level":
            value = round(base_value + random.uniform(-10, 10), 1)
            severity = "critical" if value > 90 or value < 10 else "warning" if value > 80 or value < 20 else "info"
        elif metric_type == "pressure":
            value = round(base_value + random.uniform(-0.5, 0.5), 1)
            severity = "critical" if value > 4.0 else "warning" if value > 3.0 else "info"
        else:
            value = base_value
            severity = base_severity
    else:
        value = base_value
        severity = base_severity

    # Randomly change severity for some events
    if random.random() < 0.1:  # 10% chance
        if severity == "info":
            severity = "warning" if random.random() < 0.5 else severity
        elif severity == "warning":
            severity = "critical" if random.random() < 0.3 else severity

    return value, severity


def create_event() -> FactoryEvent:
    """Create a random factory event"""
    # Pick random machine type
    machine_type: MachineType = random.choice(["PCB", "Motor", "Tank", "Sensor"])
    
    # Pick random machine ID for this type
    machine_id = random.choice(MACHINE_IDS[machine_type])
    
    # Pick random metric type
    metric_type = random.choice(METRIC_TYPES[machine_type])
    
    # Generate value and severity
    value, severity = generate_value(machine_type, metric_type)
    
    # Create event
    event = FactoryEvent(
        timestamp=datetime.utcnow().isoformat() + "Z",
        machine_id=machine_id,
        machine_type=machine_type,
        metric_type=metric_type,
        value=value,
        severity=severity
    )
    
    return event


def main():
    """Main simulator loop"""
    print(f"Starting Event Simulator...")
    print(f"Kafka Broker: {KAFKA_BROKER}")
    print(f"Kafka Topic: {KAFKA_TOPIC}")
    print(f"Event Rate: {EVENT_RATE} events/second")
    print(f"Interval: {INTERVAL:.2f} seconds")
    
    # Create Kafka producer with retry logic
    print("Waiting for Kafka to be ready...")
    producer = None
    max_retries = 30
    for attempt in range(max_retries):
        try:
            producer = KafkaProducer(
                bootstrap_servers=[KAFKA_BROKER],
                value_serializer=lambda v: json.dumps(v.to_dict()).encode('utf-8'),
                retries=3,
                acks='all'
            )
            print("Connected to Kafka successfully!")
            break
        except Exception as e:
            if attempt < max_retries - 1:
                print(f"Connection attempt {attempt + 1}/{max_retries} failed, retrying in 2 seconds...")
                time.sleep(2)
            else:
                print(f"Error connecting to Kafka after {max_retries} attempts: {e}")
                print("Make sure Kafka is running and accessible")
                return
    
    if producer is None:
        return
    
    event_count = 0
    
    try:
        while True:
            # Generate event
            event = create_event()
            
            # Send to Kafka
            try:
                future = producer.send(KAFKA_TOPIC, event)
                # Wait for confirmation
                record_metadata = future.get(timeout=10)
                event_count += 1
                
                if event_count % 10 == 0:
                    print(f"Sent {event_count} events... (Latest: {event.machine_id} - {event.metric_type} = {event.value})")
            except KafkaError as e:
                print(f"Error sending event: {e}")
            
            # Wait before next event
            time.sleep(INTERVAL)
            
    except KeyboardInterrupt:
        print(f"\nStopping simulator... (Total events sent: {event_count})")
    finally:
        producer.close()


if __name__ == "__main__":
    main()
