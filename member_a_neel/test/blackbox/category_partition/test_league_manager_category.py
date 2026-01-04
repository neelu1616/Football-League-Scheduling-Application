"""
Member A (Neel) - League Manager Module
Black-Box Testing: Category Partition

Student ID: member_a_neel
Testing Technique: Category Partition Testing
Module: league_manager.py
"""

import pytest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent.parent))

from member_a_Neel.league_manager import LeagueManager
from src.domain.league import League


class TestLeagueManagerCategoryPartition:
    """Category Partition Testing for LeagueManager"""
    
    def setup_method(self):
        """Setup test fixtures"""
        self.manager = LeagueManager(data_dir="test_data")
    
    def teardown_method(self):
        """Cleanup"""
        import shutil
        if Path("test_data").exists():
            shutil.rmtree("test_data")
    
    def test_create_league_valid_inputs(self):
        """Category: Valid name + Valid season"""
        success, msg, league = self.manager.create_league("Premier League", "2024-2025")
        assert success is True
    
    def test_create_league_invalid_name_category(self):
        """Category: Invalid name (empty) + Valid season"""
        success, msg, league = self.manager.create_league("", "2024-2025")
        assert success is False
    
    def test_add_team_valid_category(self):
        """Category: Valid team name + Valid stadium"""
        self.manager.create_league("Test League", "2024-2025")
        success, msg = self.manager.add_team("Manchester United", "Old Trafford")
        assert success is True
    
    def test_add_team_duplicate_category(self):
        """Category: Duplicate team name"""
        self.manager.create_league("Test League", "2024-2025")
        self.manager.add_team("Arsenal", "Emirates Stadium")
        success, msg = self.manager.add_team("Arsenal", "Another Stadium")
        assert success is False


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
