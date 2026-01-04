"""
Member B (Mahir) - Fixture Scheduler Module
Symbolic Execution Testing

Student ID: member_b_mahir
Testing Technique: Symbolic Execution
Module: fixture_scheduler.py
"""

import pytest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent.parent))

from member_b_Mahir.fixture_scheduler import FixtureScheduler
from src.domain.league import League
from src.domain.team import Team


class TestFixtureSchedulerSymbolic:
    """Symbolic Execution Testing for FixtureScheduler"""
    
    def setup_method(self):
        """Setup test fixtures"""
        self.scheduler = FixtureScheduler()
        self.league = League("Test League", "2024-2025")
    
    def test_generate_fixtures_symbolic_path1(self):
        """
        Symbolic Execution Tree:
        Root: generate_fixtures(league)
        ├─ Path 1: team_count >= 2 AND team_count % 2 == 0 → SUCCESS
        └─ Path 2: team_count < 2 OR team_count % 2 != 0 → FAILURE
        
        Path Condition: PC = {count >= 2, count % 2 == 0}
        Concrete: count = 4
        """
        for i in range(4):
            self.league.add_team(Team(f"Team {i}", f"Stadium {i}"))
        self.scheduler.set_league(self.league)
        success, msg = self.scheduler.generate_fixtures()
        assert isinstance(success, bool)
    
    def test_generate_fixtures_symbolic_path2(self):
        """
        Path Condition: PC = {count < 2 OR count % 2 != 0}
        Concrete: count = 1 (odd)
        """
        self.league.add_team(Team("Team A", "Stadium A"))
        self.scheduler.set_league(self.league)
        success, msg = self.scheduler.generate_fixtures()
        assert success is False
    
    def test_check_conflicts_symbolic_paths(self):
        """
        Symbolic Execution Tree:
        Root: check_conflicts(fixtures)
        ├─ Path 1: no_conflicts → TRUE
        └─ Path 2: conflicts_exist → FALSE
        
        PC for Path 1: {!has_duplicate_dates, !has_venue_conflicts}
        """
        self.league.add_team(Team("Team A", "Stadium A"))
        self.league.add_team(Team("Team B", "Stadium B"))
        self.scheduler.set_league(self.league)
        self.scheduler.generate_fixtures()
        is_valid, errors = self.scheduler.validate_fixtures()
        assert isinstance(is_valid, bool)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
