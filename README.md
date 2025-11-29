# Football League Scheduling System

**CO7095 – Software Measurement & Quality Assurance**  
**University Module Project**

A comprehensive Football League Management System implementing Agile, software measurement, and testing techniques.

## Team Members

- **Mahir** - League & Team Management (Member A)
- **Abhishek** - Scheduling Engine & Constraints (Member B)
- **Neel** - Ranking, Results & Presentation (Member C)
- **Dhawal** - Metrics, Testing & Symbolic/Concolic Analysis (Member D)

## Project Structure

```
root/
├── src/                          # Shared domain models
│   ├── domain/                   # Core entities (Team, Match, League, Table)
│   ├── scheduling/               # Scheduling algorithms
│   └── ui/                       # CLI integration layer
├── data/
│   └── diagnostics/              # Diagnostic reports and analytics output
├── member_a_mahir/               # League & Team Management Module
├── member_b_abhishek/            # Scheduling Engine Module
├── member_c_neel/                # Results & Ranking Module
├── member_d_dhawal/              # Metrics & Testing Module
├── tests/                        # Test suites
│   ├── blackbox/                 # Black-box tests
│   └── whitebox/                 # White-box tests
├── docs/                         # Sprint documentation
│   ├── sprint0/, sprint1/, ...
│   └── CMMI2.md                  # CMMI Level 2 documentation
├── data/                         # Saved leagues and metrics
├── requirements.txt              # Python dependencies
└── README.md                     # This file
```

## Features by Member

### Member A (Mahir) - League & Team Management
- ✅ A1: Create League
- ✅ A2: Add Team
- ✅ A3: Validate Duplicate Teams
- ✅ A4: Remove/Edit Team
- ✅ A5: Persist League & Team Data (JSON)
- ✅ A6: Team Data Validation Rules
- ✅ A7: Load Existing League
- ✅ A8: Export League State
- ✅ A9: Validate League Configuration Before Scheduling

### Member B (Abhishek) - Scheduling Engine
- ✅ B1: Generate Round-Robin Fixtures
- ✅ B2: Generate Home/Away Rotation
- ✅ B3: Week-by-Week Schedule Generation
- ✅ B4: Prevent Same-Week Clashes
- ✅ B5: Reschedule a Match
- ✅ B6: Validate Fixture Integrity
- ✅ B7: View Full Fixture List
- ✅ B8: Team-Specific Fixture View
- ✅ B9: Auto-Regenerate Fixtures After Team Changes

### Member C (Neel) - Ranking & Results
- ✅ C1: Record Match Result
- ✅ C2: Update League Table
- ✅ C3: Ranking Tie-Breaking Rules
- ✅ C4: Display League Table
- ✅ C5: Team Form & Performance Summary
- ✅ C6: Weekly Fixtures View
- ✅ C7: Basic UI Interface (CLI)
- ✅ C8: Export Results/Standings
- ✅ C9: Head-to-Head Statistics Dashboard

### Member D (Dhawal) - Diagnostics & Analytics
- ✅ D1: Detect Scheduling Anomalies
- ✅ D2: Analyse Team Workload Distribution
- ✅ D3: Identify Fixture Congestion Zones
- ✅ D4: Pre-Match Rule Compliance Checker
- ✅ D5: Predict Outcome Trends
- ✅ D6: Generate End-of-Season Summary
- ✅ D7: Automated Test Data Generator
- ✅ D8: Coverage-Aware Test Harness
- ✅ D9: Symbolic Path Discovery Helper

## Installation

```powershell
# Clone the repository
git clone <repository-url>
cd Football-league-management

# Create virtual environment (recommended)
python -m venv venv
.\venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt
```

## Usage

### Run the CLI Application

```powershell
python src/ui/cli.py
```

### Quick Start Example

1. **Create a League**:
   - Choose option 1
   - Enter league name (e.g., "Premier League")
   - Enter season (e.g., "2024-2025")

