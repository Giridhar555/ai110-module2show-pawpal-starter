from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, timedelta
from typing import List, Optional


@dataclass
class Owner:
    name: str
    daily_available_minutes: int = 240
    preferred_start_hour: int = 8
    preferred_end_hour: int = 20
    preferences: List[str] = field(default_factory=list)
    pets: List["Pet"] = field(default_factory=list)

    def add_pet(self, pet: "Pet") -> None:
        """Add a pet to the owner's collection."""
        if pet not in self.pets:
            self.pets.append(pet)

    def get_all_tasks(self) -> List["Task"]:
        """Return all tasks belonging to the owner's pets."""
        return [task for pet in self.pets for task in pet.tasks]


@dataclass
class Pet:
    name: str
    species: str
    owner: Owner
    age_years: Optional[int] = None
    notes: str = ""
    tasks: List["Task"] = field(default_factory=list)

    def add_task(self, task: "Task") -> None:
        """Add a task to this pet's task list."""
        self.tasks.append(task)
        if self.owner not in self.owner.pets:
            self.owner.add_pet(self)


@dataclass
class Task:
    title: str
    duration_minutes: int
    priority: str = "medium"
    category: str = "general"
    preferred_start_hour: Optional[int] = None
    recurring: bool = False
    notes: str = ""
    completed: bool = False
    frequency: str = "once"
    due_date: Optional[date] = None
    pet_name: Optional[str] = None

    def priority_score(self) -> int:
        """Return a numeric score for the task priority."""
        ranking = {"low": 1, "medium": 2, "high": 3}
        return ranking.get(self.priority.lower(), 2)

    def mark_complete(self) -> Optional["Task"]:
        """Mark the task as completed and create the next recurring occurrence when needed."""
        self.completed = True
        if self.frequency.lower() in {"daily", "weekly"}:
            next_date = self.due_date + timedelta(days=1 if self.frequency.lower() == "daily" else 7)
            return Task(
                title=self.title,
                duration_minutes=self.duration_minutes,
                priority=self.priority,
                category=self.category,
                preferred_start_hour=self.preferred_start_hour,
                recurring=self.recurring,
                notes=self.notes,
                frequency=self.frequency,
                due_date=next_date,
                pet_name=self.pet_name,
            )
        return None


@dataclass
class ScheduledTask:
    task: Task
    start_minute: int
    end_minute: int
    reason: str

    @property
    def title(self) -> str:
        return self.task.title

    @property
    def duration_minutes(self) -> int:
        return self.task.duration_minutes

    @property
    def priority(self) -> str:
        return self.task.priority


@dataclass
class DailyPlan:
    scheduled_tasks: List[ScheduledTask]
    unscheduled_tasks: List[Task]
    owner: Owner
    pet: Pet
    day_start_hour: int
    day_end_hour: int

    @property
    def total_scheduled_minutes(self) -> int:
        return sum(task.duration_minutes for task in self.scheduled_tasks)


