# CMMI Level 2 Documentation Framework

CO7095 – Software Measurement & Quality Assurance

Project: Football League Scheduling System

Team Members: Mahir, Abhishek, Neel, Dhawal

Sprints: 1 week each, starting 27 November

---

**Executive Summary:**

This document captures the CMMI Level 2-compliant process framework, artifacts, measurement and QA practices for the Football League Scheduling System project. It summarises how requirements are managed, how planning and monitoring are executed, and how configuration and quality assurance are enforced. All four team members participate in every sprint—work is assigned with clear ownership, but collaboration and peer-review are required for all key activities.

**1. Requirements Management**

- **Policy:** All functional and non-functional requirements are recorded as user stories using the canonical format: “As a <role>, I want <capability> so that <benefit>.”
- **Storage & Traceability:** Every user story is a GitHub Issue and is linked to commits, PRs, test cases and the project board card. Issues are labeled by sprint and component.
- **Workflow:** Stories progress through the GitHub Project Board stages: `Backlog → Selected for Sprint → In Progress → In Review → Done`.
- **Assignment & Ownership:** Each story has an assigned owner (one of the four members) responsible for implementation, plus at least one reviewer.
- **Evidence (Sprint 0):**
  - `/docs/sprint0/userstories_list.png` — full set of 32 user stories
  - `/docs/sprint0/projectboard_backlog.png` — initial backlog snapshot
  - `/docs/sprint0/story_mapping_matrix.md` — mapping of stories to owners

**Practices:**
- Enforce clear acceptance criteria for each story.
- Require trace links from Issue → branch → PR → CI run → tests.
- Use story-level labels for priority and risk.

**2. Project Planning**

**2.1 Sprint Schedule**

All sprints are one week long and begin 27 November. Every sprint includes participation from all team members — ownership rotates but cross-review and pairing are enforced so the entire team is familiar with core components.

| Sprint | Dates | Goal | Owner Focus | Stories Planned | Stories Completed |
|---|---|---|---:|---:|---:|
| 1 | 27 Nov – 3 Dec | Core league creation, team management, basic fixtures | Mahir & Abhishek (lead) | 12 | TBD |
| 2 | 4 Dec – 10 Dec | Scheduling constraints, ranking, black-box + white-box tests | Neel & Dhawal (lead) | 12 | TBD |
| 3 | 11 Dec – 17 Dec | Metrics (PERT, COCOMO, EVM), coverage, exports, QA | All Members (collaborative) | 12 | TBD |
| 4 (Docs) | 18 Dec – 20 Dec | Symbolic & concolic testing, final video & documentation | All Members (finalisation) | - | - |

**2.2 Planning Artifacts**

- Planning Poker estimates: `/docs/sprint0/planning_poker_estimations.png`.
- Team capacity: average availability 12–15 productive hours/week. Expected velocity: 20–25 points per sprint.
- Tools & technology: Python 3.11+, PyCharm/VSCode, `pytest`, `coverage.py`, GitHub Projects.

**Risk Register**

| Risk | Impact | Likelihood | Mitigation |
|---|---:|---:|---|
| Scheduler complexity underestimated | High | Medium | Break story into smaller tasks; pair-program; early prototype |
| Test coverage below requirement | Medium | Medium | Add tests early; define coverage gates; concolic/symbolic tasks in sprint 4 |
| Availability issues | Medium | High | Reassign story owners quickly; keep cross-training docs |
| Metric formula accuracy | Low | Low | Peer review and validation of metric calculations |

**3. Project Monitoring & Control**

Monitoring is quantitative and time-boxed. The team uses Agile metrics and formal sprint controls to detect deviations early.

- Daily updates and standups with action items.
- Daily burndown charts (stored under `/docs/sprintX/`).
- Velocity tracking per sprint; trend analysis after each sprint.
- EVM metrics (PV, EV, AC, SPI, CPI) captured in `/docs/metrics/`.
- Sprint ceremonies: planning, daily stand-up, review, and retrospective.

**Sprint 1 Monitoring Template (to complete after sprint 1):**

- Completed Stories: (list of IDs)
- Velocity: Completed Points / Planned Points
- EVM snapshot: PV, EV, AC, SPI, CPI
- Evidence:
  - `/docs/sprint1/sprint1_board_end.png`
  - `/docs/sprint1/pr_reviews.png`
  - `/docs/sprint1/burndown_sprint1.png`
  - `/docs/sprint1/velocity_sprint1.png`

**4. Configuration Management**

Branching strategy and policies are strict to ensure reproducibility.

- Branch model:
  - `main` — stable, protected
  - `dev` — integration
  - `feature/<issue-id>-<short-title>` — story branches
- Policies:
  - No direct commits to `main`.
  - Every PR requires at least one reviewer.
  - All commits reference their Issue ID in the message.
  - Version tags applied at sprint end (e.g., `v0.1-sprint0`, `v1.0-sprint1`, ...).
- Evidence:
  - `/docs/sprint0/branches_proof.png`
  - `/docs/sprint1/pr_review_flow.png`

**5. Process & Product Quality Assurance**

QA is enforced via testing, reviews, automation and coverage gates.

**Test Strategy**

| Test Type | Focus | Tool | Owner | Sprint |
|---|---|---|---:|---:|
| Black-Box | Partitioning, boundary, random | `pytest` | Dhawal | 2 |
| White-Box | Branch & basis path | `pytest` + `coverage` | Neel | 2 & 3 |
| Symbolic | Tree, constraints | Manual + Python helpers | Abhishek | 4 |
| Concolic | Concrete + symbolic | Custom scripts | Mahir | 4 |

