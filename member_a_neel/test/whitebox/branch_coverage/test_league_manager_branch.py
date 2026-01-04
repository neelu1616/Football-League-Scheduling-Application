"""
Member A (Neel) - League Manager Module
White-Box Testing: Branch Coverage

Student ID: member_a_neel
Testing Technique: Branch Coverage
Module: league_manager.py
"""

import pytest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent.parent))

from member_a_Neel.league_manager import LeagueManager


class TestLeagueManagerBranchCoverage:
    """Branch Coverage Testing for LeagueManager"""
    
    def setup_method(self):
        """Setup test fixtures"""
        self.manager = LeagueManager(data_dir="test_data")
    
    def teardown_method(self):
        """Cleanup"""
        import shutil
        if Path("test_data").exists():
            shutil.rmtree("test_data")
    
    def test_create_league_both_branches(self):
        """Test both TRUE and FALSE branches for create_league validation"""
        # TRUE branch - valid inputs
        success, msg, league = self.manager.create_league("Valid League", "2024")
        assert success is True
        
        # FALSE branch - invalid inputs
        success, msg, league = self.manager.create_league("", "2024")
        assert success is False
    
    def test_add_team_duplicate_check_branches(self):
        """Test both branches for duplicate team check"""
        self.manager.create_league("Test League", "2024-2025")
        
        # TRUE branch - unique team
        success, msg = self.manager.add_team("Team A", "Stadium A")
        assert success is True
        
        # FALSE branch - duplicate team
        success, msg = self.manager.add_team("Team A", "Stadium B")
        assert success is False
    
    def test_validate_league_odd_even_branches(self):
        """Test branches for odd/even team count validation"""
        self.manager.create_league("Test League", "2024-2025")
        
        # Odd number branch (FALSE)
        self.manager.add_team("Team A", "Stadium A")
        success, msg = self.manager.validate_for_scheduling()
        assert success is False
        
        # Even number branch (TRUE)
        self.manager.add_team("Team B", "Stadium B")
        success, msg = self.manager.validate_for_scheduling()
        assert success is True


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
