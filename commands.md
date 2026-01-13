# Commands Guide

Quick reference for cloning and running the OT Analytics Platform.

## GitHub Setup

Clone the repository:

```bash
git clone <repository-url>
cd opkii
```

Or if using SSH:

```bash
git clone git@github.com:username/opkii.git
cd opkii
```

## Initial Setup

Build and start all services:

```bash
docker-compose up -d --build
```

## Running the System

Start all services (after initial build):

```bash
docker-compose up -d
```

View logs from all services:

```bash
docker-compose logs -f
```

View logs from a specific service:

```bash
docker-compose logs -f frontend
docker-compose logs -f api-service
docker-compose logs -f event-processor
docker-compose logs -f event-simulator
```

Check service status:

```bash
docker-compose ps
```

## Stopping the System

Stop all services:

```bash
docker-compose down
```

Stop and remove all volumes (clean slate):

```bash
docker-compose down -v
```

## Access Points

- **Frontend Dashboard**: http://localhost:3000
- **API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs

## Quick Start (First Time)

```bash
# 1. Clone the repository
git clone <repository-url>
cd opkii

# 2. Build and start everything
docker-compose up -d --build

# 3. Wait for services to start (about 30-60 seconds)
# 4. Open http://localhost:3000 in your browser
```
