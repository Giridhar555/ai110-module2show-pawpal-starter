# Model Card for PawPal+ Applied AI System

## Limitations and biases

- The planner uses a tiny, hand-crafted knowledge base rather than a learned language model. This means it can only guide tasks by a fixed set of categories and may miss meaningful distinctions in user input.
- Task categories are manually selected in the UI, so incorrect category labels can cause the planner to boost the wrong tasks.
- The system assumes a single-day schedule and does not model complex multi-day dependencies or overlapping durations beyond its simple slot search.
- It is biased toward medication and feeding tasks by design; that is intentional for safety, but it may deprioritize other valid care needs too much in some cases.

## Potential misuse and prevention

- Misuse: A user could enter incorrect task categories or exaggerate priority to force the planner to schedule a task that is not genuinely urgent.
- Prevention: The app includes explicit task categories and visible planning traces, so users can verify why a task received a boost. Additional guardrails could include validation rules and category explanations in the UI.
- Misuse: A schedule could be treated as a guarantee instead of a recommendation.
- Prevention: The UI warns about skipped tasks and conflict warnings, and the planner reports a confidence score to signal uncertainty.

## Surprises during testing

- I was surprised that a simple category boost mechanism was enough to improve planner behavior without adding any external model dependency.
- I also learned that trace logging makes the system feel more trustworthy, even when the underlying logic is still fairly deterministic.

## AI collaboration

- Helpful suggestion: The AI helped generate a clean Python class design for the scheduler and task model, which saved time during the initial implementation.
- Flawed suggestion: One AI suggestion initially proposed conflict detection based only on exact start times, which would not capture overlapping durations. I corrected that by preserving scheduling slot handling and adding a resolution pass.

## Testing results

- Automated tests: 11 passed.
- Coverage focus: planner decision trace, category-based task boosts, schedule feasibility, conflict detection, and skipped-task handling.
- Human review: I validated that the Streamlit UI displays the confidence score and reasoning trace clearly.
