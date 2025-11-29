"""
Quick demo of Member D (Dhawal) - Diagnostics Engine
Demonstrates all 9 user stories: D1-D9
"""

import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from member_d_dhawal.diagnostics_engine import DiagnosticsEngine
from member_a_mahir.league_manager import LeagueManager
from member_b_abhishek.fixture_scheduler import FixtureScheduler
from member_c_neel.results_manager import ResultsManager


def print_header(title: str):
    """Print formatted header."""
    print(f"\n{'='*70}")
    print(f"  {title}")
    print(f"{'='*70}\n")


def main():
    print("\n*** MEMBER D (DHAWAL) - DIAGNOSTICS ENGINE DEMO ***")
    print("="*70)
    print("Demonstrating all 9 user stories with Football League data\n")
    
    # Initialize engines
    league_mgr = LeagueManager()
    diagnostics = DiagnosticsEngine()
    
    # Create a test league with teams
    print_header("Setup: Creating League & Teams")
    success, msg, _ = league_mgr.create_league("Premier League", "2024-2025")
    
    teams_data = [
        ("Manchester City", "Etihad Stadium"),
        ("Liverpool", "Anfield"),
        ("Arsenal", "Emirates Stadium"),
        ("Chelsea", "Stamford Bridge"),
        ("Manchester United", "Old Trafford"),
        ("Tottenham", "Tottenham Hotspur Stadium")
    ]
    
    for name, stadium in teams_data:
        league_mgr.add_team(name, stadium)
    
    print(f"[OK] League created with {len(league_mgr.current_league.teams)} teams")
    for team in league_mgr.current_league.teams:
        print(f"  • {team.name}")
    
    # Use the league from the manager
    league = league_mgr.current_league
    
    # Generate fixtures
    print_header("Setup: Generating Fixtures")
    scheduler = FixtureScheduler(league)
    scheduler.generate_fixtures()
    print(f"[OK] Generated {len(league.matches)} fixtures across {max(m.week for m in league.matches)} weeks")
    
    # Record some sample results
    print_header("Setup: Recording Sample Results")
    results_mgr = ResultsManager(league)
    sample_results = [
        (0, 3, 1),  # Match 0: home team wins 3-1
        (1, 1, 1),  # Match 1: draw
        (2, 0, 2),  # Match 2: away team wins
        (3, 2, 0),  # Match 3: home team wins
        (4, 1, 3),  # Match 4: away team wins
        (5, 2, 2),  # Match 5: draw
    ]
    
    for match_idx, home_score, away_score in sample_results:
        if match_idx < len(league.matches):
            results_mgr.record_result(league.matches[match_idx].match_id, home_score, away_score)
    
    print(f"[OK] Recorded {len(sample_results)} match results")
    
    # D1: Detect Scheduling Anomalies
    print_header("D1: Detect Scheduling Anomalies")
    anomalies = diagnostics.detect_scheduling_anomalies(league)
    
    if anomalies:
        print(f"Found {len(anomalies)} anomalies:")
        for anomaly in anomalies[:5]:  # Show first 5
            print(f"  • [{anomaly.severity.upper()}] {anomaly.anomaly_type}: {anomaly.description}")
    else:
        print("*** No scheduling anomalies detected - fixtures are valid!")
    
    # D2: Analyse Team Workload Distribution
    print_header("D2: Analyse Team Workload Distribution")
    workload = diagnostics.analyse_team_workload(league)
    
    print(f"Workload analysis for {len(workload)} teams:")
    for wm in workload[:3]:  # Show first 3
        print(f"\n  {wm.team_name}:")
        print(f"    • Total travel: {wm.total_distance:.1f} km")
        print(f"    • Avg per match: {wm.average_distance_per_match:.1f} km")
        print(f"    • Max consecutive away: {wm.max_consecutive_away}")
        print(f"    • Congestion score: {wm.match_congestion_score:.2f}")
        print(f"    • Avg rest days: {wm.rest_days_avg:.1f}")
    
    # D3: Identify Fixture Congestion Zones
    print_header("D3: Identify Fixture Congestion Zones")
    congestion = diagnostics.identify_fixture_congestion(league)
    
    if congestion:
        print(f"Found {len(congestion)} congestion zones:")
        for cz in congestion[:3]:  # Show first 3
            teams_str = ", ".join([league.get_team_by_id(tid).name for tid in cz.affected_teams[:2]])
            print(f"  • Weeks {cz.week_start}-{cz.week_end}: {len(cz.affected_teams)} teams affected")
            print(f"    Severity: {cz.severity}, Density: {cz.match_density:.2f} matches/week")
            print(f"    Teams: {teams_str}...")
    else:
        print("*** No fixture congestion detected - schedule is well-balanced!")
    
    # D4: Pre-Match Rule Compliance Checker
    print_header("D4: Pre-Match Rule Compliance Checker")
    violations = diagnostics.check_rule_compliance(league, min_rest_days=3)
    
    if violations:
        print(f"Found {len(violations)} rule violations:")
        severity_counts = {}
        for v in violations:
            severity_counts[v.severity] = severity_counts.get(v.severity, 0) + 1
        
        for severity, count in severity_counts.items():
            print(f"  • {severity.upper()}: {count} violations")
        
        print("\nSample violations:")
        for v in violations[:3]:
            print(f"  • {v.rule_name}: {v.description}")
            print(f"    Suggestion: {v.suggestion}")
    else:
        print("*** All fixtures comply with league rules!")
    
    # D5: Predict Outcome Trends
    print_header("D5: Predict Outcome Trends Using Statistical Indicators")
    trends = diagnostics.predict_outcome_trends(league, window_size=5)
    
    print(f"Trend predictions for {len(trends)} teams:")
    for trend in trends[:4]:  # Show first 4
        print(f"\n  {trend.team_name}:")
        print(f"    • Current form: {trend.current_form}")
        print(f"    • Win probability: {trend.win_probability:.1%}")
        print(f"    • Expected points (next 5): {trend.expected_points_next_5:.1f}")
        print(f"    • Momentum: {trend.momentum_score:+.2f} ({trend.trend_direction})")
    
    # D6: Generate End-of-Season Summary Report
    print_header("D6: Generate End-of-Season Summary Report")
    summary = diagnostics.generate_season_summary(league)
    
    if summary.get("status") != "no_matches_played":
        print(f"Season: {summary['season']}")
        print(f"Matches played: {summary['matches_played']} / {summary['total_matches']}")
        print(f"\nStatistics:")
        stats = summary['statistics']
        print(f"  • Total goals: {stats['total_goals']}")
        print(f"  • Avg goals/match: {stats['average_goals_per_match']:.2f}")
        print(f"  • Home wins: {stats['home_wins']} ({stats['home_win_percentage']:.1f}%)")
        print(f"  • Away wins: {stats['away_wins']}")
        print(f"  • Draws: {stats['draws']}")
        
        print(f"\nHighlights:")
        for highlight in summary['highlights'][:3]:
            print(f"  • {highlight['description']}: {highlight['value']}")
    else:
        print(summary['message'])
    
    # D7: Automated Boundary & Partition Test Generator
    print_header("D7: Automated Test Data Generator")
    test_data = diagnostics.generate_test_data(
        function_name="validate_team",
        parameter_types={"name": "string", "stadium": "string", "team_id": "int"},
        save_to_file=True
    )
    
    print(f"Generated test data for function: {test_data['function_name']}")
    print(f"  • Total test cases: {test_data['total_generated']}")
    print(f"  • Boundary values: {len(test_data['test_cases']['boundary_values'])}")
    print(f"  • Equivalence partitions: {len(test_data['test_cases']['equivalence_partitions'])}")
    print(f"  • Edge cases: {len(test_data['test_cases']['edge_cases'])}")
    print(f"  • Random cases: {len(test_data['random_test_cases'])}")
    print("\n  Sample boundary test case:")
    print(f"    {test_data['test_cases']['boundary_values'][0]}")
    
    # D8: Coverage-Aware Test Harness
    print_header("D8: Coverage-Aware Test Harness")
    harness_result = diagnostics.run_test_harness(test_suite="all", coverage_threshold=0.8)
    
    print(f"Test suite: {harness_result['test_suite']}")
    print(f"Status: {harness_result['status']}")
    print(f"Message: {harness_result['message']}")
    
    if 'coverage' in harness_result:
        cov = harness_result['coverage']
        print(f"\nCoverage metrics:")
        print(f"  • Line coverage: {cov['line_coverage']:.1%}")
        print(f"  • Branch coverage: {cov['branch_coverage']:.1%}")
        print(f"  • Function coverage: {cov['function_coverage']:.1%}")
        
        if cov['uncovered_branches']:
            print(f"\n  Uncovered branches ({len(cov['uncovered_branches'])}):")
            for branch in cov['uncovered_branches'][:2]:
                print(f"    • {branch['file']}:{branch['line']} - {branch['condition']}")
    
    # D9: Symbolic Path Discovery Helper
    print_header("D9: Symbolic Path Discovery Helper")
    
    # Sample function to analyze
    sample_function = '''
def check_scheduling_conflict(team_id: str, week: int, matches: list) -> bool:
    """Check if team has scheduling conflict in given week."""
    if not matches:
        return False
    
    for match in matches:
        if match.week == week:
            if match.home_team_id == team_id or match.away_team_id == team_id:
                return True
    
    return False
'''
    
    paths = diagnostics.extract_symbolic_paths(sample_function, "check_scheduling_conflict")
    
    if 'error' not in paths:
        print(f"Function: {paths['function_name']}")
        print(f"  • Total branches: {paths['total_branches']}")
        print(f"  • Cyclomatic complexity: {paths['cyclomatic_complexity']}")
        print(f"  • Estimated paths: {paths['estimated_paths']}")
        
        print(f"\n  Identified branches:")
        for branch in paths['branches'][:3]:
            print(f"    • Line {branch['line']}: {branch['type']}")
            if 'condition' in branch:
                print(f"      Condition: {branch['condition']}")
    else:
        print(f"Error: {paths['error']}")
    
    # Summary
    print_header("Summary: Diagnostics Reports Generated")
    diag_summary = diagnostics.get_diagnostics_summary()
    
    print(f"Total reports generated: {diag_summary.get('total_reports', 0)}")
    print(f"Reports directory: {diag_summary['diagnostics_directory']}")
    
    if 'by_type' in diag_summary:
        print(f"\nBy type:")
        for report_type, count in diag_summary['by_type'].items():
            print(f"  • {report_type}: {count} reports")
    
    print("\n" + "="*70)
    print("*** DEMO COMPLETE! ***")
    print("="*70)
    print("\nAll 9 user stories demonstrated:")
    print("  D1 [OK] Detect Scheduling Anomalies")
    print("  D2 [OK] Analyse Team Workload Distribution")
    print("  D3 [OK] Identify Fixture Congestion Zones")
    print("  D4 [OK] Pre-Match Rule Compliance Checker")
    print("  D5 [OK] Predict Outcome Trends")
    print("  D6 [OK] Generate End-of-Season Summary Report")
    print("  D7 [OK] Automated Test Data Generator")
    print("  D8 [OK] Coverage-Aware Test Harness")
    print("  D9 [OK] Symbolic Path Discovery Helper")
    print()


if __name__ == "__main__":
    main()
