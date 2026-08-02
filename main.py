from datetime import date

from pawpal_system import CareKnowledgeBase, Owner, Pet, PetCarePlanner, ScheduledTask, Task


def main() -> None:
    owner = Owner(name="Jordan", daily_available_minutes=240)
    pet1 = Pet(name="Mochi", species="dog", owner=owner)
    pet2 = Pet(name="Luna", species="cat", owner=owner)

    owner.add_pet(pet1)
    owner.add_pet(pet2)

    pet1.add_task(Task(title="Morning walk", duration_minutes=30, priority="high", category="walk", preferred_start_hour=8, pet_name=pet1.name))
    pet1.add_task(Task(title="Feeding", duration_minutes=10, priority="high", category="feeding", preferred_start_hour=9, pet_name=pet1.name))
    pet2.add_task(Task(title="Medication", duration_minutes=15, priority="high", category="medication", preferred_start_hour=8, pet_name=pet2.name))
    pet2.add_task(Task(title="Brushing", duration_minutes=12, priority="medium", category="grooming", recurring=True, pet_name=pet2.name))

    planner = PetCarePlanner(knowledge_base=CareKnowledgeBase())
    plan, trace, confidence = planner.plan(owner, pet1, owner.get_all_tasks())

    print("Today's Schedule")
    print("=" * 20)
    for item in planner.scheduler.explain_plan(plan):
        print(item)

    print(f"\nPlanner confidence: {confidence:.2f}")
    print("\nPlanner trace:")
    for line in trace:
        print(f"- {line}")

    print("\nSorted by time:")
    for task in planner.scheduler.sort_by_time(owner.get_all_tasks()):
        print(f"- {task.title} @ {task.preferred_start_hour}:00")

    print("\nFiltered for Mochi, incomplete tasks:")
    for task in planner.scheduler.filter_tasks(owner.get_all_tasks(), pet_name="Mochi", completed=False):
        print(f"- {task.title}")

    recurring_task = Task(title="Pill", duration_minutes=5, priority="high", frequency="daily", due_date=date(2026, 7, 7), pet_name=pet2.name)
    next_occurrence = recurring_task.mark_complete()
    print("\nRecurring task follow-up:")
    print(f"- {recurring_task.title} -> next occurrence: {next_occurrence.due_date if next_occurrence else 'none'}")

    conflict_warning = planner.scheduler.detect_conflicts([
        ScheduledTask(task=Task(title="Walk", duration_minutes=20, priority="high"), start_minute=480, end_minute=500, reason=""),
        ScheduledTask(task=Task(title="Feed", duration_minutes=10, priority="medium"), start_minute=480, end_minute=490, reason=""),
    ])
    print("\nConflict detection:")
    for warning in conflict_warning:
        print(f"- {warning}")


if __name__ == "__main__":
    main()