2. **Add Teams** (minimum 4 teams):
   - Choose option 2
   - Add teams with names and stadiums

3. **Generate Fixtures**:
   - Choose option 11
   - System validates league and generates round-robin schedule

4. **Record Match Results**:
   - Choose option 21
   - Enter match ID and scores

5. **View League Table**:
   - Choose option 22

### Individual Member Modules

Each member's code can be imported and used independently:

```python
# Member A - League Management
from member_a_mahir.league_manager import LeagueManager
manager = LeagueManager()
manager.create_league("Test League", "2024")

# Member B - Scheduling
from member_b_abhishek.fixture_scheduler import FixtureScheduler
scheduler = FixtureScheduler(league)
scheduler.generate_fixtures()

# Member C - Results
from member_c_neel.results_manager import ResultsManager
results = ResultsManager(league)
results.view_table()

# Member D - Diagnostics
from member_d_dhawal.diagnostics_engine import DiagnosticsEngine
diagnostics = DiagnosticsEngine(league)
anomalies = diagnostics.detect_scheduling_anomalies()
```

## Testing

### Run All Tests

```powershell
pytest tests/ -v
```

### Run with Coverage

```powershell
pytest --cov=src --cov=member_a_mahir --cov=member_b_abhishek --cov=member_c_neel --cov=member_d_dhawal --cov-report=html tests/
```

### Coverage Report

```powershell
# View HTML coverage report
start htmlcov/index.html
```

## Diagnostics & Analytics

### Detect Scheduling Anomalies
```python
from member_d_dhawal.diagnostics_engine import DiagnosticsEngine
engine = DiagnosticsEngine(league)
anomalies = engine.detect_scheduling_anomalies()
```

### Analyse Team Workload
```python
workload = engine.analyse_team_workload_distribution()
print(f"Team with most travel: {workload.teams[0].name} ({workload.teams[0].travel_km:.0f} km)")
```

### Identify Fixture Congestion
```python
congestion = engine.identify_fixture_congestion_zones(window_days=7)
print(f"Congested periods: {len(congestion.congested_periods)}")
```

### Predict Outcome Trends
```python
trends = engine.predict_outcome_trends()
for team_trend in trends.team_trends:
    print(f"{team_trend.team_name}: {team_trend.win_probability*100:.1f}% win probability")
```

## Documentation

- **CMMI Level 2**: See `docs/CMMI2.md`
- **Sprint Plans**: See `docs/sprint0/`, `docs/sprint1/`, etc.
- **User Stories**: See CMMI2.md Section 9

## Integration & Consistency

All member modules share the same domain models (`src/domain/`) ensuring:
- Consistent data structures (Team, Match, League)
- Seamless integration across modules
- Type-safe interactions
- Single source of truth for league state

## Sprint Timeline

| Sprint | Dates | Focus | Members |
|--------|-------|-------|---------|
| 0 | Pre-27 Nov | Planning, backlog, CMMI setup | All |
| 1 | 27 Nov - 3 Dec | League, teams, fixtures | Mahir, Abhishek |
| 2 | 4 Dec - 10 Dec | Constraints, ranking, tests | Neel, Dhawal |
| 3 | 11 Dec - 17 Dec | Metrics, coverage, QA | All |
| 4 | 18 Dec - 20 Dec | Symbolic/concolic, docs, video | All |

## Development Standards

- **Python Version**: 3.11+
- **Code Style**: PEP 8 (enforced with `black` and `pylint`)
- **Testing**: `pytest` with minimum 75% coverage for scheduling, 85% for metrics
- **Documentation**: Docstrings for all public methods
- **Version Control**: Git with feature branches and PR reviews

## License

This project is developed for educational purposes as part of CO7095 coursework.

## Contact

For questions or issues, contact the development team:
- Mahir (Member A)
- Abhishek (Member B)
- Neel (Member C)
- Dhawal (Member D)
