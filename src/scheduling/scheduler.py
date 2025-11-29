"""Schedule generator - implements round-robin scheduling algorithm.

Implements round-robin & weekly schedule generation. Intended to
contain algorithms with higher cyclomatic complexity (>= 10)
for teaching/assessment purposes.
"""

from typing import List, Tuple, Optional
import sys
from pathlib import Path

# Allow imports from src
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from src.domain.team import Team
from src.domain.match import Match


def generate_round_robin_pairs(teams: List[Team]) -> List[List[Tuple[Team, Team]]]:
    """
    Generate round-robin pairs using circle method algorithm.
    Cyclomatic complexity >= 10 requirement.
    
    Args:
        teams: List of Team objects (must be even number)
    
    Returns:
        List of rounds, each round is list of (home, away) tuples
    """
    n = len(teams)
    
    if n < 2:
        return []
    
    # Ensure even number of teams
    if n % 2 != 0:
        # Add a dummy "bye" team
        teams = teams.copy()
        teams.append(Team(name="BYE", stadium="N/A", team_id="bye"))
        n += 1
    
    rounds = []
    team_list = teams.copy()
    
    # Circle method: fix one team, rotate others
    for round_num in range(n - 1):
        round_matches = []
        
        for i in range(n // 2):
            team1 = team_list[i]
            team2 = team_list[n - 1 - i]
            
            # Skip if either team is BYE
            if team1.team_id == "bye" or team2.team_id == "bye":
                continue
            
            # Alternate home/away based on round and position
            if (round_num + i) % 2 == 0:
                home, away = team1, team2
            else:
                home, away = team2, team1
            
            round_matches.append((home, away))
        
        rounds.append(round_matches)
        
        # Rotate all teams except the first one
        team_list = [team_list[0]] + [team_list[-1]] + team_list[1:-1]
    
    return rounds


def balance_home_away_rotation(rounds: List[List[Tuple[Team, Team]]]) -> List[List[Tuple[Team, Team]]]:
    """
    Balance home/away assignments to prevent too many consecutive home/away games.
    Cyclomatic complexity >= 10 requirement.
    
    Args:
        rounds: List of rounds with (home, away) tuples
    
    Returns:
        Balanced rounds
    """
    if not rounds:
        return rounds
    
    # Track consecutive home/away games per team
    team_home_streak = {}
    team_away_streak = {}
    
    balanced_rounds = []
    
    for round_idx, round_matches in enumerate(rounds):
        balanced_matches = []
        
        for home, away in round_matches:
            home_id = home.team_id
            away_id = away.team_id
            
            # Initialize tracking
            if home_id not in team_home_streak:
                team_home_streak[home_id] = 0
                team_away_streak[home_id] = 0
            if away_id not in team_home_streak:
                team_home_streak[away_id] = 0
                team_away_streak[away_id] = 0
            
            # Check if we should swap
            should_swap = False
            
            # If home team has 2+ consecutive home games, consider swap
            if team_home_streak[home_id] >= 2 and team_away_streak[away_id] >= 2:
                should_swap = True
            
            # If away team has never played home and home team has played home multiple times
            elif team_home_streak[home_id] >= 2 and team_home_streak[away_id] == 0:
                should_swap = True
            
            if should_swap and round_idx > 0:  # Don't swap in first round
                # Swap home and away
                home, away = away, home
                home_id, away_id = away_id, home_id
            
            balanced_matches.append((home, away))
            
            # Update streaks
            team_home_streak[home_id] += 1
            team_away_streak[home_id] = 0
            
            team_away_streak[away_id] += 1
            team_home_streak[away_id] = 0
        
        balanced_rounds.append(balanced_matches)
    
    return balanced_rounds
