# OT Analytics Platform

A simulated Operational Technology (OT) analytics platform that collects, processes, and visualizes real-time event logs from factory equipment.

## Architecture

- **Event Streaming**: Apache Kafka
- **State Storage**: Redis
- **Event Simulation**: Python service
- **Containerization**: Docker & Docker Compose

## Quick Start

### Prerequisites

- Docker
- Docker Compose

### Run the System

```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop all services
docker-compose down
```

## Services

- **Kafka**: Event streaming (port 9092)
- **Zookeeper**: Kafka coordination (port 2181)
- **Redis**: State storage (port 6379)
- **Event Simulator**: Generates factory machine events

## Project Structure

```
.
├── docker-compose.yml      # Infrastructure setup
├── event-simulator/        # Event generation service
├── README.md              # This file
└── .env.example           # Environment variables template
```

## Phase 1 Status

✅ Part 1: Docker Compose Setup (Kafka, Zookeeper, Redis)
✅ Part 2: Project Structure  
✅ Part 3: Event Schema Definition
✅ Part 4: Event Simulator Service

**Phase 1 Complete!** ✅ The system is now generating and publishing factory events to Kafka.

### Verify Events are Being Published

To verify events are being published to Kafka, you can consume them:

```bash
# View simulator logs (shows events being sent)
docker-compose logs -f event-simulator

# Consume events from Kafka (optional - requires Kafka CLI tools)
docker exec kafka kafka-console-consumer --bootstrap-server localhost:9092 --topic factory-events --from-beginning --max-messages 5
```
