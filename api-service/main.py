"""
API Service - REST API for accessing machine state from Redis
"""

import os
import json
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
import redis

# Configuration
REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", "6379"))

# Create FastAPI app
app = FastAPI(title="OT Analytics API", version="1.0.0")

# Redis client
redis_client = None


@app.on_event("startup")
async def startup_event():
    """Initialize Redis connection on startup"""
    global redis_client
    try:
        redis_client = redis.Redis(
            host=REDIS_HOST,
            port=REDIS_PORT,
            decode_responses=True
        )
        redis_client.ping()
        print(f"Connected to Redis at {REDIS_HOST}:{REDIS_PORT}")
    except Exception as e:
        print(f"Error connecting to Redis: {e}")
        raise


@app.get("/")
async def root():
    """Root endpoint"""
    return {"message": "OT Analytics API", "version": "1.0.0"}


@app.get("/health")
async def health():
    """Health check endpoint"""
    try:
        redis_client.ping()
        return {"status": "healthy", "redis": "connected"}
    except Exception as e:
        return JSONResponse(
            status_code=503,
            content={"status": "unhealthy", "redis": "disconnected", "error": str(e)}
        )


@app.get("/api/machines")
async def get_all_machines():
    """Get all machines with their current state"""
    try:
        # Get all machine IDs
        machine_ids = redis_client.smembers("machines:all")
        
        machines = []
        for machine_id in machine_ids:
            state_key = f"machine:{machine_id}:state"
            state_json = redis_client.get(state_key)
            if state_json:
                machines.append(json.loads(state_json))
        
        return {"machines": machines, "count": len(machines)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/machines/{machine_id}")
async def get_machine(machine_id: str):
    """Get specific machine state"""
    try:
        state_key = f"machine:{machine_id}:state"
        state_json = redis_client.get(state_key)
        
        if not state_json:
            raise HTTPException(status_code=404, detail=f"Machine {machine_id} not found")
        
        return json.loads(state_json)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
