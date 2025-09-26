"""
Core race simulation engine using Monte Carlo methods.
Simulates race outcomes based on driver attributes, car performance, and track characteristics.
"""

import random
import numpy as np
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass
from ..database.models import Driver, Team, Track, Race, RaceResult
from ..config import MONTE_CARLO_ITERATIONS, RANDOM_SEED

@dataclass
class SimulationContext:
    """Context for a single race simulation"""
    race: Race
    track: Track
    drivers: List[Driver]
    teams: Dict[int, Team]  # team_id -> Team
    weather_factor: float = 1.0
    tire_degradation: float = 0.1

class RaceSimulator:
    """Monte Carlo race simulation engine"""
    
    def __init__(self, seed: int = RANDOM_SEED):
        self.rng = np.random.RandomState(seed)
        random.seed(seed)
    
    def simulate_race(self, context: SimulationContext) -> List[RaceResult]:
        """
        Simulate a complete race and return results.
        Uses Monte Carlo method to determine race outcome.
        """
        # Initialize race state
        race_state = self._initialize_race_state(context)
        
        # Run Monte Carlo simulation
        final_positions = self._run_monte_carlo_simulation(context, race_state)
        
        # Convert to race results
        results = self._generate_race_results(context, final_positions)
        
        return results
    
    def _initialize_race_state(self, context: SimulationContext) -> Dict:
        """Initialize the race state with starting grid and car performance"""
        state = {
            'grid_positions': {},  # driver_id -> grid_position
            'car_performance': {},  # driver_id -> performance_factor
            'driver_form': {},     # driver_id -> current_form_factor
        }
        
        # Calculate qualifying performance (simplified)
        qualifying_times = {}
        for driver in context.drivers:
            team = context.teams.get(driver.current_team_id)
            if not team:
                continue
                
            # Base qualifying time influenced by driver skill and team performance
            base_time = 100.0  # Base lap time in seconds
            driver_factor = (driver.skill * 0.4 + driver.consistency * 0.3 + driver.racecraft * 0.3)
            team_factor = self._calculate_team_performance(team)
            track_factor = 1.0 - (context.track.difficulty * driver.adaptability * 0.1)
            
            qualifying_time = base_time * (2.0 - driver_factor) * (2.0 - team_factor) * track_factor
            qualifying_times[driver.id] = qualifying_time
        
        # Sort by qualifying time to determine grid
        sorted_drivers = sorted(qualifying_times.items(), key=lambda x: x[1])
        for position, (driver_id, _) in enumerate(sorted_drivers, 1):
            state['grid_positions'][driver_id] = position
        
        # Calculate car performance factors
        for driver in context.drivers:
            team = context.teams.get(driver.current_team_id)
            if team:
                state['car_performance'][driver.id] = self._calculate_team_performance(team)
                state['driver_form'][driver.id] = self._calculate_driver_form(driver)
        
        return state
    
    def _run_monte_carlo_simulation(self, context: SimulationContext, race_state: Dict) -> Dict[int, int]:
        """Run Monte Carlo simulation to determine race outcome"""
        position_counts = {driver.id: [0] * len(context.drivers) for driver in context.drivers}
        
        for iteration in range(MONTE_CARLO_ITERATIONS):
            # Simulate one race iteration
            race_outcome = self._simulate_single_race_iteration(context, race_state)
            
            # Count positions
            for driver_id, position in race_outcome.items():
                if 1 <= position <= len(context.drivers):
                    position_counts[driver_id][position - 1] += 1
        
        # Determine most likely final positions
        final_positions = {}
        for driver_id in position_counts:
            # Find position with highest probability
            most_likely_position = np.argmax(position_counts[driver_id]) + 1
            final_positions[driver_id] = most_likely_position
        
        # Ensure no duplicate positions (resolve conflicts by driver skill)
        final_positions = self._resolve_position_conflicts(final_positions, context.drivers)
        
        return final_positions
    
    def _simulate_single_race_iteration(self, context: SimulationContext, race_state: Dict) -> Dict[int, int]:
        """Simulate a single race iteration"""
        race_performance = {}
        
        for driver in context.drivers:
            if driver.id not in race_state['car_performance']:
                continue
                
            # Calculate race performance
            base_performance = race_state['car_performance'][driver.id]
            driver_performance = race_state['driver_form'][driver.id]
            
            # Add randomness and various factors
            luck_factor = self.rng.normal(1.0, 0.1)  # Random events
            weather_impact = self._calculate_weather_impact(driver, context)
            track_suitability = self._calculate_track_suitability(driver, context.track)
            strategy_impact = self._simulate_strategy_impact(driver, context)
            
            # Combine all factors
            total_performance = (
                base_performance * 0.4 +
                driver_performance * 0.3 +
                weather_impact * 0.1 +
                track_suitability * 0.1 +
                strategy_impact * 0.1
            ) * luck_factor
            
            race_performance[driver.id] = total_performance
        
        # Sort by performance to get positions
        sorted_performance = sorted(race_performance.items(), key=lambda x: x[1], reverse=True)
        positions = {driver_id: position for position, (driver_id, _) in enumerate(sorted_performance, 1)}
        
        return positions
    
    def _calculate_team_performance(self, team: Team) -> float:
        """Calculate team performance factor based on budget and tier"""
        if team.tier == "tier1":
            base_performance = 0.8 + (team.budget / 400.0) * 0.2
        elif team.tier == "tier2":
            base_performance = 0.6 + (team.budget / 150.0) * 0.2
        else:  # tier3
            base_performance = 0.4 + (team.budget / 80.0) * 0.2
        
        return min(base_performance, 1.0)
    
    def _calculate_driver_form(self, driver: Driver) -> float:
        """Calculate current driver form with some randomness"""
        base_form = (driver.skill + driver.consistency + driver.racecraft) / 3.0
        form_variation = self.rng.normal(0, 0.05)  # Small random variation
        return max(0.1, min(1.0, base_form + form_variation))
    
    def _calculate_weather_impact(self, driver: Driver, context: SimulationContext) -> float:
        """Calculate weather impact on driver performance"""
        if context.weather_factor == 1.0:  # Dry conditions
            return 1.0
        
        # Wet weather favors adaptability and reduces aggression impact
        wet_skill = (driver.adaptability * 0.6 + driver.skill * 0.4)
        return 0.8 + (wet_skill * 0.2)
    
    def _calculate_track_suitability(self, driver: Driver, track: Track) -> float:
        """Calculate how well a driver suits the track"""
        # Technical tracks favor skill and racecraft
        # Power tracks favor aggression
        # Mixed surfaces favor adaptability
        
        if track.surface_type == "tarmac":
            suitability = (driver.skill * 0.5 + driver.racecraft * 0.3 + driver.consistency * 0.2)
        elif track.surface_type == "gravel":
            suitability = (driver.adaptability * 0.5 + driver.skill * 0.3 + driver.aggression * 0.2)
        else:  # mixed
            suitability = (driver.adaptability * 0.4 + driver.skill * 0.3 + driver.racecraft * 0.3)
        
        # Adjust for track difficulty
        difficulty_factor = 1.0 - (track.difficulty * (1.0 - driver.adaptability) * 0.2)
        
        return suitability * difficulty_factor
    
    def _simulate_strategy_impact(self, driver: Driver, context: SimulationContext) -> float:
        """Simulate impact of race strategy decisions"""
        # Simplified strategy simulation
        # In reality, this would involve pit stops, tire choices, etc.
        team = context.teams.get(driver.current_team_id)
        if not team:
            return 0.5
        
        # Better funded teams have better strategy
        strategy_quality = 0.5 + (self._calculate_team_performance(team) * 0.3)
        
        # Driver racecraft affects strategy execution
        execution_quality = driver.racecraft
        
        return (strategy_quality + execution_quality) / 2.0
    
    def _resolve_position_conflicts(self, positions: Dict[int, int], drivers: List[Driver]) -> Dict[int, int]:
        """Resolve conflicts where multiple drivers have the same position"""
        # Group drivers by position
        position_groups = {}
        for driver_id, position in positions.items():
            if position not in position_groups:
                position_groups[position] = []
            position_groups[position].append(driver_id)
        
        # Resolve conflicts
        final_positions = {}
        current_position = 1
        
        for position in sorted(position_groups.keys()):
            driver_ids = position_groups[position]
            
            if len(driver_ids) == 1:
                final_positions[driver_ids[0]] = current_position
                current_position += 1
            else:
                # Sort conflicted drivers by skill (tiebreaker)
                driver_skills = []
                for driver_id in driver_ids:
                    driver = next((d for d in drivers if d.id == driver_id), None)
                    if driver:
                        driver_skills.append((driver_id, driver.skill))
                
                # Assign positions based on skill
                driver_skills.sort(key=lambda x: x[1], reverse=True)
                for driver_id, _ in driver_skills:
                    final_positions[driver_id] = current_position
                    current_position += 1
        
        return final_positions
    
    def _generate_race_results(self, context: SimulationContext, final_positions: Dict[int, int]) -> List[RaceResult]:
        """Generate race results from final positions"""
        results = []
        points_system = [25, 18, 15, 12, 10, 8, 6, 4, 2, 1]  # F1-style points
        
        for driver in context.drivers:
            if driver.id not in final_positions:
                continue
                
            position = final_positions[driver.id]
            points = points_system[position - 1] if position <= len(points_system) else 0
            
            result = RaceResult(
                id=0,  # Will be set by database
                race_id=context.race.id,
                driver_id=driver.id,
                team_id=driver.current_team_id,
                position=position,
                points=points,
                fastest_lap=False,  # TODO: Implement fastest lap logic
                dnf_reason=None,
                grid_position=context.race_state.get('grid_positions', {}).get(driver.id, position)
            )
            results.append(result)
        
        # Assign fastest lap to someone in top 10
        if results:
            top_10 = [r for r in results if r.position <= 10]
            if top_10:
                fastest_lap_driver = random.choice(top_10)
                fastest_lap_driver.fastest_lap = True
                fastest_lap_driver.points += 1  # Bonus point for fastest lap
        
        return sorted(results, key=lambda x: x.position)