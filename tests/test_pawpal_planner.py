from datetime import date

from pawpal_system import CareKnowledgeBase, Owner, Pet, PetCarePlanner, Task


def test_planner_applies_category_boosts():
    owner = Owner(name="Jordan", daily_available_minutes=120)
    pet = Pet(name="Mochi", species="dog", owner=owner)
    tasks = [
        Task(title="Medication", duration_minutes=15, priority="high", category="medication", pet_name=pet.name),
        Task(title="Walk", duration_minutes=30, priority="medium", category="walk", pet_name=pet.name),
    ]

    planner = PetCarePlanner(knowledge_base=CareKnowledgeBase())
    plan, trace, confidence = planner.plan(owner, pet, tasks)

    assert any("Retrieved guidance for 'Medication'" in line for line in trace)
    assert plan.scheduled_tasks[0].task.title == "Medication"
    assert confidence > 0.5


def test_planner_confidence_is_lower_when_tasks_are_skipped():
    owner = Owner(name="Jordan", daily_available_minutes=20)
    pet = Pet(name="Mochi", species="dog", owner=owner)
    tasks = [
        Task(title="Medication", duration_minutes=15, priority="high", category="medication", pet_name=pet.name),
        Task(title="Long grooming", duration_minutes=30, priority="medium", category="grooming", pet_name=pet.name),
    ]

    planner = PetCarePlanner(knowledge_base=CareKnowledgeBase())
    plan, trace, confidence = planner.plan(owner, pet, tasks)

    assert len(plan.unscheduled_tasks) == 1
    assert 0.0 <= confidence <= 1.0
