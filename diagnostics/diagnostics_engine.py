"""
Member D (Dhawal) - Diagnostics, Analytics & Testing Module

Implements user stories D1-D9:
- D1: Detect Scheduling Anomalies
- D2: Analyse Team Workload Distribution  
- D3: Identify Fixture Congestion Zones
- D4: Pre-Match Rule Compliance Checker
- D5: Predict Outcome Trends Using Basic Statistical Indicators
- D6: Generate End-of-Season Summary Report
- D7: Automated Boundary & Partition Test Generator
- D8: Coverage-Aware Test Harness
- D9: Symbolic Path Discovery Helper
"""

import sys
from pathlib import Path
from typing import List, Dict, Optional, Set, Tuple, Any
import json
from datetime import datetime, timedelta
import subprocess
import ast
import inspect
import random
import math
from collections import defaultdict
from dataclasses import dataclass

# Import shared domain models
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.domain.league import League
from src.domain.team import Team
from src.domain.match import Match


@dataclass
class StadiumLocation:
    """Fictional stadium coordinates for travel burden calculations."""
    team_id: str
    team_name: str
    latitude: float
    longitude: float


@dataclass
class SchedulingAnomaly:
    """Represents a detected scheduling anomaly."""
    anomaly_type: str
    severity: str  # 'critical', 'warning', 'info'
    description: str
    affected_matches: List[str]
    details: Dict[str, Any]


@dataclass
class WorkloadMetrics:
    """Team workload analysis metrics."""
    team_id: str
    team_name: str
    total_distance: float
    average_distance_per_match: float
    consecutive_away_games: int
    max_consecutive_away: int
    match_congestion_score: float
    rest_days_avg: float


@dataclass
class CongestionZone:
    """Represents a period of fixture congestion."""
    week_start: int
    week_end: int
    affected_teams: List[str]
    match_density: float
    severity: str


@dataclass
class RuleViolation:
    """Represents a rule compliance violation."""
    rule_name: str
    severity: str
    description: str
    affected_entities: List[str]
    suggestion: str


@dataclass
class TrendPrediction:
    """Statistical trend prediction for a team."""
    team_id: str
    team_name: str
    current_form: str  # 'excellent', 'good', 'average', 'poor'
    win_probability: float
    expected_points_next_5: float
    momentum_score: float
    trend_direction: str  # 'up', 'stable', 'down'


@dataclass
class SeasonHighlight:
    """Individual highlight from the season."""
    category: str
    description: str
    value: Any
    match_id: Optional[str] = None


