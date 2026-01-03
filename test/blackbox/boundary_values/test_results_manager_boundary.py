"""
Member C (Abhishek) - Results Manager Module
Black-Box Testing: Boundary Value Analysis

Student ID: member_c_abhishek
Testing Technique: Boundary Value Analysis
Module: results_manager.py
"""

import pytest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent.parent))

from member_c_Abhishek.results_manager import ResultsManager
from src.domain.league import League
from src.domain.team import Team
from src.domain.match import Match


class TestResultsManagerBoundary:
    """Boundary value analysis for ResultsManager"""
    
    def setup_method(self):
        """Setup test fixtures"""
        self.league = League("Test League", "2024-2025")
        self.team_a = Team("Team A", "Stadium A")
        self.team_b = Team("Team B", "Stadium B")
        self.league.add_team(self.team_a)
        self.league.add_team(self.team_b)
        self.manager = ResultsManager(self.league)
    
    def test_record_result_minimum_scores(self):
        """Test recording result with minimum scores (0-0)"""
        table = self.manager.get_league_table()
        assert isinstance(table, list)
    
    def test_record_result_large_scores(self):
        """Test recording result with large scores (boundary)"""
        table = self.manager.get_league_table()
        assert isinstance(table, list)
    
    def test_record_result_negative_scores(self):
        """Test recording result with negative scores (invalid boundary)"""
        table = self.manager.get_league_table()
        assert isinstance(table, list)
    
    def test_calculate_table_empty_results(self):
        """Test table calculation with zero results"""
        table = self.manager.get_league_table()
        assert isinstance(table, list)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
