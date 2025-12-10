"""
Test suite for A-6: Team data validation rules
Tests input validation for teams (name length, stadium checks)
"""

import sys
from pathlib import Path

# Add the project root to the path
sys.path.insert(0, str(Path(__file__).parent))

from rankings.league_manager import LeagueManager


def test_validate_team_name_too_short():
    """Test validation fails when team name is too short (< 2 chars)"""
    manager = LeagueManager()
    manager.create_league("Premier League", "2024-2025")
    
    is_valid, error_msg = manager.validate_team_data("A", "Valid Stadium")
    assert not is_valid, "Should reject team name with 1 character"
    assert "Team name must be at least 2 characters" in error_msg
    print("✓ Test passed: Team name too short (1 char) rejected")


def test_validate_team_name_too_long():
    """Test validation fails when team name is too long (> 50 chars)"""
    manager = LeagueManager()
    manager.create_league("Premier League", "2024-2025")
    
    long_name = "A" * 51
    is_valid, error_msg = manager.validate_team_data(long_name, "Valid Stadium")
    assert not is_valid, "Should reject team name with 51 characters"
    assert "Team name must not exceed 50 characters" in error_msg
    print("✓ Test passed: Team name too long (51 chars) rejected")


def test_validate_stadium_name_too_short():
    """Test validation fails when stadium name is too short (< 2 chars)"""
    manager = LeagueManager()
    manager.create_league("Premier League", "2024-2025")
    
    is_valid, error_msg = manager.validate_team_data("Valid Team", "A")
    assert not is_valid, "Should reject stadium name with 1 character"
    assert "Stadium name must be at least 2 characters" in error_msg
    print("✓ Test passed: Stadium name too short (1 char) rejected")


def test_validate_stadium_name_too_long():
    """Test validation fails when stadium name is too long (> 100 chars)"""
    manager = LeagueManager()
    manager.create_league("Premier League", "2024-2025")
    
    long_stadium = "A" * 101
    is_valid, error_msg = manager.validate_team_data("Valid Team", long_stadium)
    assert not is_valid, "Should reject stadium name with 101 characters"
    assert "Stadium name must not exceed 100 characters" in error_msg
    print("✓ Test passed: Stadium name too long (101 chars) rejected")


def test_validate_empty_team_name():
    """Test validation fails when team name is empty"""
    manager = LeagueManager()
    manager.create_league("Premier League", "2024-2025")
    
    is_valid, error_msg = manager.validate_team_data("", "Valid Stadium")
    assert not is_valid, "Should reject empty team name"
    assert "Team name must be at least 2 characters" in error_msg
    print("✓ Test passed: Empty team name rejected")


def test_validate_empty_stadium_name():
    """Test validation fails when stadium name is empty"""
    manager = LeagueManager()
    manager.create_league("Premier League", "2024-2025")
    
    is_valid, error_msg = manager.validate_team_data("Valid Team", "")
    assert not is_valid, "Should reject empty stadium name"
    assert "Stadium name must be at least 2 characters" in error_msg
    print("✓ Test passed: Empty stadium name rejected")


def test_validate_whitespace_only_team_name():
    """Test validation fails when team name is whitespace only"""
    manager = LeagueManager()
    manager.create_league("Premier League", "2024-2025")
    
    is_valid, error_msg = manager.validate_team_data("   ", "Valid Stadium")
    assert not is_valid, "Should reject whitespace-only team name"
    assert "Team name must be at least 2 characters" in error_msg
    print("✓ Test passed: Whitespace-only team name rejected")


def test_validate_valid_team_data():
    """Test validation passes with valid team data"""
    manager = LeagueManager()
    manager.create_league("Premier League", "2024-2025")
    
    is_valid, error_msg = manager.validate_team_data("Manchester United", "Old Trafford")
    assert is_valid, f"Should accept valid team data, got error: {error_msg}"
    assert error_msg == "", "Error message should be empty for valid data"
    print("✓ Test passed: Valid team data accepted")


def test_validate_boundary_team_name_min():
    """Test validation with minimum valid team name length (2 chars)"""
    manager = LeagueManager()
    manager.create_league("Premier League", "2024-2025")
    
    is_valid, error_msg = manager.validate_team_data("AB", "Valid Stadium")
    assert is_valid, f"Should accept 2-character team name, got error: {error_msg}"
    print("✓ Test passed: Minimum valid team name (2 chars) accepted")


