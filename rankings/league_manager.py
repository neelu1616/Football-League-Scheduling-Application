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
    
    MIN_TEAM_NAME_LENGTH = 2
    MAX_TEAM_NAME_LENGTH = 50
    MIN_STADIUM_NAME_LENGTH = 2
    MAX_STADIUM_NAME_LENGTH = 100
    
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
    
    def validate_team_data(self, name: str, stadium: str) -> tuple[bool, str]:
       
       
        if not name or len(name.strip()) < self.MIN_TEAM_NAME_LENGTH:
            return False, f"Team name must be at least {self.MIN_TEAM_NAME_LENGTH} characters"
        
        if len(name.strip()) > self.MAX_TEAM_NAME_LENGTH:
            return False, f"Team name must not exceed {self.MAX_TEAM_NAME_LENGTH} characters"
        
       
        if not stadium or len(stadium.strip()) < self.MIN_STADIUM_NAME_LENGTH:
            return False, f"Stadium name must be at least {self.MIN_STADIUM_NAME_LENGTH} characters"
        
        if len(stadium.strip()) > self.MAX_STADIUM_NAME_LENGTH:
            return False, f"Stadium name must not exceed {self.MAX_STADIUM_NAME_LENGTH} characters"
        
        return True, ""
    
    def add_team(self, name: str, stadium: str) -> tuple[bool, str]:
       
        if not self.current_league:
            return False, "No active league. Create a league first."
        
       
        is_valid, error_msg = self.validate_team_data(name, stadium)
        if not is_valid:
            return False, error_msg
        
        team = Team(name=name.strip(), stadium=stadium.strip())
        return self.current_league.add_team(team)
    def edit_team(self, team_identifier: str, new_name: Optional[str] = None, 
                  new_stadium: Optional[str] = None) -> tuple[bool, str]:
        
        if not self.current_league:
            return False, "No active league"
        
        team = self.current_league.get_team_by_name(team_identifier)
        if not team:
            team = self.current_league.get_team_by_id(team_identifier)
        
        if not team:
            return False, f"Team '{team_identifier}' not found"
        
       
        if new_name:
            is_valid, error_msg = self.validate_team_data(new_name, new_stadium or team.stadium)
            if not is_valid:
                return False, error_msg
        
        if new_stadium and not new_name:
            is_valid, error_msg = self.validate_team_data(team.name, new_stadium)
            if not is_valid:
                return False, error_msg
        
        return self.current_league.edit_team(team.team_id, new_name, new_stadium)
    
    def save_league(self, filename: Optional[str] = None) -> tuple[bool, str]:
        
        if not self.current_league:
            return False, "No active league to save"
        
        if not filename:
           
            safe_name = self.current_league.name.lower().replace(" ", "_")
            safe_season = self.current_league.season.replace("/", "-")
            filename = f"{safe_name}_{safe_season}.json"
        
        filepath = self.data_dir / filename
        
        try:
            data = self.current_league.to_dict()
            data["saved_at"] = datetime.now().isoformat()
            
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            
            return True, f"League saved to {filepath}"
        
        except Exception as e:
            return False, f"Failed to save league: {str(e)}"
        
    def add_team(self, name: str, stadium: str) -> tuple[bool, str]:
        
        if not self.current_league:
            return False, "No active league. Create a league first."
        
        team = Team(name=name.strip(), stadium=stadium.strip())
        return self.current_league.add_team(team)
    
    def load_league(self, filename: str) -> tuple[bool, str, Optional[League]]:
    
        filepath = self.data_dir / filename
        
        if not filepath.exists():
            return False, f"File not found: {filepath}", None
        
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            self.current_league = League.from_dict(data)
            
            return True, f"League '{self.current_league.name}' loaded successfully", self.current_league
        
        except Exception as e:
            return False, f"Failed to load league: {str(e)}", None
        
    def export_league(self, format_type: str = "json", filename: Optional[str] = None) -> tuple[bool, str]:
        
        if not self.current_league:
            return False, "No active league to export"
        
        if format_type == "json":
            return self.save_league(filename)
        
        elif format_type == "txt":
            if not filename:
                safe_name = self.current_league.name.lower().replace(" ", "_")
                filename = f"{safe_name}_export.txt"
            
            filepath = self.data_dir / filename
            
            try:
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(f"=" * 60 + "\n")
                    f.write(f"LEAGUE: {self.current_league.name}\n")
                    f.write(f"SEASON: {self.current_league.season}\n")
                    f.write(f"=" * 60 + "\n\n")
                    
                    f.write(f"TEAMS ({len(self.current_league.teams)}):\n")
                    f.write("-" * 60 + "\n")
                    
                    for idx, team in enumerate(self.current_league.teams, 1):
                        f.write(f"{idx}. {team.name}\n")
                        f.write(f"   Stadium: {team.stadium}\n")
                        f.write(f"   ID: {team.team_id}\n")
                        if team.played > 0:
                            f.write(f"   Record: {team.won}W-{team.drawn}D-{team.lost}L\n")
                            f.write(f"   Points: {team.points}\n")
                        f.write("\n")
                    
                    f.write("\n" + "=" * 60 + "\n")
                    f.write(f"Exported: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                
                return True, f"League exported to {filepath}"
            
            except Exception as e:
                return False, f"Failed to export league: {str(e)}"
        
        else:
            return False, f"Unsupported format: {format_type}"