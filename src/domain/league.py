"""League entity - orchestrates teams, matches, and table (integration point)."""

from typing import List, Optional, Dict
from dataclasses import dataclass, field
from .team import Team
from .match import Match


@dataclass
class League:
    """Central league entity managing teams, fixtures, and standings."""
    
    name: str
    season: str
    teams: List[Team] = field(default_factory=list)
    matches: List[Match] = field(default_factory=list)
    fixtures_generated: bool = False
    
    def add_team(self, team: Team) -> tuple[bool, str]:
        """
        Add a team to the league (A2).
        
        Returns:
            tuple: (success, message)
        """
        # A3: Validate duplicate teams
        if any(t.team_id == team.team_id for t in self.teams):
            return False, f"Team '{team.name}' already exists in the league"
        
        if any(t.name.lower() == team.name.lower() for t in self.teams):
            return False, f"A team with name '{team.name}' already exists"
        
        # A6: Validate team data
        is_valid, error_msg = team.validate()
        if not is_valid:
            return False, error_msg
        
        self.teams.append(team)
        return True, f"Team '{team.name}' added successfully"
    
    def remove_team(self, team_id: str) -> tuple[bool, str]:
        """
        Remove a team from the league (A4).
        
        Returns:
            tuple: (success, message)
        """
        if self.fixtures_generated:
            return False, "Cannot remove teams after fixtures are generated"
        
        team = self.get_team_by_id(team_id)
        if not team:
            return False, f"Team with ID '{team_id}' not found"
        
        self.teams = [t for t in self.teams if t.team_id != team_id]
        return True, f"Team removed successfully"
    
    def edit_team(self, team_id: str, name: Optional[str] = None, 
                  stadium: Optional[str] = None) -> tuple[bool, str]:
        """
        Edit team details (A4).
        
        Returns:
            tuple: (success, message)
        """
        if self.fixtures_generated:
            return False, "Cannot edit teams after fixtures are generated"
        
        team = self.get_team_by_id(team_id)
        if not team:
            return False, f"Team with ID '{team_id}' not found"
        
        if name:
            team.name = name
        if stadium:
            team.stadium = stadium
        
        # Re-validate
        is_valid, error_msg = team.validate()
        if not is_valid:
            return False, error_msg
        
        return True, "Team updated successfully"
    
    def get_team_by_id(self, team_id: str) -> Optional[Team]:
        """Find team by ID."""
        return next((t for t in self.teams if t.team_id == team_id), None)
    
    def get_team_by_name(self, name: str) -> Optional[Team]:
        """Find team by name."""
        return next((t for t in self.teams if t.name.lower() == name.lower()), None)
    
    def validate_for_scheduling(self) -> tuple[bool, str]:
        """
        A9: Validate league is ready for fixture generation.
        
        Returns:
            tuple: (is_valid, error_message)
        """
        if len(self.teams) < 2:
            return False, "League must have at least 2 teams to generate fixtures"
        
        if len(self.teams) % 2 != 0:
            return False, "League must have an even number of teams for round-robin scheduling"
        
        for team in self.teams:
            is_valid, error_msg = team.validate()
            if not is_valid:
                return False, f"Team '{team.name}' validation failed: {error_msg}"
        
        return True, "League is valid for scheduling"
    
    def to_dict(self) -> dict:
        """Convert league to dictionary for serialization (A5, A8)."""
        return {
            "name": self.name,
            "season": self.season,
            "teams": [team.to_dict() for team in self.teams],
            "matches": [match.to_dict() for match in self.matches],
            "fixtures_generated": self.fixtures_generated
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'League':
        """Create league from dictionary (A7)."""
        league = cls(
            name=data["name"],
            season=data["season"],
            fixtures_generated=data.get("fixtures_generated", False)
        )
        league.teams = [Team.from_dict(t) for t in data.get("teams", [])]
        league.matches = [Match.from_dict(m) for m in data.get("matches", [])]
        return league
