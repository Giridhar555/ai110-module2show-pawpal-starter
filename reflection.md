# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

- The initial design centers on five core classes: Owner, Pet, Task, ScheduledTask, and Scheduler.
- Owner stores the daily time budget and preferences, Pet represents the animal being cared for, Task captures a care action, ScheduledTask records the assigned time slot, and Scheduler turns tasks into a daily plan.

**b. Design changes**

- The design stayed mostly consistent, but I refined how tasks are ordered so that equal-priority tasks keep the original input order after sorting by time preference.
- This change made the scheduling behavior more predictable and aligned with the tests.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- The scheduler considers task priority, preferred start hour, total available daily minutes, and conflicts between overlapping tasks.
- Priority mattered most because it reflects urgency, while time availability and start preferences influence when a task is placed.

**b. Tradeoffs**

- One tradeoff is that the scheduler favors important tasks first and may leave lower-priority items unscheduled when time runs out.
- It also only flags exact start-time conflicts, rather than checking for overlapping durations, which keeps the logic lightweight and easy to reason about.
- That tradeoff is reasonable for a pet-care assistant because urgent routines such as medication should be protected before optional tasks.

---

## 3. AI Collaboration

**a. How you used AI**

- I used AI to brainstorm the class structure, generate the initial backend skeleton, and refine the Streamlit connection.
- The most helpful prompts were ones that asked for Python class designs, test cases, and UI integration steps.
- The most effective AI features were rapid code generation, test drafting, and quick explanation of unfamiliar Python patterns.

**b. Judgment and verification**

- I did not accept the first scheduling suggestion as-is because it did not preserve the intended task order in tie cases.
- I verified the behavior by writing tests for priority ordering, available-time limits, and conflict handling.
- I also used separate chat sessions for implementation and testing so that each phase stayed focused and easier to review.
- A good example of human oversight was rejecting an overly complex conflict-detection approach in favor of a lightweight warning system that was easier to understand and maintain.

---

## 4. Testing and Verification

**a. What you tested**

- I tested that high-priority tasks appear before lower-priority tasks, that tasks which do not fit are skipped, and that tasks with conflicts are scheduled into later open slots.
- These tests are important because they protect the core scheduling logic from regressions.

**b. Confidence**

- I am moderately confident that the current scheduler works correctly for the core scenarios covered by the tests.
- If I had more time, I would add tests for recurring tasks across multiple days and for very long task lists.

---

## 5. Reflection

**a. What went well**

- I am most satisfied with the way the backend, tests, and UI now fit together into one working demo.

**b. What you would improve**

- I would add richer task categories, owner preferences, and a more advanced scheduler that can suggest better placement around recurring routines.

**c. Key takeaway**

- One important lesson was that a strong system design is easier to implement and verify when the data model and test cases are aligned from the start.
