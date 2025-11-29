"""
Quick start script - Creates a demo league and demonstrates all features.

Run this to see the system in action!
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from member_a_mahir.league_manager import LeagueManager
from member_b_abhishek.fixture_scheduler import FixtureScheduler
from member_c_neel.results_manager import ResultsManager
from member_d_dhawal.diagnostics_engine import DiagnosticsEngine


def create_demo_league():
    """Create a demo league with sample data."""
    
    print("\n" + "=" * 70)
    print("FOOTBALL LEAGUE MANAGEMENT SYSTEM - QUICK START DEMO")
    print("=" * 70)
    
    # Member A: Create league and teams
    print("\n[1/4] Member A (Mahir) - Creating League and Teams...")
    mgr = LeagueManager()
    
    success, msg, league = mgr.create_league("Demo Premier League", "2024-2025")
    print(f"  ✓ {msg}")
    
    teams = [
        ("Manchester City", "Etihad Stadium"),
        ("Liverpool", "Anfield"),
        ("Arsenal", "Emirates Stadium"),
        ("Chelsea", "Stamford Bridge")
    ]
    
    for name, stadium in teams:
        success, msg = mgr.add_team(name, stadium)
        print(f"  ✓ {msg}")
    
    # Save league
    mgr.save_league("demo_league.json")
    print(f"  ✓ League saved to data/demo_league.json")
    
    # Member B: Generate fixtures
    print("\n[2/4] Member B (Abhishek) - Generating Fixtures...")
    scheduler = FixtureScheduler(league)
    
    success, msg = scheduler.generate_fixtures("2024-12-01")
    print(f"  ✓ {msg}")
    
    fixtures = scheduler.get_all_fixtures()
    print(f"\n  Sample fixtures:")
    for fixture in fixtures[:4]:
        print(f"    Week {fixture['week']}: {fixture['home_team_name']} vs {fixture['away_team_name']}")
    
    # Member C: Record results and display table
    print("\n[3/4] Member C (Neel) - Recording Results and Displaying Table...")
    results_mgr = ResultsManager(league)
    
    # Record some sample results
    sample_results = [
        (fixtures[0]['match_id'], 3, 1),
        (fixtures[1]['match_id'], 2, 2),
        (fixtures[2]['match_id'], 1, 0),
        (fixtures[3]['match_id'], 2, 1),
    ]
    
    for match_id, home, away in sample_results:
        success, msg = results_mgr.record_result(match_id, home, away)
        print(f"  ✓ {msg}")
    
    print("\n  League Table:")
    print(results_mgr.display_table())
    
    # Member D: Run diagnostics
    print("\n[4/4] Member D (Dhawal) - Running Diagnostics & Analytics...")
    diagnostics = DiagnosticsEngine()
    
    # D1: Detect anomalies
    anomalies = diagnostics.detect_scheduling_anomalies(league, save_results=False)
    print(f"  [OK] Anomaly detection: {len(anomalies)} anomalies found")
    
    # D2: Workload analysis
    workload = diagnostics.analyse_team_workload(league, save_results=False)
    if workload:
        max_travel = max(workload, key=lambda w: w.total_distance)
        print(f"  [OK] Workload: {max_travel.team_name} travels most ({max_travel.total_distance:.0f} km)")
    
    # D3: Congestion
    congestion = diagnostics.identify_fixture_congestion(league, save_results=False)
    print(f"  [OK] Congestion: {len(congestion)} congested periods identified")
    
    # D5: Trends
    trends = diagnostics.predict_outcome_trends(league, save_results=False)
    if trends:
        best_form = max(trends, key=lambda t: t.win_probability)
        print(f"  [OK] Trends: {best_form.team_name} has best form ({best_form.win_probability:.1%} win prob)")
    
    # D6: Season summary
    summary = diagnostics.generate_season_summary(league, save_results=False)
    if summary.get('statistics'):
        print(f"  [OK] Summary: {summary['statistics']['total_goals']} total goals, "
              f"{summary['statistics']['average_goals_per_match']:.2f} avg/match")
    
    print("\n" + "=" * 70)
    print("*** DEMO COMPLETE! ***")
    print("\nNext steps:")
    print("  1. Run the full CLI: python src/ui/cli.py")
    print("  2. Run integration tests: python tests/test_integration.py")
    print("  3. Run Member D demo: python member_d_demo.py")
    print("  4. Run pytest: pytest tests/ -v")

    print("  4. View saved data in: data/ folder")
    print("=" * 70 + "\n")


if __name__ == "__main__":
    create_demo_league()
