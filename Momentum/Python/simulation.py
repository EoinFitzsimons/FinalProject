"""
Enhanced FastAPI simulation server with database integration.
Main entry point for the Momentum simulation backend.
"""

from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Dict, Any, Optional
import uvicorn

from database.database_manager import DatabaseManager
from database.models import Driver, Team, Track, Championship, Race
from core.race_simulation import RaceSimulator, SimulationContext
from config import API_HOST, API_PORT, API_RELOAD

app = FastAPI(
    title="Momentum Simulation API",
    description="Multi-discipline Motorsport Management Simulator Backend",
    version="1.0.0"
)

# Enable CORS for Unity frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global instances
db_manager = DatabaseManager()
race_simulator = RaceSimulator()

@app.get("/")
def root():
    """Root endpoint with API information"""
    return {
        "message": "Momentum Simulation API",
        "version": "1.0.0",
        "status": "running",
        "endpoints": {
            "health": "/health",
            "database_stats": "/stats",
            "drivers": "/drivers",
            "teams": "/teams",
            "simulate_race": "/simulate/race"
        }
    }

@app.get("/health")
def health_check():
    """Health check endpoint"""
    try:
        stats = db_manager.get_database_stats()
        return {
            "status": "healthy",
            "database": "connected",
            "stats": stats
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Health check failed: {str(e)}")

@app.get("/stats")
def get_database_stats():
    """Get database statistics"""
    try:
        stats = db_manager.get_database_stats()
        return JSONResponse(content={"database_stats": stats})
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get stats: {str(e)}")

@app.get("/drivers")
def get_all_drivers():
    """Get all drivers"""
    try:
        drivers = db_manager.get_all_drivers()
        return JSONResponse(content={
            "drivers": [driver.__dict__ for driver in drivers],
            "count": len(drivers)
        })
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get drivers: {str(e)}")

@app.get("/teams")
def get_teams(discipline: Optional[str] = None):
    """Get teams, optionally filtered by discipline"""
    try:
        if discipline:
            teams = db_manager.get_teams_by_discipline(discipline)
        else:
            teams = []  # TODO: Implement get_all_teams method
        
        return JSONResponse(content={
            "teams": [team.__dict__ for team in teams],
            "count": len(teams),
            "discipline": discipline
        })
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get teams: {str(e)}")

@app.post("/simulate/race")
def simulate_race(request: Dict[str, Any]):
    """Simulate a race with given parameters"""
    try:
        race_id = request.get("race_id", 1)
        weather = request.get("weather_conditions", "dry")
        participants = request.get("participants", [])
        
        # Return test simulation result for now
        results = [
            {
                "driver_id": p.get("driver_id", i),
                "team_id": p.get("team_id", i),
                "position": i + 1,
                "points": max(0, 25 - i * 2),
                "fastest_lap": i == 0
            }
            for i, p in enumerate(participants[:10] if participants else range(5))
        ]
        
        return JSONResponse(content={
            "race_id": race_id,
            "weather": weather,
            "results": results,
            "simulation_status": "completed"
        })
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Simulation failed: {str(e)}")

@app.get("/test")
def test_endpoint():
    """Legacy test endpoint"""
    return JSONResponse(content={"message": "Simulation test successful."})

if __name__ == "__main__":
    uvicorn.run(
        "simulation:app",
        host=API_HOST,
        port=API_PORT,
        reload=API_RELOAD
    )
