
# Momentum - Multi-discipline Motorsport Management Simulator

**Project Type:** Multi-discipline Motorsport Management Simulator  
**Development Scope:** Python back-end simulation + Unity front-end visualization

## Project Overview

Momentum is a persistent, emergent motorsport management simulation that spans multiple racing disciplines, leagues, and competition tiers. Unlike existing motorsport titles, Momentum emphasizes strategic depth, historical immersion, and emergent dynamics rather than driving mechanics. Players act as team principals, making managerial, financial, and strategic decisions that influence team performance, driver careers, and championship outcomes.

## Core Philosophy

- **Management-Only Gameplay:** Players never drive vehicles. Unity renders race outcomes, dashboards, statistics, and team information for strategic decision-making.
- **Persistent, Evolving World:** Python fully simulates all leagues, events, and AI teams independently of player interaction.
- **Historical Depth:** Teams, drivers, tracks, and championships carry detailed biographies, histories, and legacy statistics.
- **Multi-Discipline Coverage:** Rally, endurance, street, and open-wheel racing with distinct strategic considerations.

## System Architecture

### Python Back-End Simulation Engine (`Momentum/Python/`)
- **Core Simulation:** Monte Carlo race outcome models integrating driver attributes, car performance, track factors
- **Driver Progression:** Probabilistic growth models for skill, consistency, fatigue resilience, career arcs
- **Financial Systems:** Team budgets, sponsorships, operational costs, unexpected events
- **AI Decision-Making:** Pit strategies, driver rotations, resource allocation, long-term planning
- **Database Management:** SQLite persistence for multi-season histories, team achievements, rivalry records

### Unity Front-End Interface (`Momentum/Unity/`)
- **Race Visualization:** Telemetry, standings, team dashboards, historical statistics
- **Management UI:** Strategy decisions, finances, staffing, team operations
- **Real-time Updates:** Asynchronous JSON communication with Python backend
- **Performance Optimization:** Smooth updates without frame drops or UI latency

### Data Exchange
- **Communication:** JSON messages via HTTP/WebSockets
- **Persistence:** SQLite database with handcrafted historical data
- **Flow:** Python simulates → SQLite → JSON → Unity renders

## Technical Stack

- **Back-End:** Python 3.11+, NumPy, Pandas, SciPy, PyTorch, SQLite, FastAPI
- **Front-End:** Unity 2023+, C#, Unity UI
- **Tools:** VS Code, GitHub Desktop, SQLite browser
- **Infrastructure:** Optional cloud VMs, CI/CD via GitHub Actions

## Setup Instructions

### Python Backend
1. Navigate to Python directory: `cd Momentum/Python`
2. Install dependencies: `pip install -r requirements.txt`
3. Run simulation server: `uvicorn simulation:app --reload`

### Unity Front-End
- Open `Momentum/Unity` in Unity Editor
- Configure HTTP client for Python API communication

## Development Phases

1. **Foundation:** Requirements, architecture, design documentation
2. **Core Engine:** Race outcomes, driver progression, financial systems
3. **Historical Database:** Handcrafted teams, drivers, tracks, championships
4. **AI Integration:** Dynamic decision-making and emergent narratives
5. **Unity Frontend:** Dashboards, visualization, management interface
6. **Testing & Refinement:** Unit, integration, system, user evaluation

## Requirements

- **Python:** 3.11+
- **Unity:** 2023+
- **Database:** SQLite (builtin)
- **AI/ML:** PyTorch for advanced AI modules
