# PawPal+ Applied AI Pet Care Planner

PawPal+ started as a Module 2 project for planning pet care tasks with a simple scheduler. This submission extends that prototype into an applied AI system by adding an AI-style planning component that retrieves task guidance, boosts task priority based on category, resolves scheduling conflicts, and reports confidence and traceable reasoning.

## What this project does

PawPal+ helps a pet owner manage and schedule daily care tasks across one or more pets. The system now includes:

- A Streamlit interface for entering owner details, pets, and care tasks.
- An AI-enhanced planner that uses task categories and knowledge retrieval to prioritize medication, feeding, walks, and grooming.
- Traceable reasoning and confidence scoring so users can understand why the plan was chosen.
- A scheduler that builds a daily plan within the owner's available minutes and flags conflicts.

## Original project summary

This project began as a pet-care scheduling assistant from Module 2. Its original goal was to model owners, pets, and care tasks, then turn tasks into a daily plan while avoiding conflicts and honoring preferred start times.

## Architecture overview

The system has three main components:

1. `app.py` — Streamlit UI for user input and plan display.
2. `pawpal_system.py` — backend data model, scheduling engine, knowledge retriever, and planner.
3. `tests/` — automated tests that verify both scheduler correctness and AI planner behavior.

The new `PetCarePlanner` integrates a lightweight knowledge base and a planner workflow to make the scheduler more intelligent and explainable.

See the system diagram: [diagrams/system_architecture.mmd](diagrams/system_architecture.mmd)

## Project structure

- `app.py` — Streamlit interface with task guidance and planner trace output.
- `main.py` — CLI demo for the planner and scheduler.
- `pawpal_system.py` — data model, scheduler, knowledge base, and AI planner.
- `tests/test_pawpal.py` — core behavior tests for tasks, pets, and scheduler utilities.
- `tests/test_pawpal_system.py` — additional scheduler tests.
- `tests/test_pawpal_planner.py` — planner-specific tests and reliability checks.
- `diagrams/system_architecture.mmd` — architecture and data-flow diagram.
- `model_card.md` — responsible AI reflection and limitations.

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Run locally

```bash
streamlit run app.py
```

or run the CLI demo:

```bash
python main.py
```

## Sample interactions

### 1. Planner output for medication and walk

```text
Today's Schedule
====================
08:00 — Medication (15 min, high priority)
08:15 — Morning walk (30 min, medium priority)

Planner confidence: 0.90

- Starting planning for Mochi with 2 task(s).
- Retrieved guidance for 'Medication' (medication): Medication tasks should be scheduled at consistent times and prioritized to avoid missed doses.
- Applied knowledge boost of 1.0 to 'Medication'.
- Retrieved guidance for 'Morning walk' (walk): Walks help pets stay active, but they can often be shifted later if urgent care is needed first.
- Applied knowledge boost of 0.5 to 'Morning walk'.
- Built initial plan with 2 scheduled tasks and 0 skipped tasks.
- No conflicts detected in the initial plan.
- Final confidence score: 0.90
```

### 2. Skipping a task when time is limited

```text
Skipped tasks due to time limits or conflicts:
- Long grooming
```

## AI feature

This project includes an agentic planning workflow with:

- Retrieval from a small knowledge base (`CareKnowledgeBase`).
- Category-based priority boosts for medication, feeding, walk, and grooming tasks.
- Conflict detection and a secondary resolution pass that increases medication priority.
- Confidence scoring based on schedule coverage and conflict warnings.

## Reliability and evaluation

The system is tested with automated unit tests. Key reliability checks include:

- Planner applies category-based boosts and retrieves task guidance.
- Scheduling keeps high-priority tasks earlier when possible.
- Tasks that cannot fit within the owner's available minutes are skipped.
- Confidence is calculated and reported alongside the plan.

Test command:

```bash
python -m pytest
```

Test result:

```text
11 passed in 0.02s
```

### Human evaluation

| Test input | Evaluation criteria | Result |
|------------|--------------------|--------|
| 4 tasks incl. medication + walk at 08:00 | Medication scheduled first, confidence reported | Pass — Medication placed at 08:00, confidence 1.00 |
| Owner with only 20 available minutes | Infeasible task skipped, not silently dropped | Pass — grooming skipped, confidence lowered |
| Generate schedule with no tasks added | Handled gracefully, no crash | Pass — UI warns "Add at least one task" |
| Empty pet name in UI | Rejected with a clear message | Pass — "Please enter a pet name" |

**Summary:** 11/11 automated tests pass. Confidence averages ~1.0 on feasible
plans and drops when tasks are skipped. The planner correctly prioritized
safety-critical tasks in every human-reviewed case; the main limitation is that
task categories are user-supplied, so a mislabeled category can misdirect a boost.

## Design decisions

- I kept the AI component lightweight so the system remains reproducible without external APIs.
- Categories are used as domain knowledge, which helps the planner make more reasonable trade-offs without requiring a full NLP model.
- The planner trace adds transparency and makes scheduling decisions easier to trust.

## What I learned

This project showed me how a small AI workflow can improve a deterministic scheduler by adding knowledge-based task prioritization, traceable reasoning, and confidence scoring. It also reinforced the importance of documenting both the system architecture and the reliability tests for an applied AI portfolio entry.

## Notes

- `model_card.md` contains the formal responsible AI reflection on limitations, bias, misuse, and AI collaboration.
- `diagrams/system_architecture.mmd` contains the architecture source used for the system diagram.
