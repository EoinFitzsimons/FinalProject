# Momentum Project Documentation

## Architecture Overview

### System Components

1. **Python Backend (`Momentum/Python/`)**
   - FastAPI server with REST endpoints
   - Monte Carlo race simulation engine
   - SQLite database with historical data
   - AI decision-making systems
   - Procedural content generation

2. **Unity Frontend (`Momentum/Unity/`)**
   - Management interface and dashboards
   - Race visualization and telemetry
   - Real-time communication with Python backend
   - Player decision input systems

3. **Database Layer**
   - SQLite for persistence
   - Handcrafted historical data
   - Multi-season championship tracking
   - Driver career progression
   - Team financial modeling

### Data Flow Architecture

```
Player Input (Unity) 
    ↓
HTTP/JSON API 
    ↓
Python Backend Processing
    ↓
Database Updates (SQLite)
    ↓
Simulation Engine
    ↓
AI Decision Making
    ↓
Results (JSON Response)
    ↓
Unity UI Updates
```

## Development Status

### Completed Components

- ✅ Repository structure and organization
- ✅ FastAPI server foundation with CORS support
- ✅ SQLite database schema and models
- ✅ Database manager with CRUD operations
- ✅ Configuration management system
- ✅ Monte Carlo race simulation engine (basic)
- ✅ API endpoints for drivers, teams, and simulation
- ✅ Enhanced requirements.txt with all dependencies

### Current Implementation

The current implementation provides:

1. **API Endpoints:**
   - `GET /` - API information and available endpoints
   - `GET /health` - Health check with database stats
   - `GET /stats` - Database statistics
   - `GET /drivers` - All drivers data
   - `GET /teams` - Teams data (filtered by discipline)
   - `POST /simulate/race` - Race simulation endpoint
   - `GET /test` - Legacy test endpoint

2. **Database Schema:**
   - Drivers with skill attributes and career stats
   - Teams with financial and operational data
   - Tracks with characteristics and difficulty ratings
   - Championships with points systems and seasons
   - Races and race results with full history
   - Proper indexing for performance

3. **Simulation Engine:**
   - Monte Carlo race outcome simulation
   - Driver skill integration (skill, consistency, racecraft, etc.)
   - Team performance factors (budget, tier)
   - Track suitability calculations
   - Weather impact modeling
   - Strategy simulation framework

### Next Development Phase

To complete the Momentum project, implement:

1. **Historical Data Population:**
   - Create seed data scripts for teams, drivers, tracks
   - Populate championships and season structures
   - Add realistic biographies and historical context

2. **AI Systems:**
   - Enhanced decision-making algorithms
   - Dynamic strategy systems
   - Emergent narrative generation
   - Long-term career progression

3. **Unity Frontend:**
   - Create Unity project structure
   - Implement HTTP client for API communication
   - Design management interface
   - Add race visualization components

4. **Advanced Features:**
   - Multi-discipline racing support
   - Financial management systems
   - Procedural staff generation
   - Championship progression logic

5. **Testing & Polish:**
   - Unit tests for all modules
   - Integration testing
   - Performance optimization
   - Documentation completion

## Technical Specifications

### Python Backend Requirements
- Python 3.11+
- FastAPI for REST API
- NumPy/SciPy for simulation mathematics
- PyTorch for AI systems (when implemented)
- SQLite for data persistence

### Unity Frontend Requirements
- Unity 2023+
- C# scripting
- Unity UI system
- HTTP client for API communication

### Development Tools
- VS Code for development
- GitHub Desktop for version control
- SQLite browser for database inspection
- Postman/Thunder Client for API testing

## Getting Started

1. **Install Python Dependencies:**
   ```bash
   cd Momentum/Python
   pip install -r requirements.txt
   ```

2. **Start the Backend Server:**
   ```bash
   cd Momentum/Python
   uvicorn simulation:app --reload
   ```

3. **Test API Endpoints:**
   - Visit http://127.0.0.1:8000 for API information
   - Test endpoints with Postman or browser
   - Check /health endpoint for database connection

4. **Unity Development:**
   - Create new Unity project in `Momentum/Unity/`
   - Implement HTTP client for API communication
   - Build management interface components

## Project Vision

Momentum aims to be a comprehensive motorsport management simulation that combines:

- **Historical Depth:** Rich, handcrafted world with detailed biographies
- **Emergent Gameplay:** AI-driven narratives and dynamic championships
- **Strategic Complexity:** Multi-layered decision making
- **Technical Excellence:** Robust simulation engines and clean architecture

The current foundation provides the technical infrastructure needed to build this vision, with a solid API backend, database system, and simulation engine ready for expansion.