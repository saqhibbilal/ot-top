# Phase 3 Implementation Plan - 4 Parts

## Part 1: API Service Structure

- Create `api-service/` directory
- Add requirements.txt (FastAPI, uvicorn, redis)
- Create Dockerfile
- Basic FastAPI app structure

## Part 2: Redis Connection & Basic API Setup

- Connect to Redis
- Create FastAPI app
- Health check endpoint

## Part 3: REST Endpoints

- GET /api/machines - List all machines
- GET /api/machines/{machine_id} - Get specific machine state
- GET /api/health - Health check

## Part 4: Integration

- Add to docker-compose.yml
- Test endpoints
- Verify data flow
