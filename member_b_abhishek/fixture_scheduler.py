"""
Member B (Abhishek) - Scheduling Engine & Constraints Module

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

import sys
from pathlib import Path
from typing import List, Optional, Tuple
from datetime import datetime, timedelta

# Import shared domain models
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from src.domain.league import League
from src.domain.team import Team
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
    
    def set_league(self, league: League):
        """Set the league for scheduling."""
        self.league = league
    
    def generate_fixtures(self, start_date: Optional[str] = None) -> tuple[bool, str]:
        """
        B1 & B3: Generate full round-robin schedule organized by week.
        B2: Home/away rotation is balanced.
        B4: One match per team per week is enforced by round-robin structure.
        
        Args:
            start_date: Starting date for fixtures (format: YYYY-MM-DD)
        
        Returns:
            tuple: (success, message)
        """
        if not self.league:
            return False, "No league set"
        
        # Validate league has teams
        if len(self.league.teams) < 2:
            return False, "League must have at least 2 teams"
        
        if len(self.league.teams) % 2 != 0:
            return False, "League must have even number of teams"
        
        # Clear existing fixtures
        self.league.matches = []
        
        # B1: Generate round-robin pairs
        rounds = generate_round_robin_pairs(self.league.teams)
        
        # B2: Balance home/away rotation
        balanced_rounds = balance_home_away_rotation(rounds)
        
        # B3: Organize into weeks
        week_num = 1
        base_date = datetime.strptime(start_date, "%Y-%m-%d") if start_date else datetime.now()
        
        for round_matches in balanced_rounds:
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
        
        return True, f"Generated {total_matches} fixtures across {total_weeks} weeks"
    
    def reschedule_match(self, match_id: str, new_week: int) -> tuple[bool, str]:
        """
        B5: Reschedule a match to another week.
        B4: Validates no clashes in the new week.
        
        Args:
            match_id: ID of the match to reschedule
            new_week: New week number
        
        Returns:
            tuple: (success, message)
        """
        if not self.league:
            return False, "No league set"
        
        # Find the match
        match = next((m for m in self.league.matches if m.match_id == match_id), None)
        if not match:
            return False, f"Match '{match_id}' not found"
        
        if match.played:
            return False, "Cannot reschedule a match that has been played"
        
        # B4: Check for clashes in new week
        has_clash, clash_msg = self._check_week_clash(match.home_team_id, match.away_team_id, 
                                                       new_week, exclude_match_id=match_id)
        if has_clash:
            return False, f"Clash detected: {clash_msg}"
        
        old_week = match.week
        match.week = new_week
        
        return True, f"Match rescheduled from week {old_week} to week {new_week}"
    
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
    
    def validate_fixtures(self) -> tuple[bool, List[str]]:
        """
        B6: Validate fixture integrity - detect duplicates and invalid fixtures.
        
        Returns:
            tuple: (is_valid, list_of_errors)
        """
        if not self.league:
            return False, ["No league set"]
        
        errors = []
        
        # Check for duplicate matches
        seen_pairs = set()
        for match in self.league.matches:
            # Create canonical pair (sorted team IDs)
            pair = tuple(sorted([match.home_team_id, match.away_team_id]))
            
            if pair in seen_pairs:
                errors.append(f"Duplicate match: {match.home_team_name} vs {match.away_team_name}")
            else:
                seen_pairs.add(pair)
        
        # Check for teams playing themselves
        for match in self.league.matches:
            if match.home_team_id == match.away_team_id:
                errors.append(f"Invalid match: team playing itself in {match.match_id}")
        
        # Check for invalid team references
        valid_team_ids = {team.team_id for team in self.league.teams}
        for match in self.league.matches:
            if match.home_team_id not in valid_team_ids:
                errors.append(f"Invalid home team ID in {match.match_id}: {match.home_team_id}")
            if match.away_team_id not in valid_team_ids:
                errors.append(f"Invalid away team ID in {match.match_id}: {match.away_team_id}")
        
        # B4: Check for week clashes
        week_teams = {}
        for match in self.league.matches:
            week = match.week
            if week not in week_teams:
                week_teams[week] = set()
            
            if match.home_team_id in week_teams[week]:
                errors.append(f"Week clash: {match.home_team_name} plays multiple times in week {week}")
            if match.away_team_id in week_teams[week]:
                errors.append(f"Week clash: {match.away_team_name} plays multiple times in week {week}")
            
            week_teams[week].add(match.home_team_id)
            week_teams[week].add(match.away_team_id)
        
        return len(errors) == 0, errors
    
    def get_all_fixtures(self) -> List[dict]:
        """
        B7: View full fixture list.
        
        Returns:
            List of fixture dictionaries
        """
        if not self.league:
            return []
        
        return [match.to_dict() for match in sorted(self.league.matches, key=lambda m: (m.week, m.match_id))]
    
    def get_team_fixtures(self, team_identifier: str) -> List[dict]:
        """
        B8: Get fixtures for a specific team.
        
        Args:
            team_identifier: Team name or ID
        
        Returns:
            List of fixture dictionaries for the team
        """
        if not self.league:
            return []
        
        # Find team
        team = self.league.get_team_by_name(team_identifier)
        if not team:
            team = self.league.get_team_by_id(team_identifier)
        
        if not team:
            return []
        
        team_matches = [
            match for match in self.league.matches
            if match.home_team_id == team.team_id or match.away_team_id == team.team_id
        ]
        
        return [match.to_dict() for match in sorted(team_matches, key=lambda m: m.week)]
    
    def auto_regenerate_fixtures(self, start_date: Optional[str] = None) -> tuple[bool, str]:
        """
        B9: Automatically regenerate fixtures after team changes.
        
        This is called when teams are added/removed/edited to ensure
        the schedule stays consistent with league structure.
        
        Args:
            start_date: Starting date for fixtures (optional)
        
        Returns:
            tuple: (success, message)
        """
        if not self.league:
            return False, "No league set"
        
        # Validate league first (uses A9 validation)
        is_valid, error_msg = self.league.validate_for_scheduling()
        if not is_valid:
            return False, f"Cannot regenerate fixtures: {error_msg}"
        
        # Save any existing match results before regenerating
        results_backup = {}
        for match in self.league.matches:
            if match.is_played:
                # Store results by team pair
                pair = tuple(sorted([match.home_team_id, match.away_team_id]))
                results_backup[pair] = (match.home_score, match.away_score, match.home_team_id)
        
        # Regenerate fixtures
        success, msg = self.generate_fixtures(start_date)
        
        if success and results_backup:
            # Restore results
            restored = 0
            for match in self.league.matches:
                pair = tuple(sorted([match.home_team_id, match.away_team_id]))
                if pair in results_backup:
                    home_score, away_score, original_home_id = results_backup[pair]
                    
                    # Check if home/away switched
                    if match.home_team_id == original_home_id:
                        match.record_result(home_score, away_score)
                    else:
                        match.record_result(away_score, home_score)
                    
                    restored += 1
            
            if restored > 0:
                msg += f" (Restored {restored} match results)"
        
        return success, msg
    
    def get_fixtures_by_week(self, week: int) -> List[dict]:
        """
        Helper: Get all fixtures for a specific week.
        
        Args:
            week: Week number
        
        Returns:
            List of fixture dictionaries
        """
        if not self.league:
            return []
        
        week_matches = [match for match in self.league.matches if match.week == week]
        return [match.to_dict() for match in week_matches]
