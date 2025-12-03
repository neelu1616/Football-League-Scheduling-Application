"""Simple CLI for league creation, fixtures, and table display.

Integration layer combining all member modules (A, B, C, D).
"""

import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from member_a_Neel.league_manager import LeagueManager
from member_b_Mahir.fixture_scheduler import FixtureScheduler
from member_c_Abhishek.results_manager import ResultsManager
from member_d_Dhawal.diagnostics_engine import DiagnosticsEngine


class FootballLeagueCLI:
    """
    Main CLI application integrating all member modules.
    
    This demonstrates how all four members' code works together.
    """
    
    def __init__(self):
        """Initialize CLI with all service modules."""
        self.league_manager = LeagueManager()
        self.scheduler = None
        self.results_manager = None
        self.diagnostics = DiagnosticsEngine()
        self.running = True
    
    def display_menu(self):
        """Display main menu."""
        print("\n" + "=" * 70)
        print("FOOTBALL LEAGUE MANAGEMENT SYSTEM")
        print("=" * 70)
        print("\n[LEAGUE MANAGEMENT - Member A]")
        print("  1. Create New League")
        print("  2. Add Team")
        print("  3. Remove Team")
        print("  4. Edit Team")
        print("  5. List Teams")
        print("  6. Save League")
        print("  7. Load League")
        print("  8. Export League")
        
        print("\n[SCHEDULING - Member B]")
        print("  11. Generate Fixtures")
        print("  12. View All Fixtures")
        print("  13. View Team Fixtures")
        print("  14. Reschedule Match")
        print("  15. Validate Fixtures")
        
        print("\n[RESULTS & RANKINGS - Member C]")
        print("  21. Record Match Result")
        print("  22. View League Table")
        print("  23. View Team Form")
        print("  24. View Weekly Fixtures")
        print("  25. Head-to-Head Stats")
        print("  26. Export Standings")
        
        print("\n[DIAGNOSTICS & ANALYTICS - Member D]")
        print("  31. Detect Scheduling Anomalies")
        print("  32. Analyse Team Workload")
        print("  33. Identify Fixture Congestion")
        print("  34. Check Rule Compliance")
        print("  35. Predict Outcome Trends")
        print("  36. Generate Season Summary")
        print("  37. Generate Test Data")
        print("  38. Run Test Harness")
        print("  39. Extract Symbolic Paths")
        
        print("\n[SYSTEM]")
        print("  0. Exit")
        print("=" * 70)
    
    def run(self):
        """Main CLI loop."""
        print("\nWelcome to Football League Management System")
        print("Developed by: Mahir, Abhishek, Neel, Dhawal")
        
        while self.running:
            self.display_menu()
            choice = input("\nEnter your choice: ").strip()
            
            try:
                self.handle_choice(choice)
            except Exception as e:
                print(f"\n❌ Error: {str(e)}")
                print("Please try again.")
    
    def handle_choice(self, choice: str):
        """Handle user menu choice."""
        
        # League Management (Member A)
        if choice == "1":
            self.create_league()
        elif choice == "2":
            self.add_team()
        elif choice == "3":
            self.remove_team()
        elif choice == "4":
            self.edit_team()
        elif choice == "5":
            self.list_teams()
        elif choice == "6":
            self.save_league()
        elif choice == "7":
            self.load_league()
        elif choice == "8":
            self.export_league()
        
        # Scheduling (Member B)
        elif choice == "11":
            self.generate_fixtures()
        elif choice == "12":
            self.view_all_fixtures()
        elif choice == "13":
            self.view_team_fixtures()
        elif choice == "14":
            self.reschedule_match()
        elif choice == "15":
            self.validate_fixtures()
        
        # Results & Rankings (Member C)
        elif choice == "21":
            self.record_result()
        elif choice == "22":
            self.view_table()
        elif choice == "23":
            self.view_team_form()
        elif choice == "24":
            self.view_weekly_fixtures()
        elif choice == "25":
            self.head_to_head()
        elif choice == "26":
            self.export_standings()
        
        # Diagnostics (Member D)
        elif choice == "31":
            self.detect_anomalies()
        elif choice == "32":
            self.analyse_workload()
        elif choice == "33":
            self.identify_congestion()
        elif choice == "34":
            self.check_compliance()
        elif choice == "35":
            self.predict_trends()
        elif choice == "36":
            self.season_summary()
        elif choice == "37":
            self.generate_test_data()
        elif choice == "38":
            self.run_test_harness()
        elif choice == "39":
            self.extract_paths()
        
        elif choice == "0":
            print("\nThank you for using Football League Management System!")
            self.running = False
        
        else:
            print("\n❌ Invalid choice. Please try again.")
    
    # Member A - League Management methods
    
    def create_league(self):
        """A1: Create new league."""
        print("\n--- Create New League ---")
        name = input("League name: ").strip()
        season = input("Season (e.g., 2024-2025): ").strip()
        
        success, msg, league = self.league_manager.create_league(name, season)
        
        if success:
            print(f"\n✓ {msg}")
            self._sync_league()
        else:
            print(f"\n❌ {msg}")
    
    def add_team(self):
        """A2: Add team."""
        print("\n--- Add Team ---")
        name = input("Team name: ").strip()
        stadium = input("Stadium: ").strip()
        
        success, msg = self.league_manager.add_team(name, stadium)
        
        if success:
            print(f"\n✓ {msg}")
            self._sync_league()
        else:
            print(f"\n❌ {msg}")
    
    def remove_team(self):
        """A4: Remove team."""
        print("\n--- Remove Team ---")
        team = input("Team name or ID: ").strip()
        
        success, msg = self.league_manager.remove_team(team)
        
        if success:
            print(f"\n✓ {msg}")
            self._sync_league()
        else:
            print(f"\n❌ {msg}")
    
    def edit_team(self):
        """A4: Edit team."""
        print("\n--- Edit Team ---")
        team = input("Team name or ID: ").strip()
        new_name = input("New name (leave blank to skip): ").strip() or None
        new_stadium = input("New stadium (leave blank to skip): ").strip() or None
        
        success, msg = self.league_manager.edit_team(team, new_name, new_stadium)
        
        if success:
            print(f"\n✓ {msg}")
        else:
            print(f"\n❌ {msg}")
    
    def list_teams(self):
        """List all teams."""
        teams = self.league_manager.list_teams()
        
        if not teams:
            print("\n⚠ No teams in league")
            return
        
        print(f"\n--- Teams ({len(teams)}) ---")
        for idx, team in enumerate(teams, 1):
            print(f"{idx}. {team['name']} - {team['stadium']}")
    
    def save_league(self):
        """A5: Save league."""
        print("\n--- Save League ---")
        filename = input("Filename (leave blank for auto): ").strip() or None
        
        success, msg = self.league_manager.save_league(filename)
        
        if success:
            print(f"\n✓ {msg}")
        else:
            print(f"\n❌ {msg}")
    
    def load_league(self):
        """A7: Load league."""
        print("\n--- Load League ---")
        filename = input("Filename: ").strip()
        
        success, msg, league = self.league_manager.load_league(filename)
        
        if success:
            print(f"\n✓ {msg}")
            self._sync_league()
        else:
            print(f"\n❌ {msg}")
    
    def export_league(self):
        """A8: Export league."""
        print("\n--- Export League ---")
        format_type = input("Format (json/txt) [json]: ").strip() or "json"
        
        success, msg = self.league_manager.export_league(format_type)
        
        if success:
            print(f"\n✓ {msg}")
        else:
            print(f"\n❌ {msg}")
    
    # Member B - Scheduling methods
    
    def generate_fixtures(self):
        """B1, B2, B3: Generate fixtures."""
        print("\n--- Generate Fixtures ---")
        
        # A9: Validate before scheduling
        success, msg = self.league_manager.validate_for_scheduling()
        if not success:
            print(f"\n❌ {msg}")
            return
        
        start_date = input("Start date (YYYY-MM-DD) [today]: ").strip() or None
        
        self._ensure_scheduler()
        success, msg = self.scheduler.generate_fixtures(start_date)
        
        if success:
            print(f"\n✓ {msg}")
            self._sync_league()
        else:
            print(f"\n❌ {msg}")
    
    def view_all_fixtures(self):
        """B7: View all fixtures."""
        self._ensure_scheduler()
        fixtures = self.scheduler.get_all_fixtures()
        
        if not fixtures:
            print("\n⚠ No fixtures generated")
            return
        
        print(f"\n--- All Fixtures ({len(fixtures)}) ---")
        current_week = None
        
        for fixture in fixtures:
            if fixture['week'] != current_week:
                current_week = fixture['week']
                print(f"\n  Week {current_week}:")
            
            status = f"{fixture['home_score']}-{fixture['away_score']}" if fixture['played'] else "vs"
            print(f"    {fixture['home_team_name']} {status} {fixture['away_team_name']}")
    
    def view_team_fixtures(self):
        """B8: View team fixtures."""
        print("\n--- Team Fixtures ---")
        team = input("Team name or ID: ").strip()
        
        self._ensure_scheduler()
        fixtures = self.scheduler.get_team_fixtures(team)
        
        if not fixtures:
            print("\n⚠ No fixtures found for this team")
            return
        
        print(f"\n--- Fixtures for {team} ({len(fixtures)}) ---")
        for fixture in fixtures:
            status = f"{fixture['home_score']}-{fixture['away_score']}" if fixture['played'] else "vs"
            print(f"Week {fixture['week']}: {fixture['home_team_name']} {status} {fixture['away_team_name']}")
    
    def reschedule_match(self):
        """B5: Reschedule match."""
        print("\n--- Reschedule Match ---")
        match_id = input("Match ID: ").strip()
        new_week = int(input("New week number: ").strip())
        
        self._ensure_scheduler()
        success, msg = self.scheduler.reschedule_match(match_id, new_week)
        
        if success:
            print(f"\n✓ {msg}")
        else:
            print(f"\n❌ {msg}")
    
    def validate_fixtures(self):
        """B6: Validate fixtures."""
        print("\n--- Validate Fixtures ---")
        
        self._ensure_scheduler()
        is_valid, errors = self.scheduler.validate_fixtures()
        
        if is_valid:
            print("\n✓ Fixtures are valid!")
        else:
            print(f"\n❌ Found {len(errors)} validation error(s):")
            for error in errors:
                print(f"  - {error}")
    
    # Member C - Results & Rankings methods
    
    def record_result(self):
        """C1: Record match result."""
        print("\n--- Record Match Result ---")
        match_id = input("Match ID: ").strip()
        home_score = int(input("Home score: ").strip())
        away_score = int(input("Away score: ").strip())
        
        self._ensure_results_manager()
        success, msg = self.results_manager.record_result(match_id, home_score, away_score)
        
        if success:
            print(f"\n✓ {msg}")
        else:
            print(f"\n❌ {msg}")
    
    def view_table(self):
        """C4: View league table."""
        self._ensure_results_manager()
        print(self.results_manager.display_table())
    
    def view_team_form(self):
        """C5: View team form."""
        print("\n--- Team Form ---")
        team = input("Team name or ID: ").strip()
        
        self._ensure_results_manager()
        form = self.results_manager.get_team_form(team)
        
        if not form:
            print("\n⚠ Team not found")
            return
        
        print(f"\n--- {form['team']} Performance ---")
        print(f"Played: {form['played']}")
        print(f"Record: {form['won']}W-{form['drawn']}D-{form['lost']}L")
        print(f"Goals: {form['goals_for']} for, {form['goals_against']} against (GD: {form['goal_difference']:+d})")
        print(f"Points: {form['points']}")
        print(f"Form (last 5): {form['form']}")
        print(f"Win %: {form['win_percentage']:.1f}%")
    
    def view_weekly_fixtures(self):
        """C6: View weekly fixtures."""
        print("\n--- Weekly Fixtures ---")
        week_input = input("Week number (leave blank for all): ").strip()
        week = int(week_input) if week_input else None
        
        self._ensure_results_manager()
        fixtures = self.results_manager.get_weekly_fixtures(week)
        
        if not fixtures:
            print("\n⚠ No fixtures found")
            return
        
        for week_num, matches in sorted(fixtures.items()):
            print(f"\n  Week {week_num}:")
            for match in matches:
                status = f"{match['home_score']}-{match['away_score']}" if match['played'] else "vs"
                print(f"    {match['home_team_name']} {status} {match['away_team_name']}")
    
    def head_to_head(self):
        """C9: Head-to-head stats."""
        print("\n--- Head-to-Head Statistics ---")
        team1 = input("First team: ").strip()
        team2 = input("Second team: ").strip()
        
        self._ensure_results_manager()
        print(self.results_manager.display_head_to_head(team1, team2))
    
    def export_standings(self):
        """C8: Export standings."""
        print("\n--- Export Standings ---")
        filepath = input("Filepath: ").strip()
        format_type = input("Format (csv/txt) [csv]: ").strip() or "csv"
        
        self._ensure_results_manager()
        success, msg = self.results_manager.export_standings(filepath, format_type)
        
        if success:
            print(f"\n✓ {msg}")
        else:
            print(f"\n❌ {msg}")
    
    # Member D - Diagnostics methods
    
    def detect_anomalies(self):
        """D1: Detect Scheduling Anomalies."""
        print("\n--- Detect Scheduling Anomalies ---")
        
        if not self.league_manager.current_league:
            print("❌ No league loaded. Create a league first.")
            return
        
        league = self.league_manager.current_league
        
        if not league.matches:
            print("❌ No fixtures generated. Generate fixtures first (option 11).")
            return
        
        anomalies = self.diagnostics.detect_scheduling_anomalies(league)
        
        if not anomalies:
            print("\n✅ No scheduling anomalies detected - fixtures are valid!")
        else:
            print(f"\nFound {len(anomalies)} anomalies:")
            print(f"  Critical: {len([a for a in anomalies if a.severity == 'critical'])}")
            print(f"  Warnings: {len([a for a in anomalies if a.severity == 'warning'])}")
            print(f"  Info: {len([a for a in anomalies if a.severity == 'info'])}")
            
            print("\nTop 5 anomalies:")
            for i, anomaly in enumerate(anomalies[:5], 1):
                print(f"\n  {i}. [{anomaly.severity.upper()}] {anomaly.anomaly_type}")
                print(f"     {anomaly.description}")
            
            print(f"\n✓ Full report saved to: data/diagnostics/")
    
    def analyse_workload(self):
        """D2: Analyse Team Workload Distribution."""
        print("\n--- Analyse Team Workload Distribution ---")
        
        if not self.league_manager.current_league:
            print("❌ No league loaded. Create a league first.")
            return
        
        league = self.league_manager.current_league
        
        if not league.matches:
            print("❌ No fixtures generated. Generate fixtures first (option 11).")
            return
        
        workload = self.diagnostics.analyse_team_workload(league)
        
        if not workload:
            print("\n❌ No workload data available.")
            return
        
        print(f"\nWorkload analysis for {len(workload)} teams:\n")
        print(f"{'Team':<25} {'Travel (km)':<15} {'Consec Away':<15} {'Congestion':<12}")
        print("-" * 70)
        
        for wm in sorted(workload, key=lambda x: x.total_distance, reverse=True):
            print(f"{wm.team_name:<25} {wm.total_distance:<15.1f} {wm.max_consecutive_away:<15} {wm.match_congestion_score:<12.2f}")
        
        print(f"\n✓ Full report saved to: data/diagnostics/")
    
    def identify_congestion(self):
        """D3: Identify Fixture Congestion Zones."""
        print("\n--- Identify Fixture Congestion Zones ---")
        
        if not self.league_manager.current_league:
            print("❌ No league loaded. Create a league first.")
            return
        
        league = self.league_manager.current_league
        
        if not league.matches:
            print("❌ No fixtures generated. Generate fixtures first (option 11).")
            return
        
        threshold = input("Congestion threshold (matches in 3 weeks) [3]: ").strip()
        threshold = int(threshold) if threshold else 3
        
        congestion = self.diagnostics.identify_fixture_congestion(league, threshold)
        
        if not congestion:
            print("\n✅ No fixture congestion detected - schedule is well-balanced!")
        else:
            print(f"\nFound {len(congestion)} congestion zones:")
            
            for i, cz in enumerate(congestion[:10], 1):
                teams_str = ", ".join([league.get_team_by_id(tid).name for tid in cz.affected_teams[:3]])
                if len(cz.affected_teams) > 3:
                    teams_str += f" (+{len(cz.affected_teams) - 3} more)"
                
                print(f"\n  {i}. Weeks {cz.week_start}-{cz.week_end} [{cz.severity.upper()}]")
                print(f"     Density: {cz.match_density:.2f} matches/week")
                print(f"     Affected: {teams_str}")
            
            print(f"\n✓ Full report saved to: data/diagnostics/")
    
    def check_compliance(self):
        """D4: Pre-Match Rule Compliance Checker."""
        print("\n--- Pre-Match Rule Compliance Checker ---")
        
        if not self.league_manager.current_league:
            print("❌ No league loaded. Create a league first.")
            return
        
        league = self.league_manager.current_league
        
        if not league.matches:
            print("❌ No fixtures generated. Generate fixtures first (option 11).")
            return
        
        min_rest = input("Minimum rest days [3]: ").strip()
        min_rest = int(min_rest) if min_rest else 3
        
        violations = self.diagnostics.check_rule_compliance(league, min_rest_days=min_rest)
        
        if not violations:
            print("\n✅ All fixtures comply with league rules!")
        else:
            print(f"\nFound {len(violations)} rule violations:")
            
            by_severity = {}
            for v in violations:
                by_severity[v.severity] = by_severity.get(v.severity, 0) + 1
            
            for severity, count in by_severity.items():
                print(f"  {severity.upper()}: {count} violations")
            
            print("\nTop violations:")
            for i, v in enumerate(violations[:5], 1):
                print(f"\n  {i}. {v.rule_name}")
                print(f"     {v.description}")
                print(f"     Suggestion: {v.suggestion}")
            
            print(f"\n✓ Full report saved to: data/diagnostics/")
    
    def predict_trends(self):
        """D5: Predict Outcome Trends."""
        print("\n--- Predict Outcome Trends ---")
        
        if not self.league_manager.current_league:
            print("❌ No league loaded. Create a league first.")
            return
        
        league = self.league_manager.current_league
        
        played = [m for m in league.matches if m.is_played]
        if not played:
            print("❌ No results recorded. Record some results first (option 21).")
            return
        
        window = input("Analysis window (recent matches) [5]: ").strip()
        window = int(window) if window else 5
        
        trends = self.diagnostics.predict_outcome_trends(league, window_size=window)
        
        print(f"\nTrend predictions for {len(trends)} teams:\n")
        print(f"{'Team':<25} {'Form':<12} {'Win Prob':<12} {'Momentum':<15} {'Trend':<10}")
        print("-" * 80)
        
        for trend in sorted(trends, key=lambda t: t.win_probability, reverse=True):
            print(f"{trend.team_name:<25} {trend.current_form:<12} {trend.win_probability:<12.1%} "
                  f"{trend.momentum_score:+<15.2f} {trend.trend_direction:<10}")
        
        print(f"\n✓ Full report saved to: data/diagnostics/")
    
    def season_summary(self):
        """D6: Generate End-of-Season Summary."""
        print("\n--- Generate End-of-Season Summary ---")
        
        if not self.league_manager.current_league:
            print("❌ No league loaded. Create a league first.")
            return
        
        league = self.league_manager.current_league
        
        summary = self.diagnostics.generate_season_summary(league)
        
        if summary.get('status') == 'no_matches_played':
            print(f"\n❌ {summary['message']}")
            return
        
        print(f"\n{'='*70}")
        print(f"  {summary['league_name']} - Season {summary['season']}")
        print(f"{'='*70}")
        
        print(f"\nMatches: {summary['matches_played']} / {summary['total_matches']} played")
        
        stats = summary['statistics']
        print(f"\nStatistics:")
        print(f"  Total goals: {stats['total_goals']}")
        print(f"  Average goals/match: {stats['average_goals_per_match']:.2f}")
        print(f"  Home wins: {stats['home_wins']} ({stats['home_win_percentage']:.1f}%)")
        print(f"  Away wins: {stats['away_wins']}")
        print(f"  Draws: {stats['draws']}")
        
        print(f"\nHighlights:")
        for highlight in summary['highlights'][:5]:
            print(f"  • {highlight['description']}: {highlight['value']}")
        
        print(f"\n✓ Full report saved to: data/diagnostics/")
    
    def generate_test_data(self):
        """D7: Automated Test Data Generator."""
        print("\n--- Automated Test Data Generator ---")
        
        func_name = input("Function name to test: ").strip() or "sample_function"
        
        print("\nDefine parameters (type 'done' when finished):")
        params = {}
        
        while True:
            param = input("  Parameter name (or 'done'): ").strip()
            if param.lower() == 'done':
                break
            
            ptype = input(f"    Type for '{param}' (int/string/list/bool): ").strip()
            params[param] = ptype
        
        if not params:
            params = {"input": "string", "value": "int"}
            print(f"\nUsing default parameters: {params}")
        
        test_data = self.diagnostics.generate_test_data(func_name, params)
        
        print(f"\n✓ Generated {test_data['total_generated']} test cases")
        print(f"  Boundary values: {len(test_data['test_cases']['boundary_values'])}")
        print(f"  Equivalence partitions: {len(test_data['test_cases']['equivalence_partitions'])}")
        print(f"  Edge cases: {len(test_data['test_cases']['edge_cases'])}")
        print(f"  Random cases: {len(test_data['random_test_cases'])}")
        print(f"\n✓ Files created in: tests/generated/")
    
    def run_test_harness(self):
        """D8: Coverage-Aware Test Harness."""
        print("\n--- Coverage-Aware Test Harness ---")
        
        suite = input("Test suite (all/unit/integration/blackbox/whitebox) [all]: ").strip() or "all"
        threshold = input("Coverage threshold (0.0-1.0) [0.8]: ").strip()
        threshold = float(threshold) if threshold else 0.8
        
        results = self.diagnostics.run_test_harness(suite, threshold)
        
        print(f"\nTest Suite: {results['test_suite']}")
        print(f"Status: {results['status']}")
        print(f"Message: {results['message']}")
        
        if 'coverage' in results:
            cov = results['coverage']
            print(f"\nCoverage Metrics:")
            print(f"  Line coverage: {cov['line_coverage']:.1%}")
            print(f"  Branch coverage: {cov['branch_coverage']:.1%}")
            print(f"  Function coverage: {cov['function_coverage']:.1%}")
            
            if cov['uncovered_branches']:
                print(f"\nUncovered branches ({len(cov['uncovered_branches'])}):")
                for branch in cov['uncovered_branches'][:5]:
                    print(f"  • {branch['file']}:{branch['line']} - {branch['condition']}")
        
        print(f"\n✓ Results saved to: data/diagnostics/")
    
    def extract_paths(self):
        """D9: Symbolic Path Discovery Helper."""
        print("\n--- Symbolic Path Discovery Helper ---")
        print("\nEnter function source code (end with empty line + 'END'):")
        
        lines = []
        print(">>> ", end="")
        while True:
            line = input()
            if line.strip() == "END":
                break
            lines.append(line)
            print(">>> ", end="")
        
        if not lines:
            # Use a sample function
            source = '''def check_clash(team_id, week, matches):
    if not matches:
        return False
    for m in matches:
        if m.week == week:
            if m.home_team_id == team_id or m.away_team_id == team_id:
                return True
    return False'''
            func_name = "check_clash"
            print("\nUsing sample function: check_clash")
        else:
            source = "\n".join(lines)
            func_name = input("Function name: ").strip() or "function"
        
        paths = self.diagnostics.extract_symbolic_paths(source, func_name)
        
        if 'error' in paths:
            print(f"\n❌ Error: {paths['error']}")
            print(f"   {paths['message']}")
            return
        
        print(f"\n✓ Analysis for: {paths['function_name']}")
        print(f"  Total branches: {paths['total_branches']}")
        print(f"  Cyclomatic complexity: {paths['cyclomatic_complexity']}")
        print(f"  Estimated paths: {paths['estimated_paths']}")
        
        if paths['branches']:
            print(f"\n  Identified branches:")
            for branch in paths['branches'][:5]:
                print(f"    • Line {branch['line']}: {branch['type']}")
                if 'condition' in branch:
                    print(f"      Condition: {branch['condition']}")
        
        print(f"\n✓ Full report saved to: data/diagnostics/")

    
    # Helper methods
    
    def _sync_league(self):
        """Synchronize league across all modules."""
        if self.league_manager.current_league:
            league = self.league_manager.current_league
            
            if self.scheduler:
                self.scheduler.set_league(league)
            
            if self.results_manager:
                self.results_manager.set_league(league)
    
    def _ensure_scheduler(self):
        """Ensure scheduler is initialized."""
        if not self.scheduler:
            if self.league_manager.current_league:
                self.scheduler = FixtureScheduler(self.league_manager.current_league)
            else:
                self.scheduler = FixtureScheduler()
    
    def _ensure_results_manager(self):
        """Ensure results manager is initialized."""
        if not self.results_manager:
            if self.league_manager.current_league:
                self.results_manager = ResultsManager(self.league_manager.current_league)
            else:
                self.results_manager = ResultsManager()


def main():
    """Main entry point."""
    cli = FootballLeagueCLI()
    cli.run()


if __name__ == "__main__":
    main()
