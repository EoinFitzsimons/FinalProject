# Configuration settings for Momentum simulation
import os

# Database Configuration
DATABASE_PATH = os.path.join(os.path.dirname(__file__), "database", "momentum.db")

# Simulation Parameters
MONTE_CARLO_ITERATIONS = 1000
RANDOM_SEED = 42

# AI Configuration
AI_DECISION_FREQUENCY = 5  # seconds
STRATEGY_COMPLEXITY = "medium"  # low, medium, high

# API Configuration
API_HOST = "127.0.0.1"
API_PORT = 8000
API_RELOAD = True

# Racing Disciplines
DISCIPLINES = {
    "formula": {
        "name": "Formula Racing",
        "categories": ["F1", "F2", "F3"],
        "race_duration_minutes": 90
    },
    "rally": {
        "name": "Rally Racing", 
        "categories": ["WRC", "WRC2", "WRC3"],
        "race_duration_minutes": 180
    },
    "endurance": {
        "name": "Endurance Racing",
        "categories": ["LMP1", "LMP2", "GTE"],
        "race_duration_minutes": 360
    },
    "street": {
        "name": "Street Racing",
        "categories": ["GT3", "GT4", "Touring"],
        "race_duration_minutes": 60
    }
}

# Driver Attributes Range (0.0 to 1.0)
DRIVER_ATTRIBUTES = {
    "skill": {"min": 0.1, "max": 1.0},
    "consistency": {"min": 0.1, "max": 1.0},
    "aggression": {"min": 0.0, "max": 1.0},
    "racecraft": {"min": 0.1, "max": 1.0},
    "adaptability": {"min": 0.1, "max": 1.0}
}

# Team Financial Ranges (in millions)
TEAM_BUDGETS = {
    "tier1": {"min": 100, "max": 400},  # Top teams
    "tier2": {"min": 50, "max": 150},   # Mid-field
    "tier3": {"min": 20, "max": 80}     # Lower teams
}