QA Activities:
- Mandatory PR reviews and sign-off.
- Linting and formatting checks in CI.
- Coverage targets:
  - ≥ 75% for core scheduling modules (`src/scheduling`)
  - ≥ 85% for metrics modules (`src/metrics`)

**6. Measurement & Analysis**

Measurement drives both project control and learning outcomes for CO7095.

Implemented metrics (files referenced):
- PERT — expected duration & variance: `src/metrics/pert.py` and `/docs/metrics/pert_diagram.png`.
- COCOMO I/II — effort & cost: `src/metrics/cocomo.py` and `/docs/metrics/cocomo.xlsx`.
- EVM — EV/PV/AC/SPI/CPI: `src/metrics/evm.py` and `/docs/metrics/evm_sprint3.xlsx`.
- Velocity — sprint performance charts: `/docs/sprintX/velocity.png`.
- Coverage — HTML reports: `/docs/sprintX/coverage_report.html`.

All metric outputs are stored under `/docs/metrics/` and cross-referenced in sprint reviews.

**7. Sprint Evidence Index**

| Sprint | Folder | Key Artifacts |
|---|---|---|
| 0 | `/docs/sprint0` | Backlog, planning poker, CMMI doc, branching evidence |
| 1 | `/docs/sprint1` | League creation, fixtures, PR logs, burndown, velocity |
| 2 | `/docs/sprint2` | Constraints, ranking, black-box & white-box tests |
| 3 | `/docs/sprint3` | Metrics engine, coverage reports, exports, QA artifacts |
| 4 | `/docs/sprint4` | Symbolic execution trees, concolic testing report, final docs & video |

**8. Continuous Improvement Statement**

After every sprint the team performs a retrospective that documents:
- What went well
- What did not go well
- Risks encountered
- Improvement actions (owner and target sprint)

These retrospectives feed process improvements, which are then implemented in the next sprint to satisfy the CMMI Level 2 Managed Process requirements.

**9. Roles, Responsibilities and Story Allocation**

All members participate in every sprint; primary ownership rotates but all members review, test and contribute to integration. Below is the canonical set of user stories and the primary member assignment groups (each member remains responsible for their primary area but collaborates broadly):

- Member A — League & Team Management (Lead: Mahir)
  - A1 — Create League
  - A2 — Add Team
  - A3 — Validate Duplicate Teams
  - A4 — Remove/Edit Team
  - A5 — Persist League & Team Data
  - A6 — Team Data Validation Rules
  - A7 — Load Existing League
  - A8 — Export League State
  - A9 — Validate League Configuration Before Scheduling

- Member B — Scheduling Engine & Constraints (Lead: Abhishek)
  - B1 — Generate Round-Robin Fixtures
  - B2 — Generate Home/Away Rotation
  - B3 — Week-by-Week Schedule Generation
  - B4 — Prevent Same-Week Clashes
  - B5 — Reschedule a Match
  - B6 — Validate Fixture Integrity
  - B7 — View Full Fixture List
  - B8 — Team-Specific Fixture View
  - B9 — Auto-Regenerate Fixtures After Team Changes

- Member C — Ranking, Results & Presentation (Lead: Neel)
  - C1 — Record Match Result
  - C2 — Update League Table
  - C3 — Ranking Tie-Breaking Rules
  - C4 — Display League Table
  - C5 — Team Form & Performance Summary
  - C6 — Weekly Fixtures View
  - C7 — Basic UI Interface (CLI/Web)
  - C8 — Export Results/Standings
  - C9 — Head-to-Head Statistics Dashboard

- Member D — Metrics, Testing & Symbolic/Concolic Analysis (Lead: Dhawal)
  - D1 — PERT Calculation Module
  - D2 — COCOMO I & II Estimation Module
  - D3 — Earned Value Management (EVM)
  - D4 — Generate Burndown & Velocity Charts
  - D5 — Black-Box Test Suite
  - D6 — White-Box Test Suite
  - D7 — Symbolic Execution of Constraint Function
  - D8 — Concolic Testing for Coverage Improvement
  - D9 — Automated Test Coverage Report Generator

**Note on Collaboration:**
Each story has a primary owner but requires at least one collaborator during implementation and one reviewer during PR. This ensures knowledge sharing and reduces single points of failure.

**10. Evidence and Traceability**

The following evidence artifacts are referenced throughout this document and will be kept under the `/docs` folder and linked from the sprint boards and Issues:

- `/docs/sprint0/*` — backlog, story mapping, planning poker outputs
- `/docs/sprint1/*` — sprint board end snapshot, PR review screenshots, burndown and velocity charts
- `/docs/sprint2/*` — test suites, reports and ranking validations
- `/docs/metrics/*` — PERT, COCOMO, EVM spreadsheets and diagrams

**Appendix A — Template: Sprint Review Metrics**

- Planned points: 
- Completed points: 
- Velocity: Completed/Planned
- Coverage: (per module)
- EVM snapshot: PV / EV / AC / SPI / CPI

---

This CMMI Level 2 framework is intentionally pragmatic: it balances the course learning outcomes for CO7095 with lightweight Agile practices suited to a small team. The policy of full-team participation each sprint ensures robust knowledge sharing and continuous process improvement.
