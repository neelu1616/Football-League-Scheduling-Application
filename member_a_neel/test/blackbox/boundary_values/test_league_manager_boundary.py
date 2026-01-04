"""
Member A (Neel) - League Manager Module
Black-Box Testing: Boundary Value Analysis

Student ID: member_a_neel
Testing Technique: Boundary Value Analysis
Module: league_manager.py
"""

import pytest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent.parent))

from member_a_Neel.league_manager import LeagueManager
from src.domain.league import League
from src.domain.team import Team


class TestLeagueManagerBoundary:
    """Boundary value analysis for LeagueManager"""
    
    def setup_method(self):
        """Setup test fixtures"""
        self.manager = LeagueManager(data_dir="test_data")
    
    def teardown_method(self):
        """Cleanup after each test"""
        import shutil
        if Path("test_data").exists():
            shutil.rmtree("test_data")
    
    # ===== A1: Create League - Boundary Tests =====
    
    def test_create_league_minimum_boundary(self):
        """Test creating league with minimum valid length inputs"""
        success, msg, league = self.manager.create_league("ABC", "2024")
        assert success is True
        assert league is not None
    
    def test_create_league_empty_inputs(self):
        """Test creating league with empty inputs (boundary)"""
        success, msg, league = self.manager.create_league("", "")
        assert success is False
    
    def test_add_team_boundary_values(self):
        """Test adding team with boundary value inputs"""
        self.manager.create_league("Test League", "2024-2025")
        success, msg = self.manager.add_team("", "Stadium A")
        assert success is False
    
    def test_validate_league_team_count_boundaries(self):
        """Test validation with different team counts (boundary analysis)"""
        self.manager.create_league("Test League", "2024-2025")
        
        # Zero teams
        success, msg = self.manager.validate_for_scheduling()
        assert success is False
        
        # Two teams (minimum valid)
        self.manager.add_team("Team A", "Stadium A")
        self.manager.add_team("Team B", "Stadium B")
        success, msg = self.manager.validate_for_scheduling()
        assert success is True


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
