# PawPal+ Applied AI Project Presentation

## Slide 1: Title
- **PawPal+ Applied AI Pet Care Planner**
- Extended from the Module 2 pet-scheduling starter project
- Built by Giridhar

## Slide 2: Problem Statement
- Many pet owners struggle to manage daily care tasks across multiple pets.
- Important routines such as medication, feeding, and exercise can be missed.
- Existing tools rarely explain why a plan was chosen or how confident it is.

## Slide 3: Solution Overview
- PawPal+ is a Streamlit app that collects owner, pet, and task data.
- It creates a daily care schedule using priority, preferred time, and available minutes.
- The system now includes an AI-style planner that guides scheduling with category knowledge.

## Slide 4: System Architecture
- `app.py`: user interface and plan presentation
- `pawpal_system.py`: backend model, scheduler, knowledge base, and planner
- `main.py`: CLI demo for the planner workflow
- `tests/`: automated reliability checks
- `diagrams/system_architecture.mmd`: architecture source

## Slide 5: AI Features
- Retrieval-style guidance from `CareKnowledgeBase`
- Category-based priority boosts for medication, feeding, walks, and grooming
- Conflict detection and secondary resolution pass
- Planner trace logging and confidence scoring

## Slide 6: Reliability and Testing
- Added tests for planner behavior and scheduler correctness
- `python -m pytest` passes: `11 passed`
- Confidence score helps users understand plan reliability
- Trace output makes decisions transparent

## Slide 7: Demo Flow
- Enter owner profile and availability
- Add pets and care tasks with categories, duration, and preferred time
- Generate the daily plan
- Review scheduled tasks, skipped tasks, warnings, confidence, and planner trace

## Slide 8: Lessons and Impact
- Simple AI workflows improve user trust without external models
- Transparency makes scheduling decisions easier to accept
- This applied AI system turns a static scheduler into a more responsible planner

## Slide 9: Repository and Files
- GitHub: `https://github.com/Giridhar555/ai110-module2show-pawpal-starter`
- Key files:
  - `README.md`
  - `model_card.md`
  - `diagrams/system_architecture.mmd`
  - `tests/test_pawpal_planner.py`
  - `app.py`, `pawpal_system.py`, `main.py`

## Slide 10: Thank you
- Questions?
- Contact information or next steps
