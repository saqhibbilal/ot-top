"""
Event Processor - Consumes events from Kafka and stores state in Redis
"""

import os
import json
import time
from kafka import KafkaConsumer
from kafka.errors import KafkaError
import redis
from state_manager import StateManager

# Configuration
KAFKA_BROKER = os.getenv("KAFKA_BROKER", "localhost:9092")
KAFKA_TOPIC = os.getenv("KAFKA_TOPIC", "factory-events")
REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", "6379"))


def main():
    """Main processor loop"""
    print("Starting Event Processor...")
    print(f"Kafka Broker: {KAFKA_BROKER}")
    print(f"Kafka Topic: {KAFKA_TOPIC}")
    print(f"Redis: {REDIS_HOST}:{REDIS_PORT}")
    
    # Connect to Redis
    print("Connecting to Redis...")
    try:
        redis_client = redis.Redis(
            host=REDIS_HOST,
            port=REDIS_PORT,
            decode_responses=True
        )
        redis_client.ping()
        print("Connected to Redis successfully!")
    except Exception as e:
        print(f"Error connecting to Redis: {e}")
        return
    
    # Create state manager
    state_manager = StateManager(redis_client)
    
    # Create Kafka consumer
    print("Connecting to Kafka...")
    max_retries = 30
    consumer = None
    for attempt in range(max_retries):
        try:
            consumer = KafkaConsumer(
                KAFKA_TOPIC,
                bootstrap_servers=[KAFKA_BROKER],
                value_deserializer=lambda m: json.loads(m.decode('utf-8')),
                auto_offset_reset='latest',
                enable_auto_commit=True
            )
            print("Connected to Kafka successfully!")
            break
        except Exception as e:
            if attempt < max_retries - 1:
                print(f"Connection attempt {attempt + 1}/{max_retries} failed, retrying in 2 seconds...")
                time.sleep(2)
            else:
                print(f"Error connecting to Kafka after {max_retries} attempts: {e}")
                return
    
    if consumer is None:
        return
    
    event_count = 0
    
    try:
        print("Processing events...")
        for message in consumer:
            try:
                event = message.value
                
                # Update machine state in Redis
                state_manager.update_machine_state(event)
                
                event_count += 1
                
                if event_count % 10 == 0:
                    machine_id = event.get('machine_id', 'unknown')
                    metric_type = event.get('metric_type', 'unknown')
                    print(f"Processed {event_count} events... (Latest: {machine_id} - {metric_type})")
                    
            except Exception as e:
                print(f"Error processing event: {e}")
                
    except KeyboardInterrupt:
        print(f"\nStopping processor... (Total events processed: {event_count})")
    finally:
        if consumer:
            consumer.close()


if __name__ == "__main__":
    main()