class DiagnosticsEngine:
    """
    Diagnostics, Analytics and Testing Service (Member D - Dhawal).
    Handles fixture diagnostics, workload analysis, rule checking, and test generation.
    """
    
    def __init__(self, data_dir: str = "data/diagnostics"):
        """Initialize diagnostics engine."""
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)
        
        # Fictional stadium locations for travel calculations
        self.stadium_locations: Dict[str, StadiumLocation] = {}
    
    def _calculate_distance(self, loc1: StadiumLocation, loc2: StadiumLocation) -> float:
        """
        Calculate distance between two stadium locations using Haversine formula.
        
        Args:
            loc1: First stadium location
            loc2: Second stadium location
        
        Returns:
            Distance in kilometers
        """
        # Haversine formula
        R = 6371  # Earth radius in km
        
        lat1_rad = math.radians(loc1.latitude)
        lat2_rad = math.radians(loc2.latitude)
        delta_lat = math.radians(loc2.latitude - loc1.latitude)
        delta_lon = math.radians(loc2.longitude - loc1.longitude)
        
        a = math.sin(delta_lat/2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(delta_lon/2)**2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
        
        return R * c
    
    def _generate_stadium_locations(self, teams: List[Team]) -> None:
        """
        Generate fictional stadium coordinates for teams.
        Distributes teams across a fictional geographic area.
        """
        # Use deterministic random for consistency
        random.seed(42)
        
        # Generate locations in a 500km x 500km area
        base_lat, base_lon = 51.5074, -0.1278  # London as center
        
        for team in teams:
            # Spread teams within ~250km radius
            offset_lat = random.uniform(-2.5, 2.5)
            offset_lon = random.uniform(-2.5, 2.5)
            
            self.stadium_locations[team.team_id] = StadiumLocation(
                team_id=team.team_id,
                team_name=team.name,
                latitude=base_lat + offset_lat,
                longitude=base_lon + offset_lon
            )
    
    def detect_scheduling_anomalies(self, league: League, save_results: bool = True) -> List[SchedulingAnomaly]:
        """
        D1: Detect scheduling anomalies such as duplicate matches, mismatched rounds,
        or invalid team references.
        
        This function has high cyclomatic complexity (CC > 10) due to multiple
        anomaly detection branches.
        
        Args:
            league: League object with teams and matches
            save_results: Whether to save results to file
        
        Returns:
            List of detected anomalies
        """
        anomalies: List[SchedulingAnomaly] = []
        match_signatures: Set[str] = set()
        
        # Check 1: Duplicate matches
        for match in league.matches:
            signature = f"{min(match.home_team_id, match.away_team_id)}-{max(match.home_team_id, match.away_team_id)}-{match.week}"
            if signature in match_signatures:
                anomalies.append(SchedulingAnomaly(
                    anomaly_type="duplicate_match",
                    severity="critical",
                    description=f"Duplicate match found in week {match.week}",
                    affected_matches=[match.match_id],
                    details={
                        "home": match.home_team_name,
                        "away": match.away_team_name,
                        "week": match.week
                    }
                ))
            match_signatures.add(signature)
        
        # Check 2: Invalid team references
        valid_team_ids = {team.team_id for team in league.teams}
        for match in league.matches:
            if match.home_team_id not in valid_team_ids:
                anomalies.append(SchedulingAnomaly(
                    anomaly_type="invalid_team_reference",
                    severity="critical",
                    description=f"Home team '{match.home_team_id}' not found in league",
                    affected_matches=[match.match_id],
                    details={"team_id": match.home_team_id, "role": "home"}
                ))
            
            if match.away_team_id not in valid_team_ids:
                anomalies.append(SchedulingAnomaly(
                    anomaly_type="invalid_team_reference",
                    severity="critical",
                    description=f"Away team '{match.away_team_id}' not found in league",
                    affected_matches=[match.match_id],
                    details={"team_id": match.away_team_id, "role": "away"}
                ))
        
        # Check 3: Team playing itself
        for match in league.matches:
            if match.home_team_id == match.away_team_id:
                anomalies.append(SchedulingAnomaly(
                    anomaly_type="self_match",
                    severity="critical",
                    description=f"Team cannot play against itself",
                    affected_matches=[match.match_id],
                    details={"team_id": match.home_team_id}
                ))
        
        # Check 4: Mismatched rounds - incomplete weeks
        matches_by_week: Dict[int, List[Match]] = defaultdict(list)
        for match in league.matches:
            matches_by_week[match.week].append(match)
        
        num_teams = len(league.teams)
        expected_matches_per_week = num_teams // 2 if num_teams % 2 == 0 else (num_teams // 2) + 1
        
        for week, week_matches in matches_by_week.items():
            if len(week_matches) != expected_matches_per_week:
                anomalies.append(SchedulingAnomaly(
                    anomaly_type="incomplete_round",
                    severity="warning",
                    description=f"Week {week} has {len(week_matches)} matches, expected {expected_matches_per_week}",
                    affected_matches=[m.match_id for m in week_matches],
                    details={
                        "week": week,
                        "actual_count": len(week_matches),
                        "expected_count": expected_matches_per_week
                    }
                ))
        
        # Check 5: Multiple matches for same team in one week
        for week, week_matches in matches_by_week.items():
            team_appearances: Dict[str, int] = defaultdict(int)
            for match in week_matches:
                team_appearances[match.home_team_id] += 1
                team_appearances[match.away_team_id] += 1
            
            for team_id, count in team_appearances.items():
                if count > 1:
                    team = league.get_team_by_id(team_id)
                    team_name = team.name if team else team_id
                    anomalies.append(SchedulingAnomaly(
                        anomaly_type="multiple_matches_per_week",
                        severity="critical",
                        description=f"Team '{team_name}' has {count} matches in week {week}",
                        affected_matches=[m.match_id for m in week_matches if m.home_team_id == team_id or m.away_team_id == team_id],
                        details={
                            "team_id": team_id,
                            "team_name": team_name,
                            "week": week,
                            "count": count
                        }
                    ))
        
        # Check 6: Home/Away balance - ensure teams play each other once home and once away
        if len(league.teams) >= 2:
            for i, team1 in enumerate(league.teams):
                for team2 in league.teams[i+1:]:
                    home_matches = [m for m in league.matches if m.home_team_id == team1.team_id and m.away_team_id == team2.team_id]
                    away_matches = [m for m in league.matches if m.home_team_id == team2.team_id and m.away_team_id == team1.team_id]
                    
                    total_matches = len(home_matches) + len(away_matches)
                    
                    if total_matches == 0:
                        anomalies.append(SchedulingAnomaly(
                            anomaly_type="missing_fixture",
                            severity="warning",
                            description=f"No fixture between {team1.name} and {team2.name}",
                            affected_matches=[],
                            details={
                                "team1": team1.name,
                                "team2": team2.name
                            }
                        ))
                    elif total_matches > 2:
                        anomalies.append(SchedulingAnomaly(
                            anomaly_type="excessive_fixtures",
                            severity="warning",
                            description=f"More than 2 fixtures between {team1.name} and {team2.name}",
                            affected_matches=[m.match_id for m in home_matches + away_matches],
                            details={
                                "team1": team1.name,
                                "team2": team2.name,
                                "count": total_matches
                            }
                        ))
        
        # Check 7: Invalid week numbers
        if league.matches:
            max_week = max(m.week for m in league.matches)
            min_week = min(m.week for m in league.matches)
            
            if min_week < 1:
                anomalies.append(SchedulingAnomaly(
                    anomaly_type="invalid_week_number",
                    severity="critical",
                    description=f"Week numbers cannot be less than 1 (found: {min_week})",
                    affected_matches=[m.match_id for m in league.matches if m.week < 1],
                    details={"min_week": min_week}
                ))
            
            # Check for gaps in week sequence
            expected_weeks = set(range(1, max_week + 1))
            actual_weeks = {m.week for m in league.matches}
            missing_weeks = expected_weeks - actual_weeks
            
            if missing_weeks:
                anomalies.append(SchedulingAnomaly(
                    anomaly_type="week_sequence_gap",
                    severity="info",
                    description=f"Missing weeks in sequence: {sorted(missing_weeks)}",
                    affected_matches=[],
                    details={"missing_weeks": sorted(missing_weeks)}
                ))
        
        if save_results:
            result = {
                "league_name": league.name,
                "season": league.season,
                "total_anomalies": len(anomalies),
                "critical": len([a for a in anomalies if a.severity == "critical"]),
                "warnings": len([a for a in anomalies if a.severity == "warning"]),
                "info": len([a for a in anomalies if a.severity == "info"]),
                "anomalies": [
                    {
                        "type": a.anomaly_type,
                        "severity": a.severity,
                        "description": a.description,
                        "affected_matches": a.affected_matches,
                        "details": a.details
                    } for a in anomalies
                ],
                "analyzed_at": datetime.now().isoformat()
            }
            
            filepath = self.data_dir / f"anomalies_{league.name.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            with open(filepath, 'w') as f:
                json.dump(result, f, indent=2)
        
        return anomalies
    
    def analyse_team_workload(self, league: League, save_results: bool = True) -> List[WorkloadMetrics]:
        """
        D2: Analyse team workload distribution including travel burden, consecutive
        away games, and match congestion.
        
        Uses fictional stadium coordinates to simulate travel distances.
        Has high cyclomatic complexity (CC > 10) due to multiple metrics calculations.
        
        Args:
            league: League object with teams and matches
            save_results: Whether to save results to file
        
        Returns:
            List of workload metrics for each team
        """
        # Generate stadium locations if not already done
        if not self.stadium_locations:
            self._generate_stadium_locations(league.teams)
        
        workload_metrics: List[WorkloadMetrics] = []
        
        for team in league.teams:
            # Get all matches for this team
            team_matches = [m for m in league.matches if m.home_team_id == team.team_id or m.away_team_id == team.team_id]
            team_matches.sort(key=lambda m: m.week)
            
            if not team_matches:
                continue
            
            # Calculate travel burden
            total_distance = 0.0
            for match in team_matches:
                if match.away_team_id == team.team_id:
                    # Away game - team travels to opponent's stadium
                    opponent_id = match.home_team_id
                    if team.team_id in self.stadium_locations and opponent_id in self.stadium_locations:
                        distance = self._calculate_distance(
                            self.stadium_locations[team.team_id],
                            self.stadium_locations[opponent_id]
                        )
                        total_distance += distance * 2  # Round trip
            
            avg_distance = total_distance / len(team_matches) if team_matches else 0.0
            
            # Count consecutive away games
            consecutive_away = 0
            max_consecutive_away = 0
            current_streak = 0
            
            for match in team_matches:
                if match.away_team_id == team.team_id:
                    current_streak += 1
                    max_consecutive_away = max(max_consecutive_away, current_streak)
                else:
                    current_streak = 0
            
            consecutive_away = max_consecutive_away
            
            # Calculate match congestion score
            # Higher score = more congested schedule
            weeks_with_matches = {m.week for m in team_matches}
            if len(weeks_with_matches) > 1:
                week_span = max(weeks_with_matches) - min(weeks_with_matches) + 1
                congestion_score = len(team_matches) / week_span
            else:
                congestion_score = float(len(team_matches))
            
            # Calculate average rest days
            rest_days_list: List[int] = []
            for i in range(len(team_matches) - 1):
                rest_days = (team_matches[i+1].week - team_matches[i].week - 1) * 7
                rest_days_list.append(rest_days)
            
            avg_rest_days = sum(rest_days_list) / len(rest_days_list) if rest_days_list else 0.0
            
            workload_metrics.append(WorkloadMetrics(
                team_id=team.team_id,
                team_name=team.name,
                total_distance=round(total_distance, 2),
                average_distance_per_match=round(avg_distance, 2),
                consecutive_away_games=consecutive_away,
                max_consecutive_away=max_consecutive_away,
                match_congestion_score=round(congestion_score, 3),
                rest_days_avg=round(avg_rest_days, 1)
            ))
        
        if save_results:
            result = {
                "league_name": league.name,
                "season": league.season,
                "workload_analysis": [
                    {
                        "team_id": wm.team_id,
                        "team_name": wm.team_name,
                        "total_travel_km": wm.total_distance,
                        "avg_travel_per_match_km": wm.average_distance_per_match,
                        "max_consecutive_away": wm.max_consecutive_away,
                        "match_congestion_score": wm.match_congestion_score,
                        "avg_rest_days": wm.rest_days_avg
                    } for wm in workload_metrics
                ],
                "analyzed_at": datetime.now().isoformat()
            }
            
            filepath = self.data_dir / f"workload_{league.name.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            with open(filepath, 'w') as f:
                json.dump(result, f, indent=2)
        
        return workload_metrics
    

    def identify_fixture_congestion(self, league: League, congestion_threshold: int = 3,
                                   save_results: bool = True) -> List[CongestionZone]:
        """
        D3: Identify fixture congestion zones - weeks where teams have tightly
        packed schedules.
        
        Args:
            league: League object with teams and matches
            congestion_threshold: Number of matches in a window to flag congestion
            save_results: Whether to save results to file
        
        Returns:
            List of congestion zones
        """
        congestion_zones: List[CongestionZone] = []
        
        # Analyze each team's schedule
        for team in league.teams:
            team_matches = sorted([m for m in league.matches if m.home_team_id == team.team_id or m.away_team_id == team.team_id],
                                key=lambda m: m.week)
            
            if len(team_matches) < congestion_threshold:
                continue
            
            # Use sliding window to find congested periods
            window_size = 3  # Check 3-week windows
            
            for i in range(len(team_matches) - congestion_threshold + 1):
                window_matches = team_matches[i:i+congestion_threshold]
                
                if len(window_matches) < congestion_threshold:
                    continue
                
                week_start = window_matches[0].week
                week_end = window_matches[-1].week
                week_span = week_end - week_start + 1
                
                # If 3+ matches within 3 weeks, it's congested
                if week_span <= window_size:
                    match_density = len(window_matches) / week_span
                    
                    # Determine severity
                    if match_density >= 2.0:
                        severity = "high"
                    elif match_density >= 1.5:
                        severity = "medium"
                    else:
                        severity = "low"
                    
                    # Check if this zone already exists
                    existing = next((cz for cz in congestion_zones 
                                   if cz.week_start == week_start and cz.week_end == week_end
                                   and team.team_id in cz.affected_teams), None)
                    
                    if not existing:
                        congestion_zones.append(CongestionZone(
                            week_start=week_start,
                            week_end=week_end,
                            affected_teams=[team.team_id],
                            match_density=round(match_density, 2),
                            severity=severity
                        ))
                    elif team.team_id not in existing.affected_teams:
                        existing.affected_teams.append(team.team_id)
        
        if save_results:
            result = {
                "league_name": league.name,
                "season": league.season,
                "congestion_threshold": congestion_threshold,
                "total_zones": len(congestion_zones),
                "congestion_zones": [
                    {
                        "weeks": f"{cz.week_start}-{cz.week_end}",
                        "affected_teams": [league.get_team_by_id(tid).name if league.get_team_by_id(tid) else tid 
                                         for tid in cz.affected_teams],
                        "match_density": cz.match_density,
                        "severity": cz.severity
                    } for cz in congestion_zones
                ],
                "analyzed_at": datetime.now().isoformat()
            }
            
            filepath = self.data_dir / f"congestion_{league.name.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            with open(filepath, 'w') as f:
                json.dump(result, f, indent=2)
        
        return congestion_zones