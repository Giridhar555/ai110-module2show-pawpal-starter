# AI Interactions Log

This file documents the **agentic planning workflow** in PawPal+. The
`PetCarePlanner` runs a multi-step reasoning chain — retrieve guidance, apply
knowledge-based priority boosts, build a plan, check for conflicts, and (if
needed) run a resolution pass — and records every step to a trace. The traces
below are captured directly from `python main.py`.

---

## Agentic Workflow (Planner reasoning trace)

**Task given to the agent:** Turn a list of pet-care tasks into a feasible,
explainable daily schedule that respects the owner's available time, prioritizes
safety-critical tasks (medication, feeding), and reports its confidence.

**Steps the agent takes (plan → act → check):**

1. **Retrieve** category guidance for each task from `CareKnowledgeBase`.
2. **Act** by applying a category-based priority boost (medication 1.0,
   feeding 0.7, walk 0.5, grooming 0.3).
3. **Build** an initial plan with the scheduler.
4. **Check** for conflicts (tasks sharing a start time).
5. **Resolve** — if conflicts exist, bump medication priority and re-plan.
6. **Score** confidence from schedule coverage and remaining conflicts.

### Trace 1 — four tasks, no conflicts (from `python main.py`)

```text
Today's Schedule
====================
08:00 — Medication (15 min, high priority)
08:15 — Morning walk (30 min, high priority)
08:45 — Brushing (12 min, medium priority)
09:00 — Feeding (10 min, high priority)

Planner confidence: 1.00

Planner trace:
- Starting planning for Mochi with 4 task(s).
- Retrieved guidance for 'Morning walk' (walk): Walks help pets stay active, but they can often be shifted later if urgent care is needed first.
- Applied knowledge boost of 0.5 to 'Morning walk'.
- Retrieved guidance for 'Feeding' (feeding): Regular feeding supports pet health; keep feeding tasks early and predictable.
- Applied knowledge boost of 0.7 to 'Feeding'.
- Retrieved guidance for 'Medication' (medication): Medication tasks should be scheduled at consistent times and prioritized to avoid missed doses.
- Applied knowledge boost of 1.0 to 'Medication'.
- Retrieved guidance for 'Brushing' (grooming): Grooming is important for comfort and can be scheduled after higher-priority tasks.
- Applied knowledge boost of 0.3 to 'Brushing'.
- Built initial plan with 4 scheduled tasks and 0 skipped tasks.
- No conflicts detected in the initial plan.
- Final confidence score: 1.00
```

**What the trace shows:** the knowledge boost reorders tasks so Medication is
placed first even though Morning walk shared the same 08:00 preferred start. The
decision chain is fully auditable — each retrieval and boost is logged before the
schedule is built.

### Trace 2 — limited time forces a skip (lower confidence)

Captured from `tests/test_pawpal_planner.py`
(`test_planner_confidence_is_lower_when_tasks_are_skipped`): with only 20
available minutes, a 15-min medication and a 30-min grooming task cannot both
fit. The planner schedules medication, skips grooming, and lowers confidence
below 1.0 — demonstrating the "check" step catching an infeasible plan rather
than silently dropping a task.

---

## What I had to verify or fix manually

- The agent originally proposed conflict detection based only on exact start
  times. That misses overlapping durations, so I kept the scheduler's slot-based
  occupancy check and added a secondary resolution pass. (Also noted in
  `model_card.md`.)
- I verified the reasoning trace is surfaced to the user in the Streamlit UI
  (`app.py`, "Planner trace and AI reasoning" expander), not just printed to the
  console.
