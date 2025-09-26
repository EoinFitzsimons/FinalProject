"""
SQLite database models for Momentum motorsport simulation.
Defines the schema for teams, drivers, tracks, championships, and historical data.
"""

import sqlite3
from dataclasses import dataclass
from typing import Optional, List, Dict
from datetime import datetime

@dataclass
class Driver:
    """Driver entity with attributes and historical data"""
    id: int
    name: str
    nationality: str
    birth_date: str
    skill: float  # 0.0 to 1.0
    consistency: float
    aggression: float
    racecraft: float
    adaptability: float
    career_wins: int = 0
    career_podiums: int = 0
    career_points: int = 0
    biography: str = ""
    current_team_id: Optional[int] = None

@dataclass
class Team:
    """Team entity with financial and operational data"""
    id: int
    name: str
    nationality: str
    founded_year: int
    discipline: str  # formula, rally, endurance, street
    tier: str  # tier1, tier2, tier3
    budget: float  # in millions
    headquarters: str
    team_principal: str
    biography: str = ""
    total_wins: int = 0
    total_podiums: int = 0
    championships: int = 0

@dataclass
class Track:
    """Racing track/circuit with characteristics"""
    id: int
    name: str
    country: str
    length_km: float
    surface_type: str  # tarmac, gravel, mixed
    difficulty: float  # 0.0 to 1.0
    weather_impact: float  # how much weather affects performance
    overtaking_difficulty: float  # 0.0 to 1.0
    discipline: str
    lap_record_time: Optional[str] = None
    description: str = ""

@dataclass
class Championship:
    """Championship/League definition"""
    id: int
    name: str
    discipline: str
    tier: str
    season_length: int  # number of races
    points_system: str  # JSON string of points distribution
    current_season: int
    founded_year: int
    description: str = ""

@dataclass
class Race:
    """Individual race instance"""
    id: int
    championship_id: int
    track_id: int
    season: int
    round_number: int
    race_date: str
    weather_conditions: str
    race_duration_minutes: int
    status: str  # scheduled, completed, cancelled

@dataclass
class RaceResult:
    """Race result for a driver"""
    id: int
    race_id: int
    driver_id: int
    team_id: int
    position: int
    points: int
    fastest_lap: bool = False
    dnf_reason: Optional[str] = None
    grid_position: int = 1

# Database Schema Creation SQL
SCHEMA_SQL = """
-- Drivers table
CREATE TABLE IF NOT EXISTS drivers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    nationality TEXT NOT NULL,
    birth_date TEXT NOT NULL,
    skill REAL NOT NULL CHECK(skill >= 0.0 AND skill <= 1.0),
    consistency REAL NOT NULL CHECK(consistency >= 0.0 AND consistency <= 1.0),
    aggression REAL NOT NULL CHECK(aggression >= 0.0 AND aggression <= 1.0),
    racecraft REAL NOT NULL CHECK(racecraft >= 0.0 AND racecraft <= 1.0),
    adaptability REAL NOT NULL CHECK(adaptability >= 0.0 AND adaptability <= 1.0),
    career_wins INTEGER DEFAULT 0,
    career_podiums INTEGER DEFAULT 0,
    career_points INTEGER DEFAULT 0,
    biography TEXT DEFAULT '',
    current_team_id INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (current_team_id) REFERENCES teams (id)
);

-- Teams table
CREATE TABLE IF NOT EXISTS teams (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    nationality TEXT NOT NULL,
    founded_year INTEGER NOT NULL,
    discipline TEXT NOT NULL CHECK(discipline IN ('formula', 'rally', 'endurance', 'street')),
    tier TEXT NOT NULL CHECK(tier IN ('tier1', 'tier2', 'tier3')),
    budget REAL NOT NULL,
    headquarters TEXT NOT NULL,
    team_principal TEXT NOT NULL,
    biography TEXT DEFAULT '',
    total_wins INTEGER DEFAULT 0,
    total_podiums INTEGER DEFAULT 0,
    championships INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tracks table
CREATE TABLE IF NOT EXISTS tracks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    country TEXT NOT NULL,
    length_km REAL NOT NULL,
    surface_type TEXT NOT NULL CHECK(surface_type IN ('tarmac', 'gravel', 'mixed')),
    difficulty REAL NOT NULL CHECK(difficulty >= 0.0 AND difficulty <= 1.0),
    weather_impact REAL NOT NULL CHECK(weather_impact >= 0.0 AND weather_impact <= 1.0),
    overtaking_difficulty REAL NOT NULL CHECK(overtaking_difficulty >= 0.0 AND overtaking_difficulty <= 1.0),
    discipline TEXT NOT NULL CHECK(discipline IN ('formula', 'rally', 'endurance', 'street')),
    lap_record_time TEXT,
    description TEXT DEFAULT '',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Championships table
CREATE TABLE IF NOT EXISTS championships (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    discipline TEXT NOT NULL CHECK(discipline IN ('formula', 'rally', 'endurance', 'street')),
    tier TEXT NOT NULL CHECK(tier IN ('tier1', 'tier2', 'tier3')),
    season_length INTEGER NOT NULL,
    points_system TEXT NOT NULL, -- JSON string
    current_season INTEGER NOT NULL,
    founded_year INTEGER NOT NULL,
    description TEXT DEFAULT '',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Races table
CREATE TABLE IF NOT EXISTS races (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    championship_id INTEGER NOT NULL,
    track_id INTEGER NOT NULL,
    season INTEGER NOT NULL,
    round_number INTEGER NOT NULL,
    race_date TEXT NOT NULL,
    weather_conditions TEXT DEFAULT 'dry',
    race_duration_minutes INTEGER NOT NULL,
    status TEXT DEFAULT 'scheduled' CHECK(status IN ('scheduled', 'completed', 'cancelled')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (championship_id) REFERENCES championships (id),
    FOREIGN KEY (track_id) REFERENCES tracks (id),
    UNIQUE(championship_id, season, round_number)
);

-- Race results table
CREATE TABLE IF NOT EXISTS race_results (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    race_id INTEGER NOT NULL,
    driver_id INTEGER NOT NULL,
    team_id INTEGER NOT NULL,
    position INTEGER NOT NULL,
    points INTEGER DEFAULT 0,
    fastest_lap BOOLEAN DEFAULT FALSE,
    dnf_reason TEXT,
    grid_position INTEGER DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (race_id) REFERENCES races (id),
    FOREIGN KEY (driver_id) REFERENCES drivers (id),
    FOREIGN KEY (team_id) REFERENCES teams (id),
    UNIQUE(race_id, driver_id)
);

-- Indexes for performance
CREATE INDEX IF NOT EXISTS idx_drivers_team ON drivers(current_team_id);
CREATE INDEX IF NOT EXISTS idx_teams_discipline ON teams(discipline);
CREATE INDEX IF NOT EXISTS idx_tracks_discipline ON tracks(discipline);
CREATE INDEX IF NOT EXISTS idx_races_championship_season ON races(championship_id, season);
CREATE INDEX IF NOT EXISTS idx_race_results_race ON race_results(race_id);
CREATE INDEX IF NOT EXISTS idx_race_results_driver ON race_results(driver_id);
"""