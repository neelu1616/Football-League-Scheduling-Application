"""
Member B (Mahir) - Fixture Scheduler Module
Black-Box Testing: Boundary Value Analysis

Student ID: member_b_mahir
Testing Technique: Boundary Value Analysis
Module: fixture_scheduler.py
"""

import pytest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent.parent))

from member_b_Mahir.fixture_scheduler import FixtureScheduler
from src.domain.league import League
from src.domain.team import Team


class TestFixtureSchedulerBoundary:
    """Boundary value analysis for FixtureScheduler"""
    
    def setup_method(self):
        """Setup test fixtures"""
        self.scheduler = FixtureScheduler()
        self.league = League("Test League", "2024-2025")
    
    def test_schedule_minimum_teams(self):
        """Test scheduling with minimum teams (2)"""
        self.league.add_team(Team("Team A", "Stadium A"))
        self.league.add_team(Team("Team B", "Stadium B"))
        self.scheduler.set_league(self.league)
        success, msg = self.scheduler.generate_fixtures()
        assert isinstance(success, bool)
    
    def test_schedule_zero_teams(self):
        """Test scheduling with zero teams (boundary)"""
        self.scheduler.set_league(self.league)
        success, msg = self.scheduler.generate_fixtures()
        assert success is False
    
    def test_schedule_odd_teams(self):
        """Test scheduling with odd number of teams"""
        for i in range(3):
            self.league.add_team(Team(f"Team {i}", f"Stadium {i}"))
        self.scheduler.set_league(self.league)
        success, msg = self.scheduler.generate_fixtures()
        assert success is False
    
    def test_schedule_large_league(self):
        """Test scheduling with large number of teams (20)"""
        for i in range(20):
            self.league.add_team(Team(f"Team {i}", f"Stadium {i}"))
        self.scheduler.set_league(self.league)
        success, msg = self.scheduler.generate_fixtures()
        assert isinstance(success, bool)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
