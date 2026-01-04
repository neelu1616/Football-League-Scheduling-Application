"""
Member A (Neel) - League Manager Module
Symbolic Execution Testing

Student ID: member_a_neel
Testing Technique: Symbolic Execution
Module: league_manager.py
"""

import pytest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent.parent))

from member_a_Neel.league_manager import LeagueManager


class TestLeagueManagerSymbolic:
    """Symbolic Execution Testing for LeagueManager"""
    
    def setup_method(self):
        """Setup test fixtures"""
        self.manager = LeagueManager(data_dir="test_data")
    
    def teardown_method(self):
        """Cleanup"""
        import shutil
        if Path("test_data").exists():
            shutil.rmtree("test_data")
    
    def test_create_league_symbolic_path1(self):
        """
        Symbolic Execution Tree:
        Root: create_league(name, season)
        ├─ Path 1: name != "" AND season != "" → SUCCESS
        └─ Path 2: name == "" OR season == "" → FAILURE
        
        Path Condition: PC = {name != "", season != ""}
        """
        # Concrete values satisfying PC
        success, msg, league = self.manager.create_league("League", "2024")
        assert success is True
    
    def test_create_league_symbolic_path2(self):
        """
        Path Condition: PC = {name == "" OR season == ""}
        """
        # Concrete value: name == ""
        success, msg, league = self.manager.create_league("", "2024")
        assert success is False
    
    def test_add_team_symbolic_paths(self):
        """
        Symbolic Execution Tree:
        Root: add_team(name, stadium)
        ├─ Path 1: league_exists AND name_valid AND !duplicate → SUCCESS
        ├─ Path 2: !league_exists → FAILURE
        ├─ Path 3: name_invalid → FAILURE
        └─ Path 4: duplicate → FAILURE
        
        PC for Path 1: {league != None, name != "", !is_duplicate}
        """
        self.manager.create_league("Test League", "2024-2025")
        success, msg = self.manager.add_team("Team A", "Stadium A")
        assert success is True
    
    def test_validate_league_symbolic_paths(self):
        """
        Symbolic Execution Tree:
        Root: validate_league()
        ├─ Path 1: team_count >= 2 AND team_count % 2 == 0 → SUCCESS
        ├─ Path 2: team_count < 2 → FAILURE
        └─ Path 3: team_count % 2 != 0 → FAILURE
        
        PC for Path 1: {count >= 2, count % 2 == 0}
        Concrete: count = 2
        """
        self.manager.create_league("Test League", "2024-2025")
        self.manager.add_team("Team A", "Stadium A")
        self.manager.add_team("Team B", "Stadium B")
        success, msg = self.manager.validate_for_scheduling()
        assert success is True


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
