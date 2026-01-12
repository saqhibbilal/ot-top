# Phase 2 Implementation Plan - 4 Parts

## Part 1: Event Processor Service Structure

- Create `event-processor/` directory
- Add requirements.txt (kafka-python, redis)
- Create Dockerfile
- Add to docker-compose.yml

## Part 2: Kafka Consumer Implementation

- Create consumer service that reads from `factory-events` topic
- Parse JSON events
- Basic error handling

## Part 3: Redis State Storage

- Connect to Redis
- Define state storage schema (machine state keys)
- Store latest machine state

## Part 4: Integration

- Process events from Kafka
- Update Redis state for each machine
- Add logging and error handling