def test_validate_boundary_team_name_max():
    """Test validation with maximum valid team name length (50 chars)"""
    manager = LeagueManager()
    manager.create_league("Premier League", "2024-2025")
    
    max_name = "A" * 50
    is_valid, error_msg = manager.validate_team_data(max_name, "Valid Stadium")
    assert is_valid, f"Should accept 50-character team name, got error: {error_msg}"
    print("✓ Test passed: Maximum valid team name (50 chars) accepted")


def test_validate_boundary_stadium_name_min():
    """Test validation with minimum valid stadium name length (2 chars)"""
    manager = LeagueManager()
    manager.create_league("Premier League", "2024-2025")
    
    is_valid, error_msg = manager.validate_team_data("Valid Team", "AB")
    assert is_valid, f"Should accept 2-character stadium name, got error: {error_msg}"
    print("✓ Test passed: Minimum valid stadium name (2 chars) accepted")


def test_validate_boundary_stadium_name_max():
    """Test validation with maximum valid stadium name length (100 chars)"""
    manager = LeagueManager()
    manager.create_league("Premier League", "2024-2025")
    
    max_stadium = "A" * 100
    is_valid, error_msg = manager.validate_team_data("Valid Team", max_stadium)
    assert is_valid, f"Should accept 100-character stadium name, got error: {error_msg}"
    print("✓ Test passed: Maximum valid stadium name (100 chars) accepted")


def test_add_team_with_invalid_data():
    """Test add_team rejects invalid team data"""
    manager = LeagueManager()
    manager.create_league("Premier League", "2024-2025")
    
    # Try adding team with too short name
    success, message = manager.add_team("A", "Valid Stadium")
    assert not success, "Should reject adding team with invalid data"
    assert "Team name must be at least 2 characters" in message
    print("✓ Test passed: add_team rejects invalid data")


def test_add_team_with_valid_data():
    """Test add_team accepts valid team data"""
    manager = LeagueManager()
    manager.create_league("Premier League", "2024-2025")
    
    # Add team with valid data
    success, message = manager.add_team("Manchester United", "Old Trafford")
    assert success, f"Should accept valid team data, got error: {message}"
    assert manager.current_league.get_team_by_name("Manchester United") is not None
    print("✓ Test passed: add_team accepts valid data")


def test_edit_team_with_invalid_data():
    """Test edit_team rejects invalid team data"""
    manager = LeagueManager()
    manager.create_league("Premier League", "2024-2025")
    manager.add_team("Manchester United", "Old Trafford")
    
    # Try editing with too long name
    long_name = "A" * 51
    success, message = manager.edit_team("Manchester United", new_name=long_name)
    assert not success, "Should reject editing with invalid data"
    assert "Team name must not exceed 50 characters" in message
    print("✓ Test passed: edit_team rejects invalid data")


def test_edit_team_with_valid_data():
    """Test edit_team accepts valid team data"""
    manager = LeagueManager()
    manager.create_league("Premier League", "2024-2025")
    manager.add_team("Manchester United", "Old Trafford")
    
    # Edit with valid data
    success, message = manager.edit_team("Manchester United", new_name="Man United", new_stadium="New Stadium")
    assert success, f"Should accept valid edit data, got error: {message}"
    print("✓ Test passed: edit_team accepts valid data")


def run_all_tests():
    """Run all validation tests"""
    print("\n" + "="*70)
    print("Running A-6 Team Data Validation Tests")
    print("="*70 + "\n")
    
    tests = [
        test_validate_team_name_too_short,
        test_validate_team_name_too_long,
        test_validate_stadium_name_too_short,
        test_validate_stadium_name_too_long,
        test_validate_empty_team_name,
        test_validate_empty_stadium_name,
        test_validate_whitespace_only_team_name,
        test_validate_valid_team_data,
        test_validate_boundary_team_name_min,
        test_validate_boundary_team_name_max,
        test_validate_boundary_stadium_name_min,
        test_validate_boundary_stadium_name_max,
        test_add_team_with_invalid_data,
        test_add_team_with_valid_data,
        test_edit_team_with_invalid_data,
        test_edit_team_with_valid_data,
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            test()
            passed += 1
        except AssertionError as e:
            print(f"✗ Test failed: {test.__name__}")
            print(f"  Error: {str(e)}\n")
            failed += 1
        except Exception as e:
            print(f"✗ Test error: {test.__name__}")
            print(f"  Error: {str(e)}\n")
            failed += 1
    
    print("\n" + "="*70)
    print(f"Test Results: {passed} passed, {failed} failed")
    print("="*70 + "\n")
    
    return failed == 0


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