class Scheduler:
    def __init__(self, day_start_hour: int = 8, day_end_hour: int = 20) -> None:
        """Create a scheduler with a time window for the day."""
        self.day_start_hour = day_start_hour
        self.day_end_hour = day_end_hour

    def sort_by_time(self, tasks: List[Task]) -> List[Task]:
        """Return tasks ordered by their preferred start hour, then by title."""
        return sorted(
            tasks,
            key=lambda task: (
                task.preferred_start_hour if task.preferred_start_hour is not None else 99,
                task.title.lower(),
            ),
        )

    def filter_tasks(self, tasks: List[Task], pet_name: Optional[str] = None, completed: Optional[bool] = None) -> List[Task]:
        """Filter tasks by pet name and completion status."""
        filtered = list(tasks)
        if pet_name is not None:
            filtered = [task for task in filtered if task.pet_name == pet_name]
        if completed is not None:
            filtered = [task for task in filtered if task.completed is completed]
        return filtered

    def detect_conflicts(self, scheduled_tasks: List[ScheduledTask]) -> List[str]:
        """Return lightweight warnings whenever two scheduled tasks share the same start time."""
        warnings: List[str] = []
        seen_by_start_time: dict[int, ScheduledTask] = {}
        for item in scheduled_tasks:
            if item.start_minute in seen_by_start_time:
                first_item = seen_by_start_time[item.start_minute]
                warnings.append(
                    f"Conflict detected between {first_item.task.title} and {item.task.title} at {self._format_time(item.start_minute)}."
                )
            else:
                seen_by_start_time[item.start_minute] = item
        return warnings

    def build_daily_plan(self, owner: Owner, pet: Pet, tasks: List[Task]) -> DailyPlan:
        """Build a daily plan for the provided tasks and time window."""
        day_start_minutes = self.day_start_hour * 60
        day_end_minutes = self.day_end_hour * 60
        available_minutes = min(owner.daily_available_minutes, max(0, day_end_minutes - day_start_minutes))

        ordered_tasks = list(enumerate(tasks))
        sorted_tasks = [
            task
            for _, task in sorted(
                ordered_tasks,
                key=lambda item: (
                    -item[1].priority_score(),
                    item[1].preferred_start_hour is None,
                    item[1].preferred_start_hour if item[1].preferred_start_hour is not None else 99,
                    item[0],
                    item[1].title.lower(),
                ),
            )
        ]

        scheduled: List[ScheduledTask] = []
        unscheduled: List[Task] = []
        used_minutes = 0
        occupied_slots: List[tuple[int, int]] = []

        for task in sorted_tasks:
            if used_minutes + task.duration_minutes > available_minutes:
                unscheduled.append(task)
                continue

            preferred_start = self._preferred_start(task, day_start_minutes)
            start_minute = self._find_next_available_slot(
                preferred_start,
                task.duration_minutes,
                occupied_slots,
                day_start_minutes,
                day_end_minutes,
            )

            if start_minute is None:
                unscheduled.append(task)
                continue

            end_minute = start_minute + task.duration_minutes
            occupied_slots.append((start_minute, end_minute))
            used_minutes += task.duration_minutes
            scheduled.append(
                ScheduledTask(
                    task=task,
                    start_minute=start_minute,
                    end_minute=end_minute,
                    reason=self._reason_for_task(task, start_minute),
                )
            )

        scheduled.sort(key=lambda item: (item.start_minute, item.end_minute, item.title.lower()))
        return DailyPlan(
            scheduled_tasks=scheduled,
            unscheduled_tasks=unscheduled,
            owner=owner,
            pet=pet,
            day_start_hour=self.day_start_hour,
            day_end_hour=self.day_end_hour,
        )

    def explain_plan(self, plan: DailyPlan) -> List[str]:
        """Create a human-readable explanation of the scheduled plan."""
        explanations: List[str] = []
        for item in plan.scheduled_tasks:
            time_label = self._format_time(item.start_minute)
            explanations.append(
                f"{time_label} — {item.title} ({item.duration_minutes} min, {item.priority} priority)"
            )
        if plan.unscheduled_tasks:
            explanations.append("Skipped tasks due to time limits or conflicts:")
            for task in plan.unscheduled_tasks:
                explanations.append(f"- {task.title}")
        return explanations

    def _preferred_start(self, task: Task, day_start_minutes: int) -> int:
        if task.preferred_start_hour is None:
            return day_start_minutes
        return max(day_start_minutes, task.preferred_start_hour * 60)

    def _find_next_available_slot(
        self,
        preferred_start: int,
        duration: int,
        occupied_slots: List[tuple[int, int]],
        day_start_minutes: int,
        day_end_minutes: int,
    ) -> Optional[int]:
        candidate = max(preferred_start, day_start_minutes)
        while candidate + duration <= day_end_minutes:
            if all(candidate + duration <= slot_start or candidate >= slot_end for slot_start, slot_end in occupied_slots):
                return candidate
            candidate = self._next_end_after_conflict(candidate, duration, occupied_slots)
        return None

    def _next_end_after_conflict(
        self,
        candidate: int,
        duration: int,
        occupied_slots: List[tuple[int, int]],
    ) -> int:
        conflicts = [slot_end for slot_start, slot_end in occupied_slots if candidate < slot_end and candidate + duration > slot_start]
        if conflicts:
            return max(conflicts)
        return candidate + 15

    def _reason_for_task(self, task: Task, start_minute: int) -> str:
        if task.recurring:
            return "recurring task kept in the plan"
        if task.preferred_start_hour is not None and start_minute == task.preferred_start_hour * 60:
            return "matched preferred start time"
        return "scheduled within available time"

    def _format_time(self, total_minutes: int) -> str:
        hours = total_minutes // 60
        minutes = total_minutes % 60
        return f"{hours:02d}:{minutes:02d}"


if __name__ == "__main__":
    owner = Owner(name="Jordan", daily_available_minutes=240)
    pet = Pet(name="Mochi", species="dog", owner=owner)
    scheduler = Scheduler(day_start_hour=8, day_end_hour=20)
    tasks = [
        Task(title="Morning walk", duration_minutes=30, priority="high", category="walk", preferred_start_hour=8),
        Task(title="Feeding", duration_minutes=10, priority="high", category="feeding", preferred_start_hour=9),
        Task(title="Medication", duration_minutes=15, priority="high", category="medication", preferred_start_hour=8),
        Task(title="Brushing", duration_minutes=15, priority="medium", category="grooming", recurring=True),
    ]
    plan = scheduler.build_daily_plan(owner, pet, tasks)
    print(f"Daily plan for {pet.name}:")
    for line in scheduler.explain_plan(plan):
        print(line)
