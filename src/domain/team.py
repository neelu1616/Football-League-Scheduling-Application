"""Team entity - shared across all member modules."""

from dataclasses import dataclass, field
from typing import Optional


@dataclass
class Team:
    """Represents a football team in the league."""
    
    name: str
    stadium: str
    team_id: Optional[str] = None
    
    # Statistics (managed by Member C)
    played: int = 0
    won: int = 0
    drawn: int = 0
    lost: int = 0
    goals_for: int = 0
    goals_against: int = 0
    points: int = 0
    
    def __post_init__(self):
        """Generate team_id if not provided."""
        if not self.team_id:
            self.team_id = self.name.lower().replace(" ", "_")
    
    @property
    def goal_difference(self) -> int:
        """Calculate goal difference."""
        return self.goals_for - self.goals_against
    
    def validate(self) -> tuple[bool, str]:
        """
        Validate team data according to A6 requirements.
        
        Returns:
            tuple: (is_valid, error_message)
        """
        if not self.name or len(self.name.strip()) < 2:
            return False, "Team name must be at least 2 characters"
        
        if len(self.name) > 50:
            return False, "Team name must not exceed 50 characters"
        
        if not self.stadium or len(self.stadium.strip()) < 2:
            return False, "Stadium name must be at least 2 characters"
        
        if len(self.stadium) > 100:
            return False, "Stadium name must not exceed 100 characters"
        
        return True, ""
    
    def to_dict(self) -> dict:
        """Convert team to dictionary for serialization."""
        return {
            "team_id": self.team_id,
            "name": self.name,
            "stadium": self.stadium,
            "played": self.played,
            "won": self.won,
            "drawn": self.drawn,
            "lost": self.lost,
            "goals_for": self.goals_for,
            "goals_against": self.goals_against,
            "points": self.points
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Team':
        """Create team from dictionary."""
        return cls(**data)
