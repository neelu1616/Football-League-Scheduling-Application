# Member Quick Reference Guide

## Member A (Mahir) - League & Team Management

**Your folder:** `member_a_mahir/`

### Your Responsibilities
1. League creation and configuration
2. Team CRUD operations (Create, Read, Update, Delete)
3. Data validation (team names, stadiums)
4. Persistence (save/load leagues to/from JSON)
5. Pre-scheduling validation (A9)

### Key File
- `league_manager.py` - Your main implementation

### Testing Your Code
```powershell
# Quick test
python -c "from member_a_mahir import LeagueManager; m=LeagueManager(); m.create_league('Test','2024'); print('✓ Works!')"

# Full integration
python tests/test_integration.py
```

### User Stories to Demo
- A1: Create league → Show league creation
- A2: Add teams → Add 4 teams
- A5: Save league → Save to JSON
- A7: Load league → Load saved file
- A9: Validation → Try to schedule with odd number of teams (should fail)

---

## Member B (Abhishek) - Scheduling Engine & Constraints

**Your folder:** `member_b_abhishek/`

### Your Responsibilities
1. Round-robin fixture generation (B1)
2. Home/away balancing (B2)
3. Week-by-week organization (B3)
4. Clash detection (B4)
5. Rescheduling (B5)
6. Fixture validation (B6)
7. Auto-regeneration on team changes (B9)

### Key Files
- `fixture_scheduler.py` - Your main implementation
- `../src/scheduling/scheduler.py` - Round-robin algorithm (cyclomatic ≥10)

### Testing Your Code
```powershell
# Quick test
python quick_start.py  # See scheduling in action

# Integration test
python tests/test_integration.py
```

### User Stories to Demo
- B1: Generate fixtures → Show round-robin generation
- B2: Home/away → Point out balanced assignments
- B4: Clash detection → Try to reschedule causing clash
- B6: Validation → Run validate_fixtures()
- B9: Auto-regen → Add team after fixtures generated

### Cyclomatic Complexity
Your `generate_round_robin_pairs()` and `balance_home_away_rotation()` functions have complexity ≥10 for assessment purposes.

---

## Member C (Neel) - Ranking, Results & Presentation

**Your folder:** `member_c_neel/`

### Your Responsibilities
1. Recording match results (C1)
2. Updating league table (C2)
3. Tie-breaking rules (C3)
4. Displaying rankings (C4)
5. Team form analysis (C5)
6. Weekly fixture views (C6)
7. CLI interface (C7)
8. Exporting standings (C8)
9. Head-to-head statistics (C9)

### Key Files
- `results_manager.py` - Your main implementation
- `../src/domain/table.py` - Ranking logic

### Testing Your Code
```powershell
# Quick test
python quick_start.py  # See table in action

# Manual test via CLI
python src/ui/cli.py
# Then: Create league → Add teams → Generate fixtures → Record results → View table
```

### User Stories to Demo
- C1: Record result → Enter match scores
- C4: View table → Show formatted league table
- C3: Tie-breaking → Show teams with equal points sorted by GD
- C5: Team form → Show W/D/L and last 5 results
- C9: Head-to-head → Compare two teams directly

### Tie-Breaking Order
1. Points (descending)
2. Goal difference (descending)
3. Goals scored (descending)
4. Alphabetical by name

---

## Member D (Dhawal) - Diagnostics, Analytics & Testing

**Your folder:** `member_d_dhawal/`

### Your Responsibilities
1. Detect scheduling anomalies (D1)
2. Analyse team workload distribution (D2)
3. Identify fixture congestion zones (D3)
4. Pre-match rule compliance checker (D4)
5. Predict outcome trends using statistical indicators (D5)
6. Generate end-of-season summary reports (D6)
7. Automated boundary & partition test data generator (D7)
8. Coverage-aware test harness (D8)
9. Symbolic path discovery helper (D9)

