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