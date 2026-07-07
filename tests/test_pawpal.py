from datetime import date

from pawpal_system import DailyPlan, Owner, Pet, Scheduler, ScheduledTask, Task


def test_mark_complete_updates_status():
    owner = Owner(name="Jordan")
    pet = Pet(name="Mochi", species="dog", owner=owner)
    task = Task(title="Walk", duration_minutes=20, priority="high")
    pet.add_task(task)

    task.mark_complete()

    assert task.completed is True


def test_adding_task_increases_pet_task_count():
    owner = Owner(name="Jordan")
    pet = Pet(name="Mochi", species="dog", owner=owner)

    pet.add_task(Task(title="Feed", duration_minutes=10, priority="medium"))

    assert len(pet.tasks) == 1


def test_scheduler_sort_by_time_orders_tasks_by_preferred_start_hour():
    scheduler = Scheduler()
    tasks = [
        Task(title="Later task", duration_minutes=15, priority="medium", preferred_start_hour=10),
        Task(title="Earlier task", duration_minutes=10, priority="medium", preferred_start_hour=8),
    ]

    ordered = scheduler.sort_by_time(tasks)

    assert [task.title for task in ordered] == ["Earlier task", "Later task"]


def test_scheduler_filters_tasks_by_pet_and_completion_status():
    scheduler = Scheduler()
    owner = Owner(name="Jordan")
    pet_one = Pet(name="Mochi", species="dog", owner=owner)
    pet_two = Pet(name="Luna", species="cat", owner=owner)
    task_one = Task(title="Walk", duration_minutes=20, priority="high", pet_name="Mochi")
    task_two = Task(title="Feed", duration_minutes=10, priority="medium", pet_name="Luna")
    task_two.mark_complete()
    pet_one.add_task(task_one)
    pet_two.add_task(task_two)

    filtered = scheduler.filter_tasks([task_one, task_two], pet_name="Luna", completed=False)

    assert filtered == []


def test_mark_complete_creates_next_occurrence_for_recurring_task():
    task = Task(title="Pill", duration_minutes=5, priority="high", frequency="daily", due_date=date(2026, 7, 7))

    next_task = task.mark_complete()

    assert task.completed is True
    assert next_task is not None
    assert next_task.frequency == "daily"
    assert next_task.due_date == date(2026, 7, 8)


def test_scheduler_detects_conflicts_for_same_start_time():
    scheduler = Scheduler()
    first = ScheduledTask(task=Task(title="Walk", duration_minutes=20, priority="high"), start_minute=480, end_minute=500, reason="")
    second = ScheduledTask(task=Task(title="Feed", duration_minutes=10, priority="medium"), start_minute=480, end_minute=490, reason="")

    warnings = scheduler.detect_conflicts([first, second])

    assert len(warnings) == 1
    assert "Walk" in warnings[0] and "Feed" in warnings[0]