### Key Files
- `diagnostics_engine.py` - Your main implementation (1400+ lines)
- `../src/domain/*.py` - Shared domain models (Team, Match, League)
- `../tests/generated/*.py` - Auto-generated test files (D7)
- `../data/diagnostics/*.json` - Generated diagnostic reports

### Testing Your Code
```powershell
# Quick test
python -c "from member_d_dhawal import DiagnosticsEngine; d=DiagnosticsEngine(); print(d.get_diagnostics_summary())"

# Full demo
python member_d_demo.py
```

### User Stories to Demo
- D1: Anomalies → Detect duplicate matches, invalid team refs, incomplete rounds
- D2: Workload → Calculate travel distances using fictional coordinates
- D3: Congestion → Identify weeks with tightly packed fixtures
- D4: Compliance → Check rest days, consecutive away games, repeated opponents
- D5: Trends → Statistical predictions (win probability, momentum, form)
- D6: Summary → Top scorers, biggest wins, clean sheets, season stats
- D7: Test Gen → Auto-generate boundary/partition/random test cases
- D8: Harness → Simulated test runner with coverage reporting
- D9: Paths → Extract branches and calculate cyclomatic complexity

### Functions with High Cyclomatic Complexity (CC > 10)
Your module includes several complex diagnostic functions:
- `detect_scheduling_anomalies()` - 8+ decision branches
- `analyse_team_workload()` - 10+ branches for travel/congestion calculations

### Sample Usage
```python
from member_d_dhawal import DiagnosticsEngine
from member_a_mahir import LeagueManager

# Setup
league_mgr = LeagueManager()
league_mgr.create_league("Premier League", "2024-2025")
league = league_mgr.current_league

diagnostics = DiagnosticsEngine()

# D1: Find anomalies
anomalies = diagnostics.detect_scheduling_anomalies(league)
for a in anomalies:
    print(f"{a.severity}: {a.description}")

# D2: Workload analysis
workload = diagnostics.analyse_team_workload(league)
for wm in workload:
    print(f"{wm.team_name}: {wm.total_distance:.0f}km, {wm.max_consecutive_away} away")

# D3: Congestion
congestion = diagnostics.identify_fixture_congestion(league, congestion_threshold=3)

# D4: Rule compliance
violations = diagnostics.check_rule_compliance(league, min_rest_days=3)

# D5: Trends
trends = diagnostics.predict_outcome_trends(league, window_size=5)

# D6: Season summary
summary = diagnostics.generate_season_summary(league)
print(summary['statistics'])

# D7: Generate test data
test_data = diagnostics.generate_test_data(
    "validate_fixture",
    {"home_id": "string", "away_id": "string", "week": "int"}
)
# Creates: tests/generated/test_validate_fixture.py

# D8: Test harness
results = diagnostics.run_test_harness("all", coverage_threshold=0.8)

# D9: Symbolic paths
function_src = '''def check_clash(t1, t2, week, matches):
    if not matches:
        return False
    for m in matches:
        if m.week == week and (m.home == t1 or m.away == t1):
            return True
    return False'''

paths = diagnostics.extract_symbolic_paths(function_src, "check_clash")
print(f"CC: {paths['cyclomatic_complexity']}, Paths: {paths['estimated_paths']}")
```

### Data Files Generated
All diagnostics save to `data/diagnostics/`:
- `anomalies_*.json` - D1 results
- `workload_*.json` - D2 results  
- `congestion_*.json` - D3 results
- `compliance_*.json` - D4 results
- `trends_*.json` - D5 results
- `season_summary_*.json` - D6 results
- `test_harness_*.json` - D8 results
- `symbolic_paths_*.json` - D9 results

Test files go to `tests/generated/`:
- `test_data_*.json` - Generated test case data
- `test_*.py` - Python test file templates

---

## Integration Points Between Members

### A → B (League to Scheduling)
```python
# Member A creates league
league = league_mgr.current_league

# Member B receives it
scheduler = FixtureScheduler(league)
```

### B → C (Fixtures to Results)
```python
# Member B generates fixtures (stored in league.matches)
scheduler.generate_fixtures()

# Member C uses same league
results_mgr = ResultsManager(league)
results_mgr.record_result(match_id, 2, 1)
```

