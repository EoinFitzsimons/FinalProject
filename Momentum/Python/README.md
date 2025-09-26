# Momentum Python Backend Structure

## Core Modules (`core/`)
- `race_simulation.py` - Monte Carlo race outcome models
- `driver_progression.py` - Driver skill evolution and career arcs
- `team_management.py` - Financial systems, budgets, operations
- `championship_manager.py` - Multi-league season management
- `procedural_generation.py` - Minor procedural elements (staff names, etc.)

## AI Modules (`ai/`)
- `decision_engine.py` - AI decision-making framework
- `strategy_ai.py` - Race strategy and pit decisions
- `team_ai.py` - Long-term team planning and resource allocation
- `narrative_engine.py` - Emergent storyline generation

## Database (`database/`)
- `models.py` - SQLite schema definitions
- `historical_data.py` - Handcrafted teams, drivers, tracks data
- `database_manager.py` - CRUD operations and queries
- `seed_data.sql` - Initial database population scripts

## Tests (`tests/`)
- `test_simulation.py` - Race simulation unit tests
- `test_ai.py` - AI decision-making tests
- `test_database.py` - Database integrity tests
- `test_integration.py` - Python-Unity communication tests

## Entry Points
- `simulation.py` - FastAPI server and main entry point
- `config.py` - Configuration settings and constants