"""
Member A (Mahir) - League & Team Management Module

Implements user stories A1-A9:
- A1: Create League
- A2: Add Team
- A3: Validate Duplicate Teams
- A4: Remove/Edit Team
- A5: Persist League & Team Data
- A6: Team Data Validation Rules
- A7: Load Existing League
- A8: Export League State
- A9: Validate League Configuration Before Scheduling
"""

import json
import os
from pathlib import Path
from typing import Optional
from datetime import datetime

# Import shared domain models
import sys
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from src.domain.league import League
from src.domain.team import Team


class LeagueManager:
    """
    League and Team Management Service (Member A - Mahir).
    Handles all operations related to league and team lifecycle.
    """
    
    def __init__(self, data_dir: str = "data"):
        """Initialize league manager with data directory."""
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(exist_ok=True)
        self.current_league: Optional[League] = None
    
    def create_league(self, name: str, season: str) -> tuple[bool, str, Optional[League]]:
        """
        A1: Create a new league with name and season.
        
        Args:
            name: League name
            season: Season identifier (e.g., "2024-2025")
        
        Returns:
            tuple: (success, message, league_object)
        """
        if not name or len(name.strip()) < 3:
            return False, "League name must be at least 3 characters", None
        
        if not season or len(season.strip()) < 4:
            return False, "Season must be specified (e.g., '2024-2025')", None
        
        self.current_league = League(name=name.strip(), season=season.strip())
        return True, f"League '{name}' created for season {season}", self.current_league
    
    def add_team(self, name: str, stadium: str) -> tuple[bool, str]:
        """
        A2: Add a team to the current league.
        A3: Duplicate validation is handled in League.add_team()
        A6: Validation rules applied in Team.validate()
        
        Args:
            name: Team name
            stadium: Stadium name
        
        Returns:
            tuple: (success, message)
        """
        if not self.current_league:
            return False, "No active league. Create a league first."
        
        team = Team(name=name.strip(), stadium=stadium.strip())
        return self.current_league.add_team(team)
    
    def remove_team(self, team_identifier: str) -> tuple[bool, str]:
        """
        A4: Remove a team from the league.
        
        Args:
            team_identifier: Team name or ID
        
        Returns:
            tuple: (success, message)
        """
        if not self.current_league:
            return False, "No active league"
        
        # Try to find by name first, then by ID
        team = self.current_league.get_team_by_name(team_identifier)
        if not team:
            team = self.current_league.get_team_by_id(team_identifier)
        
        if not team:
            return False, f"Team '{team_identifier}' not found"
        
        return self.current_league.remove_team(team.team_id)
    
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
    
    def save_league(self, filename: Optional[str] = None) -> tuple[bool, str]:
        """
        A5: Persist league and team data to JSON file.
        
        Args:
            filename: Custom filename (optional, auto-generated if not provided)
        
        Returns:
            tuple: (success, message)
        """
        if not self.current_league:
            return False, "No active league to save"
        
        if not filename:
            # Auto-generate filename from league name and season
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
    
    def load_league(self, filename: str) -> tuple[bool, str, Optional[League]]:
        """
        A7: Load a previously saved league from JSON file.
        
        Args:
            filename: Name of the file to load
        
        Returns:
            tuple: (success, message, league_object)
        """
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
        """
        A8: Export league data to a readable file.
        
        Args:
            format_type: Export format ('json' or 'txt')
            filename: Custom filename (optional)
        
        Returns:
            tuple: (success, message)
        """
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
    
    def validate_for_scheduling(self) -> tuple[bool, str]:
        """
        A9: Validate that league is ready for fixture generation.
        
        Returns:
            tuple: (is_valid, message)
        """
        if not self.current_league:
            return False, "No active league"
        
        return self.current_league.validate_for_scheduling()
    
    def list_teams(self) -> list[dict]:
        """
        Helper: Get list of all teams in the league.
        
        Returns:
            List of team dictionaries
        """
        if not self.current_league:
            return []
        
        return [team.to_dict() for team in self.current_league.teams]
    
    def get_league_summary(self) -> dict:
        """
        Helper: Get summary of current league.
        
        Returns:
            Dictionary with league summary
        """
        if not self.current_league:
            return {}
        
        return {
            "name": self.current_league.name,
            "season": self.current_league.season,
            "team_count": len(self.current_league.teams),
            "fixtures_generated": self.current_league.fixtures_generated,
            "total_matches": len(self.current_league.matches)
        }