### All → D (Everyone to Metrics)
```python
# Member D works independently
metrics = MetricsEngine()
metrics.calculate_evm(80, 100, 85)
```

---

## Common Commands for All Members

### Run Integration Test
```powershell
python tests/test_integration.py
```

### Run Quick Demo
```powershell
python quick_start.py
```

### Run Full CLI
```powershell
python src/ui/cli.py
```

### Check Your Code Works
```powershell
# For Member A
python -c "from member_a_mahir import LeagueManager; print('✓')"

# For Member B
python -c "from member_b_abhishek import FixtureScheduler; print('✓')"

# For Member C
python -c "from member_c_neel import ResultsManager; print('✓')"

# For Member D
python -c "from member_d_dhawal import MetricsEngine; print('✓')"
```

### Run Tests with Coverage
```powershell
pip install pytest pytest-cov
pytest --cov=member_a_mahir --cov=member_b_abhishek --cov=member_c_neel --cov=member_d_dhawal tests/
```

---

## Sprint Work Distribution

### Sprint 1 (27 Nov - 3 Dec)
**Focus:** Core league, teams, basic fixtures  
**Primary:** Mahir (A), Abhishek (B)  
**Support:** All members review PRs

### Sprint 2 (4 Dec - 10 Dec)
**Focus:** Constraints, ranking, tests  
**Primary:** Neel (C), Dhawal (D)  
**Support:** All members review PRs

### Sprint 3 (11 Dec - 17 Dec)
**Focus:** Metrics, coverage, QA  
**Primary:** All members collaborate

### Sprint 4 (18 Dec - 20 Dec)
**Focus:** Symbolic/concolic, docs, video  
**Primary:** All members finalize

---

## Files Each Member Should Focus On

### Member A (Mahir)
- ✏️ `member_a_mahir/league_manager.py`
- 📖 `src/domain/league.py`
- 📖 `src/domain/team.py`

### Member B (Abhishek)
- ✏️ `member_b_abhishek/fixture_scheduler.py`
- ✏️ `src/scheduling/scheduler.py`
- 📖 `src/domain/match.py`

### Member C (Neel)
- ✏️ `member_c_neel/results_manager.py`
- 📖 `src/domain/table.py`
- ✏️ `src/ui/cli.py` (presentation logic)

### Member D (Dhawal)
- ✏️ `member_d_dhawal/metrics_engine.py`
- ✏️ `src/metrics/pert.py`
- ✏️ `src/metrics/cocomo.py`
- ✏️ `src/metrics/evm.py`
- ✏️ `tests/blackbox/*.py`
- ✏️ `tests/whitebox/*.py`

---

## Common Issues & Solutions

### Issue: "Module not found"
**Solution:** Run from project root: `C:\...\Football-league-management\`

### Issue: "No active league"
**Solution:** Create league first (Member A), then pass to other modules

### Issue: "Fixtures not generated"
**Solution:** Validate league has even number of teams (A9 → B1)

### Issue: "Tests fail"
**Solution:** Check you're using correct Python: `python --version`

### Issue: "Import errors"
**Solution:** All modules use `sys.path.insert` to find src/domain

---

## Tips for Success

1. **Test early, test often** - Run integration test after every change
2. **Use the CLI** - It shows how all modules work together
3. **Read INTEGRATION.md** - Understand data flow between modules
4. **Follow PEP 8** - Keep code clean and readable
5. **Document changes** - Update docstrings when adding features
6. **Collaborate** - All members participate each sprint
7. **Validate inputs** - Use domain model validation methods
8. **Share the League object** - Don't create duplicates

---

## Questions? Check These Files

- **How does it all fit together?** → `INTEGRATION.md`
- **What features are implemented?** → `PROJECT_SUMMARY.md`
- **How do I run it?** → `README.md`
- **What's the process?** → `docs/CMMI2.md`
- **Quick demo?** → `quick_start.py`

---

**Good luck with your development and testing!**
