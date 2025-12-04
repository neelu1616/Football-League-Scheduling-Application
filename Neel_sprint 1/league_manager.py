
import json
import os
from pathlib import Path
from typing import Optional
from datetime import datetime


import sys
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from src.domain.league import League # pyright: ignore[reportMissingImports]
from src.domain.team import Team # pyright: ignore[reportMissingImports]


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