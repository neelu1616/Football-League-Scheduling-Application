"""
Member C (Neel) - Ranking, Results & Presentation Module

Implements user stories C1-C9:
- C1: Record Match Result
- C2: Update League Table
- C3: Ranking Tie-Breaking Rules
- C4: Display League Table
- C5: Team Form & Performance Summary
- C6: Weekly Fixtures View
- C7: Basic UI Interface (CLI/Web)
- C8: Export Results/Standings
- C9: Head-to-Head Statistics Dashboard
"""

import sys
from pathlib import Path
from typing import List, Optional, Dict, Tuple
import csv
from collections import defaultdict

# Import shared domain models
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from src.domain.league import League
from src.domain.team import Team
from src.domain.match import Match
from src.domain.table import LeagueTable


class ResultsManager:
    """
    Results and Ranking Service (Member C - Neel).
    Handles match results, league table, and presentation.
    """
    
    def __init__(self, league: Optional[League] = None):
        """Initialize results manager with a league."""
        self.league = league
        self.table: Optional[LeagueTable] = None
        
        if league and league.teams:
            self.table = LeagueTable(league.teams)
    
    def set_league(self, league: League):
        """Set the league and initialize table."""
        self.league = league
        if league.teams:
            self.table = LeagueTable(league.teams)
    
    def record_result(self, match_identifier: str, home_score: int, away_score: int) -> tuple[bool, str]:
        """
        C1: Record a match result.
        C2: Automatically updates league table.
        
        Args:
            match_identifier: Match ID or description
            home_score: Home team score
            away_score: Away team score
        
        Returns:
            tuple: (success, message)
        """
        if not self.league:
            return False, "No league set"
        
        if not self.table:
            return False, "League table not initialized"
        
        # Find the match
        match = next((m for m in self.league.matches if m.match_id == match_identifier), None)
        
        if not match:
            return False, f"Match '{match_identifier}' not found"
        
        if match.played:
            return False, f"Match already played (score: {match.home_score}-{match.away_score})"
        
        # Validate scores
        if home_score < 0 or away_score < 0:
            return False, "Scores cannot be negative"
        
        # Record result
        try:
            match.record_result(home_score, away_score)
        except ValueError as e:
            return False, str(e)
        
        # C2: Update league table
        home_team = self.league.get_team_by_id(match.home_team_id)
        away_team = self.league.get_team_by_id(match.away_team_id)
        
        if not home_team or not away_team:
            return False, "Team not found in league"
        
        self.table.update_from_match(match, home_team, away_team)
        
        return True, f"Result recorded: {match.home_team_name} {home_score}-{away_score} {match.away_team_name}"
    
    def get_league_table(self) -> List[dict]:
        """
        C3 & C4: Get league table with tie-breaking applied.
        
        Returns:
            List of table rows (sorted by rank)
        """
        if not self.table:
            return []
        
        return self.table.get_table_data()
    
    def display_table(self) -> str:
        """
        C4: Display league table in formatted text.
        
        Returns:
            Formatted table string
        """
        if not self.table:
            return "No league table available"
        
        table_data = self.get_league_table()
        
        if not table_data:
            return "League table is empty"
        
        # Build formatted table
        lines = []
        lines.append("=" * 90)
        lines.append(f"LEAGUE TABLE - {self.league.name if self.league else 'Unknown'}")
        lines.append("=" * 90)
        
        header = f"{'Pos':<4} {'Team':<25} {'P':<3} {'W':<3} {'D':<3} {'L':<3} {'GF':<4} {'GA':<4} {'GD':<5} {'Pts':<4}"
        lines.append(header)
        lines.append("-" * 90)
        
        for row in table_data:
            line = (
                f"{row['position']:<4} "
                f"{row['team']:<25} "
                f"{row['played']:<3} "
                f"{row['won']:<3} "
                f"{row['drawn']:<3} "
                f"{row['lost']:<3} "
                f"{row['goals_for']:<4} "
                f"{row['goals_against']:<4} "
                f"{row['goal_difference']:+5} "
                f"{row['points']:<4}"
            )
            lines.append(line)
        
        lines.append("=" * 90)
        
        return "\n".join(lines)
    
    def get_team_form(self, team_identifier: str) -> dict:
        """
        C5: Get team form and performance summary.
        
        Args:
            team_identifier: Team name or ID
        
        Returns:
            Dictionary with performance stats
        """
        if not self.league:
            return {}
        
        team = self.league.get_team_by_name(team_identifier)
        if not team:
            team = self.league.get_team_by_id(team_identifier)
        
        if not team:
            return {}
        
        # Get last 5 results
        recent_matches = []
        form = []
        
        for match in self.league.matches:
            if not match.is_played:
                continue
            
            if match.home_team_id == team.team_id:
                recent_matches.append(match)
                if match.home_score > match.away_score:
                    form.append('W')
                elif match.home_score < match.away_score:
                    form.append('L')
                else:
                    form.append('D')
            
            elif match.away_team_id == team.team_id:
                recent_matches.append(match)
                if match.away_score > match.home_score:
                    form.append('W')
                elif match.away_score < match.home_score:
                    form.append('L')
                else:
                    form.append('D')
        
        # Get last 5
        form = form[-5:] if len(form) > 5 else form
        
        return {
            "team": team.name,
            "played": team.played,
            "won": team.won,
            "drawn": team.drawn,
            "lost": team.lost,
            "goals_for": team.goals_for,
            "goals_against": team.goals_against,
            "goal_difference": team.goal_difference,
            "points": team.points,
            "form": "".join(form),
            "win_percentage": (team.won / team.played * 100) if team.played > 0 else 0
        }
    
    def get_weekly_fixtures(self, week: Optional[int] = None) -> Dict[int, List[dict]]:
        """
        C6: View fixtures grouped by week.
        
        Args:
            week: Specific week number (optional, returns all if None)
        
        Returns:
            Dictionary mapping week number to list of fixtures
        """
        if not self.league:
            return {}
        
        fixtures_by_week = defaultdict(list)
        
        for match in self.league.matches:
            if week is None or match.week == week:
                fixtures_by_week[match.week].append(match.to_dict())
        
        return dict(fixtures_by_week)
    
    def export_standings(self, filepath: str, format_type: str = "csv") -> tuple[bool, str]:
        """
        C8: Export final standings to a file.
        
        Args:
            filepath: Output file path
            format_type: Export format ('csv' or 'txt')
        
        Returns:
            tuple: (success, message)
        """
        if not self.table:
            return False, "No league table available"
        
        table_data = self.get_league_table()
        
        if not table_data:
            return False, "League table is empty"
        
        try:
            if format_type == "csv":
                with open(filepath, 'w', newline='', encoding='utf-8') as f:
                    fieldnames = ['position', 'team', 'played', 'won', 'drawn', 'lost',
                                  'goals_for', 'goals_against', 'goal_difference', 'points']
                    writer = csv.DictWriter(f, fieldnames=fieldnames)
                    writer.writeheader()
                    writer.writerows(table_data)
                
                return True, f"Standings exported to {filepath}"
            
            elif format_type == "txt":
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(self.display_table())
                
                return True, f"Standings exported to {filepath}"
            
            else:
                return False, f"Unsupported format: {format_type}"
        
        except Exception as e:
            return False, f"Export failed: {str(e)}"
    
    def get_head_to_head(self, team1_identifier: str, team2_identifier: str) -> dict:
        """
        C9: Get head-to-head statistics between two teams.
        
        Args:
            team1_identifier: First team name or ID
            team2_identifier: Second team name or ID
        
        Returns:
            Dictionary with head-to-head stats
        """
        if not self.league:
            return {}
        
        team1 = self.league.get_team_by_name(team1_identifier)
        if not team1:
            team1 = self.league.get_team_by_id(team1_identifier)
        
        team2 = self.league.get_team_by_name(team2_identifier)
        if not team2:
            team2 = self.league.get_team_by_id(team2_identifier)
        
        if not team1 or not team2:
            return {}
        
        # Find all matches between these teams
        h2h_matches = []
        team1_wins = 0
        team2_wins = 0
        draws = 0
        team1_goals = 0
        team2_goals = 0
        
        for match in self.league.matches:
            if not match.is_played:
                continue
            
            is_h2h = False
            team1_score = 0
            team2_score = 0
            
            if match.home_team_id == team1.team_id and match.away_team_id == team2.team_id:
                is_h2h = True
                team1_score = match.home_score
                team2_score = match.away_score
            elif match.home_team_id == team2.team_id and match.away_team_id == team1.team_id:
                is_h2h = True
                team1_score = match.away_score
                team2_score = match.home_score
            
            if is_h2h:
                h2h_matches.append({
                    "week": match.week,
                    "home": match.home_team_name,
                    "away": match.away_team_name,
                    "score": f"{match.home_score}-{match.away_score}"
                })
                
                team1_goals += team1_score
                team2_goals += team2_score
                
                if team1_score > team2_score:
                    team1_wins += 1
                elif team2_score > team1_score:
                    team2_wins += 1
                else:
                    draws += 1
        
        return {
            "team1": team1.name,
            "team2": team2.name,
            "matches_played": len(h2h_matches),
            "team1_wins": team1_wins,
            "team2_wins": team2_wins,
            "draws": draws,
            "team1_goals": team1_goals,
            "team2_goals": team2_goals,
            "matches": h2h_matches
        }
    
    def display_head_to_head(self, team1_identifier: str, team2_identifier: str) -> str:
        """
        C9: Display head-to-head statistics in formatted text.
        
        Args:
            team1_identifier: First team name or ID
            team2_identifier: Second team name or ID
        
        Returns:
            Formatted head-to-head string
        """
        h2h = self.get_head_to_head(team1_identifier, team2_identifier)
        
        if not h2h:
            return "No head-to-head data available"
        
        lines = []
        lines.append("=" * 70)
        lines.append(f"HEAD-TO-HEAD: {h2h['team1']} vs {h2h['team2']}")
        lines.append("=" * 70)
        lines.append(f"Matches Played: {h2h['matches_played']}")
        lines.append("")
        lines.append(f"{h2h['team1']} wins: {h2h['team1_wins']}")
        lines.append(f"{h2h['team2']} wins: {h2h['team2_wins']}")
        lines.append(f"Draws: {h2h['draws']}")
        lines.append("")
        lines.append(f"Goals: {h2h['team1']} {h2h['team1_goals']} - {h2h['team2_goals']} {h2h['team2']}")
        lines.append("")
        
        if h2h['matches']:
            lines.append("Match History:")
            lines.append("-" * 70)
            for match in h2h['matches']:
                lines.append(f"Week {match['week']}: {match['home']} vs {match['away']} ({match['score']})")
        
        lines.append("=" * 70)
        
        return "\n".join(lines)
