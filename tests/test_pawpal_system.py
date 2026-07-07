from pawpal_system import Owner, Pet, Task, Scheduler


def test_scheduler_prioritizes_high_priority_tasks():
    owner = Owner(name="Jordan", daily_available_minutes=240)
    pet = Pet(name="Mochi", species="dog", owner=owner)
    scheduler = Scheduler()

    tasks = [
        Task(title="Grooming", duration_minutes=20, priority="low", category="grooming"),
        Task(title="Medication", duration_minutes=15, priority="high", category="medication"),
    ]

    plan = scheduler.build_daily_plan(owner, pet, tasks)

    assert [task.title for task in plan.scheduled_tasks] == ["Medication", "Grooming"]


def test_scheduler_skips_tasks_that_do_not_fit():
    owner = Owner(name="Taylor", daily_available_minutes=60)
    pet = Pet(name="Luna", species="cat", owner=owner)
    scheduler = Scheduler(day_start_hour=8, day_end_hour=9)

    tasks = [
        Task(title="Long walk", duration_minutes=50, priority="high", category="walk"),
        Task(title="Feeding", duration_minutes=20, priority="medium", category="feeding"),
    ]

    plan = scheduler.build_daily_plan(owner, pet, tasks)

    assert [task.title for task in plan.scheduled_tasks] == ["Long walk"]
    assert plan.unscheduled_tasks[0].title == "Feeding"


def test_scheduler_handles_conflicts_and_recurring_tasks():
    owner = Owner(name="Avery", daily_available_minutes=180)
    pet = Pet(name="Pip", species="other", owner=owner)
    scheduler = Scheduler(day_start_hour=8, day_end_hour=12)

    tasks = [
        Task(title="Morning walk", duration_minutes=30, priority="high", category="walk", preferred_start_hour=8),
        Task(title="Medication", duration_minutes=20, priority="high", category="medication", preferred_start_hour=8),
        Task(title="Daily brushing", duration_minutes=10, priority="medium", category="grooming", recurring=True),
    ]

    plan = scheduler.build_daily_plan(owner, pet, tasks)

    scheduled_titles = [task.title for task in plan.scheduled_tasks]

    assert "Morning walk" in scheduled_titles
    assert "Medication" in scheduled_titles
    assert "Daily brushing" in scheduled_titles
    assert plan.scheduled_tasks[0].title == "Morning walk"
