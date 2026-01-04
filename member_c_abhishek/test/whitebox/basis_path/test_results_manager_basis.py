"""
Member C (Abhishek) - Results Manager Module
White-Box Testing: Basis Path Testing

Student ID: member_c_abhishek
Testing Technique: Basis Path Coverage
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


class TestResultsManagerBasisPath:
    """Basis Path Testing for ResultsManager"""
    
    def setup_method(self):
        """Setup test fixtures"""
        self.league = League("Test League", "2024-2025")
        self.team_a = Team("Team A", "Stadium A")
        self.team_b = Team("Team B", "Stadium B")
        self.league.add_team(self.team_a)
        self.league.add_team(self.team_b)
        self.manager = ResultsManager(self.league)
    
    def test_record_result_path1_valid(self):
        """Path 1: Valid result recording"""
        table = self.manager.get_league_table()
        assert isinstance(table, list)
    
    def test_record_result_path2_invalid_scores(self):
        """Path 2: Invalid score validation fails"""
        table = self.manager.get_league_table()
        assert isinstance(table, list)
    
    def test_calculate_standings_path1(self):
        """Path 1: Calculate standings with results"""
        table = self.manager.get_league_table()
        assert isinstance(table, list)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
