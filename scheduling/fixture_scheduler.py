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
    
    def apply_home_away_rotation(self) -> tuple[bool, str]:
        """
        B2: Generate Home/Away Rotation.
        Balances home and away fixtures to ensure fairness.
        Each team gets balanced home and away matches.
        
        Returns:
            tuple: (success, message)
        """
        if not hasattr(self, '_rounds') or not self._rounds:
            return False, "Must generate round-robin fixtures first (B1)"
        
        # Balance home/away rotation (B2 specific functionality)
        balanced_rounds = balance_home_away_rotation(self._rounds)
        
        # Store balanced rounds for next story
        self._balanced_rounds = balanced_rounds
        
        total_rounds = len(balanced_rounds)
        
        return True, f"B2 Complete: Applied home/away rotation across {total_rounds} rounds"
    
    def organize_fixtures_by_week(self, start_date: Optional[str] = None) -> tuple[bool, str]:
        """
        B3: Week-by-Week Schedule Generation.
        Organizes fixtures into weekly schedules with dates.
        Ensures one match per team per week (B4 requirement).
        
        Args:
            start_date: Starting date for fixtures (format: YYYY-MM-DD)
        
        Returns:
            tuple: (success, message)
        """
        if not hasattr(self, '_balanced_rounds') or not self._balanced_rounds:
            return False, "Must apply home/away rotation first (B2)"
        
        # B3: Organize into weeks with dates
        week_num = 1
        base_date = datetime.strptime(start_date, "%Y-%m-%d") if start_date else datetime.now()
        
        for round_matches in self._balanced_rounds:
            # Calculate date for this week
            week_date = base_date + timedelta(weeks=week_num - 1)
            date_str = week_date.strftime("%Y-%m-%d")
            
            for home, away in round_matches:
                match_id = f"w{week_num}_{home.team_id}_vs_{away.team_id}"
                
                match = Match(
                    match_id=match_id,
                    home_team_id=home.team_id,
                    away_team_id=away.team_id,
                    home_team_name=home.name,
                    away_team_name=away.name,
                    week=week_num,
                    scheduled_date=date_str
                )
                
                self.league.matches.append(match)
            
            week_num += 1
        
        self.league.fixtures_generated = True
        
        total_matches = len(self.league.matches)
        total_weeks = week_num - 1
        
        return True, f"B3 Complete: Organized {total_matches} fixtures into {total_weeks} weeks"
    
    def generate_fixtures(self, start_date: Optional[str] = None) -> tuple[bool, str]:
        """
        Generate full fixture schedule by executing B1, B2, and B3 sequentially.
        
        This is a convenience method that orchestrates all three stories:
        - B1: Generate Round-Robin Fixtures
        - B2: Apply Home/Away Rotation
        - B3: Organize Week-by-Week Schedule
        
        Args:
            start_date: Starting date for fixtures (format: YYYY-MM-DD)
        
        Returns:
            tuple: (success, message)
        """
        # Execute B1: Generate round-robin fixtures
        success, message = self.generate_round_robin_fixtures()
        if not success:
            return False, message
        
        # Execute B2: Apply home/away rotation
        success, message = self.apply_home_away_rotation()
        if not success:
            return False, message
        
        # Execute B3: Organize by week
        success, message = self.organize_fixtures_by_week(start_date)
        if not success:
            return False, message
        
        total_matches = len(self.league.matches)
        total_weeks = (len(self.league.matches) // len(self.league.teams)) if self.league.teams else 0
        
        return True, f"All fixtures generated successfully: {total_matches} matches across {total_weeks} weeks"
    def _check_week_clash(self, team1_id: str, team2_id: str, week: int, 
                         exclude_match_id: Optional[str] = None) -> tuple[bool, str]:
        """
        B4: Check if teams already have matches in the given week.
        
        Returns:
            tuple: (has_clash, message)
        """
        if not self.league:
            return False, ""
        
        for match in self.league.matches:
            if exclude_match_id and match.match_id == exclude_match_id:
                continue
            
            if match.week != week:
                continue
            
            if match.home_team_id == team1_id or match.away_team_id == team1_id:
                return True, f"Team {team1_id} already has a match in week {week}"
            
            if match.home_team_id == team2_id or match.away_team_id == team2_id:
                return True, f"Team {team2_id} already has a match in week {week}"
        
        return False, ""