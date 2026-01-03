# Football League Management System

Course project (CO7095 – Software Measurement & Quality Assurance). Compact guide for setup, running, and structure.

---

## Quick Start

- Windows: double-click START.bat
- Mac/Linux/any terminal: `python start.py`

The starter checks Python, installs requirements, and opens an interactive menu (run app, run tests, project info).

---

## Manual Setup (if not using start.py)

```bash
python -m pip install -r requirements.txt
```

Python 3.11+ recommended.

---

## Run the Application

- Preferred: use the menu from START.bat / `python start.py` and choose option 1.
- Direct CLI (bypasses menu): `python src/ui/cli.py`

---

## Run Tests

- From menu: option 2 (all or per-member). Coverage option also available there.
- Direct: `python -m pytest tests -v`
- Direct with coverage: `python run_tests.py coverage`

All 55 tests currently pass.

---

## Folder Structure (key paths)

```
root/
├─ start.py          # main entry point (menu)
├─ START.bat         # Windows launcher
├─ run_tests.py      # test runner helper
├─ requirements.txt  # dependencies
├─ src/              # shared domain + CLI
│  ├─ domain/        # Team, Match, League, Table
│  ├─ scheduling/    # scheduling algorithms
│  └─ ui/cli.py      # interactive CLI
├─ member_a_Neel/    # league & team management
├─ member_b_Mahir/   # fixture scheduler
├─ member_c_Abhishek/# results & standings
├─ member_d_dhawal/  # diagnostics & analytics
├─ tests/            # ~55 pytest cases
└─ docs/, data/      # reports and sample data
```

---

## Module Highlights (one-liners)

- Member A: create league, add/edit teams, validate before scheduling.
- Member B: generate/validate fixtures, reschedule matches, team views.
- Member C: record results, compute standings, display tables/forms.
- Member D: detect anomalies, workload/congestion checks, reports.

---

## Usage Tips

- Use names ≥3 chars when creating a league (validation rule).
- Ensure at least 4 teams before generating fixtures.
---

## Contact

Neel (A), Mahir (B), Abhishek (C), Dhawal (D).
