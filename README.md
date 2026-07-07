# PawPal+ (Module 2 Project)

PawPal+ is a Streamlit app that helps a pet owner plan daily care tasks for one or more pets. The backend uses Python classes and a simple scheduling algorithm to prioritize important routines, avoid conflicts, and explain why a task made it into the plan.

## Features

- Lets a user enter owner and pet information.
- Lets a user add care tasks with duration, priority, and preferred start times.
- Builds a daily schedule based on time limits and priority.
- Sorts tasks by preferred start time and filters them by pet or completion status.
- Warns about conflicts when two tasks share the same start time.
- Supports daily or weekly recurring tasks that create a follow-up occurrence after completion.
- Includes automated tests for core scheduling behavior.

## Project structure

- [app.py](app.py) — the Streamlit UI.
- [pawpal_system.py](pawpal_system.py) — the backend model and scheduler.
- [tests/test_pawpal.py](tests/test_pawpal.py) — automated tests for core behaviors.
- [tests/test_pawpal_system.py](tests/test_pawpal_system.py) — additional scheduler tests.
- [diagrams/uml_final.mmd](diagrams/uml_final.mmd) — final Mermaid UML diagram.

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

## Sample output

```text
Today's Schedule
====================
08:00 — Morning walk (30 min, high priority)
08:30 — Medication (15 min, high priority)
08:45 — Brushing (12 min, medium priority)
09:00 — Feeding (10 min, high priority)
```

## Smarter Scheduling

- Sorting behavior: Scheduler.sort_by_time() orders tasks by preferred start hour and title.
- Filtering behavior: Scheduler.filter_tasks() filters tasks by pet name and completion status.
- Conflict detection logic: Scheduler.detect_conflicts() warns when two tasks share the same start time.
- Recurring task logic: Task.mark_complete() creates the next occurrence for daily or weekly tasks.

## Testing PawPal+

Run the automated test suite with:

```bash
python3 -m pytest
```

The tests cover:
- task completion updates
- task addition on pets
- sorting by preferred start time
- filtering by pet and completion status
- recurring-task follow-up behavior
- conflict detection for duplicate start times

Sample output:

```text
..........
9 passed in 0.01s
```

Confidence level: ⭐⭐⭐⭐⭐

## Demo walkthrough

1. Open the app in Streamlit and enter owner and pet details.
2. Add one or more pets and then add care tasks with durations, priorities, and preferred start times.
3. Review the sorted task list and incomplete-task summary shown for the active pet.
4. Click Generate schedule to create a daily plan, view the planned tasks, and read the scheduler explanation.
5. If a conflict is detected, the app shows a warning so the owner can adjust the plan.

Sample CLI output from running main.py:

```text
Today's Schedule
====================
08:00 — Morning walk (30 min, high priority)
08:30 — Medication (15 min, high priority)
08:45 — Brushing (12 min, medium priority)
09:00 — Feeding (10 min, high priority)
```
