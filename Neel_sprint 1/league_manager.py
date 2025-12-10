import json
import os
from pathlib import Path
from typing import Optional
from datetime import datetime


import sys
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from src.domain.league import League
from src.domain.team import Team


class LeagueManager:
    
    
    def __init__(self, data_dir: str = "data"):
       
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(exist_ok=True)
        self.current_league: Optional[League] = None
    
    def create_league(self, name: str, season: str) -> tuple[bool, str, Optional[League]]:
       
        if not name or len(name.strip()) < 3:
            return False, "League name must be at least 3 characters", None
        
        if not season or len(season.strip()) < 4:
            return False, "Season must be specified (e.g., '2024-2025')", None
        
        self.current_league = League(name=name.strip(), season=season.strip())
        return True, f"League '{name}' created for season {season}", self.current_league
    
    def add_team(self, name: str, stadium: str) -> tuple[bool, str]:
        
        if not self.current_league:
            return False, "No active league. Create a league first."
        
        team = Team(name=name.strip(), stadium=stadium.strip())
        return self.current_league.add_team(team)
    def edit_team(self, team_identifier: str, new_name: Optional[str] = None, 
                  new_stadium: Optional[str] = None) -> tuple[bool, str]:
        """
        A4: Edit team details.
        
        Args:
            team_identifier: Team name or ID
            new_name: New team name (optional)
            new_stadium: New stadium name (optional)
        
        Returns:
            tuple: (success, message)
        """
        if not self.current_league:
            return False, "No active league"
        
        team = self.current_league.get_team_by_name(team_identifier)
        if not team:
            team = self.current_league.get_team_by_id(team_identifier)
        
        if not team:
            return False, f"Team '{team_identifier}' not found"
        
        return self.current_league.edit_team(team.team_id, new_name, new_stadium)