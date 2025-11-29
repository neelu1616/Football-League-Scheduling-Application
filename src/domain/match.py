"""Match entity - shared across all member modules."""

from dataclasses import dataclass
from typing import Optional
from datetime import datetime


@dataclass
class Match:
    """Represents a single match in the league."""
    
    match_id: str
    home_team_id: str
    away_team_id: str
    week: int
    home_team_name: str = ""
    away_team_name: str = ""
    home_score: Optional[int] = None
    away_score: Optional[int] = None
    played: bool = False
    scheduled_date: Optional[str] = None
    
    @property
    def is_played(self) -> bool:
        """Check if match has been played."""
        return self.played and self.home_score is not None and self.away_score is not None
    
    def record_result(self, home_score: int, away_score: int):
        """Record match result (C1 requirement)."""
        if home_score < 0 or away_score < 0:
            raise ValueError("Scores cannot be negative")
        
        self.home_score = home_score
        self.away_score = away_score
        self.played = True
    
    def to_dict(self) -> dict:
        """Convert match to dictionary for serialization."""
        return {
            "match_id": self.match_id,
            "home_team_id": self.home_team_id,
            "away_team_id": self.away_team_id,
            "home_team_name": self.home_team_name,
            "away_team_name": self.away_team_name,
            "week": self.week,
            "home_score": self.home_score,
            "away_score": self.away_score,
            "played": self.played,
            "scheduled_date": self.scheduled_date
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Match':
        """Create match from dictionary."""
        return cls(**data)
    
    def __str__(self) -> str:
        """String representation of match."""
        if self.is_played:
            return f"Week {self.week}: {self.home_team_name} {self.home_score}-{self.away_score} {self.away_team_name}"
        else:
            return f"Week {self.week}: {self.home_team_name} vs {self.away_team_name}"
