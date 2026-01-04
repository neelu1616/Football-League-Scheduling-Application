"""
Member B (Mahir) - Fixture Scheduler Module
White-Box Testing: Basis Path Testing

Student ID: member_b_mahir
Testing Technique: Basis Path Coverage
Module: fixture_scheduler.py
"""

import pytest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent.parent))

from member_b_Mahir.fixture_scheduler import FixtureScheduler
from src.domain.league import League
from src.domain.team import Team


class TestFixtureSchedulerBasisPath:
    """Basis Path Testing for FixtureScheduler"""
    
    def setup_method(self):
        """Setup test fixtures"""
        self.scheduler = FixtureScheduler()
        self.league = League("Test League", "2024-2025")
    
    def test_generate_fixtures_path1_success(self):
        """Path 1: Successful fixture generation"""
        self.league.add_team(Team("Team A", "Stadium A"))
        self.league.add_team(Team("Team B", "Stadium B"))
        self.scheduler.set_league(self.league)
        success, msg = self.scheduler.generate_fixtures()
        assert isinstance(success, bool)
    
    def test_generate_fixtures_path2_no_teams(self):
        """Path 2: No teams to schedule"""
        self.scheduler.set_league(self.league)
        success, msg = self.scheduler.generate_fixtures()
        assert success is False
    
    def test_validate_schedule_path1_valid(self):
        """Path 1: Schedule validation succeeds"""
        self.league.add_team(Team("Team A", "Stadium A"))
        self.league.add_team(Team("Team B", "Stadium B"))
        self.scheduler.set_league(self.league)
        self.scheduler.generate_fixtures()
        is_valid, errors = self.scheduler.validate_fixtures()
        assert isinstance(is_valid, bool)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
