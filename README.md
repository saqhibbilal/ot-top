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

### API Endpoints

Once the system is running, the API is available at `http://localhost:8000`:

- `GET /health` - Health check
- `GET /api/machines` - Get all machines with current state
- `GET /api/machines/{machine_id}` - Get specific machine state

Example:

```bash
# Health check
curl http://localhost:8000/health

# Get all machines
curl http://localhost:8000/api/machines

# Get specific machine
curl http://localhost:8000/api/machines/PCB-001
```

### Frontend Dashboard

Access the dashboard at `http://localhost:3000`:

- Real-time machine status monitoring
- Color-coded severity indicators (green/yellow/red)
- Auto-refreshes every 5 seconds
- Modern, clean interface

## Services

- **Kafka**: Event streaming (port 9092)
- **Zookeeper**: Kafka coordination (port 2181)
- **Redis**: State storage (port 6379)
- **Event Simulator**: Generates factory machine events
- **Event Processor**: Consumes events from Kafka and stores state in Redis
- **API Service**: REST API for accessing machine state (port 8000)
- **Frontend**: React dashboard for visualization (port 3000)

## Project Structure

```
.
├── docker-compose.yml      # Infrastructure setup
├── event-simulator/        # Event generation service
├── event-processor/        # Event processing service
├── api-service/           # REST API service
├── frontend/              # React dashboard
├── README.md              # This file
└── .env.example           # Environment variables template
```

## Phase Status

### Phase 1: Infrastructure & Event Simulation ✅

✅ Part 1: Docker Compose Setup (Kafka, Zookeeper, Redis)
✅ Part 2: Project Structure  
✅ Part 3: Event Schema Definition
✅ Part 4: Event Simulator Service

### Phase 2: Event Processing & State Management ✅

✅ Part 1: Event processor service structure
✅ Part 2: Kafka consumer implementation
✅ Part 3: Redis state storage logic
✅ Part 4: Integration - process events and update state

### Phase 3: API Layer & Data Access ✅

✅ Part 1: API service structure
✅ Part 2: Redis connection and basic setup
✅ Part 3: REST endpoints implementation
✅ Part 4: Integration and testing

### Phase 4: Frontend Dashboard & Visualization ✅

✅ Part 1: Frontend structure (React + Vite)
✅ Part 2: Modern UI & theme setup
✅ Part 3: Dashboard components & API integration
✅ Part 4: Docker integration & polish

### Verify Events are Being Published

To verify events are being published to Kafka, you can consume them:

```bash
# View simulator logs (shows events being sent)
docker-compose logs -f event-simulator

# Consume events from Kafka (optional - requires Kafka CLI tools)
docker exec kafka kafka-console-consumer --bootstrap-server localhost:9092 --topic factory-events --from-beginning --max-messages 5
```
