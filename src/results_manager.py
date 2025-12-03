

import sys
from pathlib import Path
from typing import List, Optional, Dict, Tuple
import csv
from collections import defaultdict

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

# C2 UPDATE LEAGUE RESULTS


from src.domain.league import League
from src.domain.team import Team
from src.domain.match import Match
from src.domain.table import LeagueTable


class ResultsManager:
    
    def __init__(self, league: Optional[League] = None):
        self.league = league
        self.table: Optional[LeagueTable] = None
        
        if league and league.teams:
            self.table = LeagueTable(league.teams)
    
    def set_league(self, league: League):
        self.league = league
        if league.teams:
            self.table = LeagueTable(league.teams)
    
    def record_result(self, match_identifier: str, home_score: int, away_score: int) -> tuple[bool, str]:
        if not self.league:
            return False, "No league set"
        
        if not self.table:
            return False, "League table not initialized"
        
        match = next((m for m in self.league.matches if m.match_id == match_identifier), None)
        
        if not match:
            return False, f"Match '{match_identifier}' not found"
        
        if match.played:
            return False, f"Match already played (score: {match.home_score}-{match.away_score})"
        
        if home_score < 0 or away_score < 0:
            return False, "Scores cannot be negative"
        
        try:
            match.record_result(home_score, away_score)
        except ValueError as e:
            return False, str(e)
        
        home_team = self.league.get_team_by_id(match.home_team_id)
        away_team = self.league.get_team_by_id(match.away_team_id)
        
        if not home_team or not away_team:
            return False, "Team not found in league"
        
        self.table.update_from_match(match, home_team, away_team)
        
        return True, f"Result recorded: {match.home_team_name} {home_score}-{away_score} {match.away_team_name}"
