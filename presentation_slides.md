# PawPal+ Applied AI Project Presentation

---

## Title

- PawPal+ Applied AI Pet Care Planner
- Extended from the Module 2 pet-scheduling starter project
- Built by Giridhar

---

## Problem Statement

- Pet owners often struggle to manage daily care tasks across multiple pets.
- Important routines like medication, feeding, and exercise can be missed.
- Existing tools rarely explain why a plan was chosen or how confident it is.

---

## Solution Overview

- PawPal+ collects owner, pet, and care task input.
- The app generates a daily schedule using priorities, availability, and preferred times.
- The system now includes an AI-style planner with category knowledge and traceability.

---

## System Architecture

- `app.py` — Streamlit UI for input and plan display.
- `pawpal_system.py` — backend data model, scheduler, knowledge base, and planner.
- `main.py` — CLI demo for the planner workflow.
- `tests/` — automated reliability checks.
- `diagrams/system_architecture.mmd` — architecture and data-flow source.

---

## AI Features

- Retrieval-style guidance from `CareKnowledgeBase`.
- Category-based priority boosts for medication, feeding, walks, and grooming.
- Conflict detection and secondary resolution logic.
- Planner trace logging and confidence scoring for transparency.

---

## Reliability and Testing

- Added planner-specific tests and scheduler verification.
- Project passes `11` automated tests.
- Confidence scores highlight potential schedule uncertainty.
- Trace output shows why each plan decision was made.

---

## Demo Flow

- Enter owner profile and availability.
- Add pets and task details.
- Generate a schedule.
- Review scheduled tasks, skipped tasks, warnings, confidence score, and reasoning trace.

---

## Lessons and Impact

- Small AI workflows can improve deterministic schedulers without external APIs.
- Transparent reasoning builds trust in planning decisions.
- The system evolves a prototype scheduler into a responsible applied AI planner.

---

## Repository and Files

- `https://github.com/Giridhar555/ai110-module2show-pawpal-starter`
- Key files:
  - `README.md`
  - `model_card.md`
  - `diagrams/system_architecture.mmd`
  - `tests/test_pawpal_planner.py`
  - `app.py`, `pawpal_system.py`, `main.py`

---

## Thank You

- Questions?
- Ready for next steps or a live demo.
