"""
Member A (Neel) - League Manager Module
White-Box Testing: Basis Path Testing

Student ID: member_a_neel
Testing Technique: Basis Path Coverage
Module: league_manager.py
"""

import pytest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent.parent))

from member_a_Neel.league_manager import LeagueManager


class TestLeagueManagerBasisPath:
    """Basis Path Testing for LeagueManager"""
    
    def setup_method(self):
        """Setup test fixtures"""
        self.manager = LeagueManager(data_dir="test_data")
    
    def teardown_method(self):
        """Cleanup"""
        import shutil
        if Path("test_data").exists():
            shutil.rmtree("test_data")
    
    def test_create_league_path1_success(self):
        """Path 1: Successful league creation"""
        success, msg, league = self.manager.create_league("Test League", "2024-2025")
        assert success is True
        assert league is not None
    
    def test_create_league_path2_invalid_name(self):
        """Path 2: Invalid name validation fails"""
        success, msg, league = self.manager.create_league("", "2024-2025")
        assert success is False
    
    def test_add_team_path1_success(self):
        """Path 1: Successfully add team"""
        self.manager.create_league("Test League", "2024-2025")
        success, msg = self.manager.add_team("Team A", "Stadium A")
        assert success is True
    
    def test_validate_league_path1_valid(self):
        """Path 1: League validation succeeds with even teams"""
        self.manager.create_league("Test League", "2024-2025")
        self.manager.add_team("Team A", "Stadium A")
        self.manager.add_team("Team B", "Stadium B")
        success, msg = self.manager.validate_for_scheduling()
        assert success is True


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
