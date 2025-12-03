"""
Member B (Mahir) - Scheduling Engine & Constraints Module

Implements user stories B1-B9:
- B1: Generate Round-Robin Fixtures
- B2: Generate Home/Away Rotation
- B3: Week-by-Week Schedule Generation
- B4: Prevent Same-Week Clashes
- B5: Reschedule a Match
- B6: Validate Fixture Integrity
- B7: View Full Fixture List
- B8: Team-Specific Fixture View
- B9: Auto-Regenerate Fixtures After Team Changes
"""

from typing import Optional
from datetime import datetime, timedelta

import sys
from pathlib import Path

# Add parent directory to path to enable imports
sys.path.insert(0, str(Path(__file__).parent.parent))

# Import from src directory
from src.domain.league import League
from src.domain.match import Match
from src.scheduling.scheduler import generate_round_robin_pairs, balance_home_away_rotation


class FixtureScheduler:
    """
    Fixture Scheduling Service (Member B - Abhishek).
    Handles fixture generation, validation, and rescheduling.
    """
    
    def __init__(self, league: Optional[League] = None):
        """Initialize scheduler with a league."""
        self.league = league
        self._rounds = []
        self._balanced_rounds = []
    
    def set_league(self, league: League):
        """Set the league for scheduling."""
        self.league = league
    
    def _validate_league(self) -> tuple[bool, str]:
        """
        Validate that league is ready for fixture generation.
        
        Returns:
            tuple: (is_valid, error_message)
        """
        if not self.league:
            return False, "No league set"
        
        if len(self.league.teams) < 2:
            return False, "League must have at least 2 teams"
        
        if len(self.league.teams) % 2 != 0:
            return False, "League must have even number of teams"
        
        return True, "League is valid"
    
    def generate_round_robin_fixtures(self) -> tuple[bool, str]:
        """
        B1: Generate Round-Robin Fixtures.
        Creates all match pairings using round-robin algorithm.
        Each team plays every other team exactly once.
        
        Returns:
            tuple: (success, message)
        """
        is_valid, error_msg = self._validate_league()
        if not is_valid:
            return False, error_msg
        
        # Clear existing fixtures
        self.league.matches = []
        
        # Generate round-robin pairs (B1 specific functionality)
        rounds = generate_round_robin_pairs(self.league.teams)
        
        # Store rounds temporarily for next stories
        self._rounds = rounds
        
        total_rounds = len(rounds)
        
        return True, f"B1 Complete: Generated {total_rounds} rounds of round-robin fixtures"
    
    