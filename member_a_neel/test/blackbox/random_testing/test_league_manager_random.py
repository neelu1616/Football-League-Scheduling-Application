"""
Member A (Neel) - League Manager Module
Black-Box Testing: Random Testing

Student ID: member_a_neel
Testing Technique: Random Testing
Module: league_manager.py
"""

import pytest
import sys
import random
import string
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent.parent))

from member_a_Neel.league_manager import LeagueManager


class TestLeagueManagerRandom:
    """Random Testing for LeagueManager"""
    
    def setup_method(self):
        """Setup test fixtures"""
        self.manager = LeagueManager(data_dir="test_data")
        random.seed(42)
    
    def teardown_method(self):
        """Cleanup"""
        import shutil
        if Path("test_data").exists():
            shutil.rmtree("test_data")
    
    def random_string(self, length=10):
        """Generate random string"""
        return ''.join(random.choices(string.ascii_letters + string.digits, k=length))
    
    def test_create_league_random_inputs(self):
        """Test with random valid inputs"""
        name = self.random_string(15)
        season = f"{random.randint(2020, 2030)}-{random.randint(2021, 2031)}"
        success, msg, league = self.manager.create_league(name, season)
        assert isinstance(success, bool)
    
    def test_add_random_teams(self):
        """Test adding multiple random teams"""
        self.manager.create_league("Random League", "2024-2025")
        for _ in range(4):
            team_name = self.random_string(10)
            stadium = self.random_string(12)
            success, msg = self.manager.add_team(team_name, stadium)
            assert isinstance(success, bool)
    
    def test_random_special_characters(self):
        """Test with random special characters"""
        special_chars = "!@#$%^&*()"
        name = ''.join(random.choices(special_chars, k=5))
        success, msg, league = self.manager.create_league(name, "2024")
        assert isinstance(success, bool)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
