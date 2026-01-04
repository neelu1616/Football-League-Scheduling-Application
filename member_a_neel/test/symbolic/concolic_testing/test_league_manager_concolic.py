"""
Member A (Neel) - League Manager Module
Concolic Testing

Student ID: member_a_neel
Testing Technique: Concolic Testing (Concrete + Symbolic Execution)
Module: league_manager.py
"""

import pytest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent.parent))

from member_a_Neel.league_manager import LeagueManager


class TestLeagueManagerConcolic:
    """Concolic Testing for LeagueManager"""
    
    def setup_method(self):
        """Setup test fixtures"""
        self.manager = LeagueManager(data_dir="test_data")
    
    def teardown_method(self):
        """Cleanup"""
        import shutil
        if Path("test_data").exists():
            shutil.rmtree("test_data")
    
    def test_create_league_concolic_iteration1(self):
        """
        Iteration 1: Start with concrete input
        Concrete: name="League", season="2024"
        Execute and collect: PC = {name != "", season != ""}
        Result: SUCCESS path taken
        """
        success, msg, league = self.manager.create_league("League", "2024")
        assert success is True
    
    def test_create_league_concolic_iteration2(self):
        """
        Iteration 2: Negate constraint to explore alternate path
        Negate PC: {name == "" OR season == ""}
        New concrete: name="", season="2024"
        Result: FAILURE path explored
        """
        success, msg, league = self.manager.create_league("", "2024")
        assert success is False
    
    def test_add_team_concolic_exploration(self):
        """
        Iteration 1: name="TeamA", stadium="StadiumA"
        PC = {league_exists, name!="", !duplicate}
        Result: SUCCESS
        
        Iteration 2: Add same team again
        Negate !duplicate → duplicate
        Result: FAILURE (duplicate check)
        """
        self.manager.create_league("Test League", "2024-2025")
        
        # Iteration 1
        success1, msg1 = self.manager.add_team("TeamA", "StadiumA")
        assert success1 is True
        
        # Iteration 2 - explore duplicate path
        success2, msg2 = self.manager.add_team("TeamA", "StadiumB")
        assert success2 is False


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
