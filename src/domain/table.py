"""League table and ranking logic - used by Member C."""

from typing import List, Tuple
from .team import Team
from .match import Match


class LeagueTable:
    """Manages league standings and rankings (C2, C3, C4)."""
    
    def __init__(self, teams: List[Team]):
        """Initialize table with teams."""
        self.teams = teams
    
    def update_from_match(self, match: Match, home_team: Team, away_team: Team):
        """
        Update team statistics from a match result (C2).
        
        Args:
            match: The played match
            home_team: Home team object
            away_team: Away team object
        """
        if not match.is_played:
            return
        
        home_team.played += 1
        away_team.played += 1
        
        home_team.goals_for += match.home_score
        home_team.goals_against += match.away_score
        away_team.goals_for += match.away_score
        away_team.goals_against += match.home_score
        
        # Determine result
        if match.home_score > match.away_score:
            # Home win
            home_team.won += 1
            home_team.points += 3
            away_team.lost += 1
        elif match.home_score < match.away_score:
            # Away win
            away_team.won += 1
            away_team.points += 3
            home_team.lost += 1
        else:
            # Draw
            home_team.drawn += 1
            away_team.drawn += 1
            home_team.points += 1
            away_team.points += 1
    
    def get_rankings(self) -> List[Team]:
        """
        Get teams sorted by ranking (C3, C4).
        
        Tie-breaking order:
        1. Points (descending)
        2. Goal difference (descending)
        3. Goals scored (descending)
        4. Alphabetical by name
        
        Returns:
            List of teams sorted by rank
        """
        return sorted(
            self.teams,
            key=lambda t: (
                -t.points,
                -t.goal_difference,
                -t.goals_for,
                t.name.lower()
            )
        )
    
    def get_table_data(self) -> List[dict]:
        """
        Get formatted table data (C4).
        
        Returns:
            List of dicts with ranking info
        """
        rankings = self.get_rankings()
        table = []
        
        for pos, team in enumerate(rankings, start=1):
            table.append({
                "position": pos,
                "team": team.name,
                "played": team.played,
                "won": team.won,
                "drawn": team.drawn,
                "lost": team.lost,
                "goals_for": team.goals_for,
                "goals_against": team.goals_against,
                "goal_difference": team.goal_difference,
                "points": team.points
            })
        
        return table
