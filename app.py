import streamlit as st

from pawpal_system import DailyPlan, Owner, Pet, Scheduler, Task

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")
st.caption("A smart pet-care planner that turns routine tasks into a daily plan.")

if "owner" not in st.session_state:
    st.session_state.owner = Owner(name="Jordan", daily_available_minutes=240)

owner: Owner = st.session_state.owner

st.subheader("Owner profile")
owner_name = st.text_input("Owner name", value=owner.name)
availability = st.number_input(
    "Daily available minutes",
    min_value=30,
    max_value=720,
    value=owner.daily_available_minutes,
)
if st.button("Save owner profile"):
    owner.name = owner_name
    owner.daily_available_minutes = int(availability)
    st.success(f"Updated profile for {owner.name}.")

st.divider()
st.subheader("Add a pet")
pet_name = st.text_input("Pet name", value="Mochi")
species = st.selectbox("Species", ["dog", "cat", "other"])
pet_notes = st.text_area("Pet notes", value="Loves morning walks and treats.")
if st.button("Add pet"):
    if not pet_name.strip():
        st.warning("Please enter a pet name.")
    else:
        pet = Pet(name=pet_name, species=species, owner=owner, notes=pet_notes)
        owner.add_pet(pet)
        st.session_state.selected_pet_name = pet.name
        st.success(f"Added {pet.name} to {owner.name}'s profile.")

if owner.pets:
    pet_names = [pet.name for pet in owner.pets]
    if "selected_pet_name" not in st.session_state or st.session_state.selected_pet_name not in pet_names:
        st.session_state.selected_pet_name = pet_names[0]

    selected_pet_name = st.selectbox(
        "Active pet",
        pet_names,
        index=pet_names.index(st.session_state.selected_pet_name),
    )
    st.session_state.selected_pet_name = selected_pet_name
    selected_pet = next(pet for pet in owner.pets if pet.name == selected_pet_name)

    st.write("Current pets:")
    st.table(
        [
            {"Name": pet.name, "Species": pet.species, "Tasks": len(pet.tasks)}
            for pet in owner.pets
        ]
    )

    st.divider()
    st.subheader("Add tasks")
    col1, col2, col3 = st.columns(3)
    with col1:
        task_title = st.text_input("Task title", value="Morning walk")
    with col2:
        duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
    with col3:
        priority = st.selectbox("Priority", ["low", "medium", "high"], index=2)

    recurring = st.checkbox("Recurring task")
    preferred_start = st.number_input("Preferred start hour", min_value=0, max_value=23, value=8)

    if st.button("Add task"):
        if not task_title.strip():
            st.warning("Please enter a task title.")
        else:
            task = Task(
                title=task_title,
                duration_minutes=int(duration),
                priority=priority,
                recurring=recurring,
                preferred_start_hour=int(preferred_start),
            )
            selected_pet.add_task(task)
            st.success(f"Added {task.title} to {selected_pet.name}.")

    if selected_pet.tasks:
        st.write(f"Tasks for {selected_pet.name}:")
        st.table(
            [
                {
                    "Task": task.title,
                    "Duration": task.duration_minutes,
                    "Priority": task.priority,
                    "Recurring": task.recurring,
                    "Completed": task.completed,
                }
                for task in selected_pet.tasks
            ]
        )

        scheduler = Scheduler(day_start_hour=8, day_end_hour=20)
        sorted_tasks = scheduler.sort_by_time(selected_pet.tasks)
        st.caption("Sorted by preferred start time")
        st.table(
            [
                {
                    "Task": task.title,
                    "Preferred start": task.preferred_start_hour if task.preferred_start_hour is not None else "—",
                }
                for task in sorted_tasks
            ]
        )

        incomplete_tasks = scheduler.filter_tasks(selected_pet.tasks, completed=False)
        if incomplete_tasks:
            st.caption("Incomplete tasks")
            st.write([task.title for task in incomplete_tasks])
    else:
        st.info("No tasks yet for this pet.")
else:
    st.info("Add at least one pet to start tracking tasks.")

st.divider()
st.subheader("Build Schedule")

if st.button("Generate schedule"):
    if not owner.get_all_tasks():
        st.warning("Add at least one task before generating a schedule.")
    else:
        scheduler = Scheduler(day_start_hour=8, day_end_hour=20)
        plan = scheduler.build_daily_plan(owner, owner.pets[0], owner.get_all_tasks())
        conflicts = scheduler.detect_conflicts(plan.scheduled_tasks)
        st.session_state.plan = plan
        st.session_state.explanations = scheduler.explain_plan(plan)
        st.session_state.conflicts = conflicts

if "plan" in st.session_state:
    plan: DailyPlan = st.session_state.plan
    st.success(f"Planned {len(plan.scheduled_tasks)} task(s) for {plan.pet.name}.")
    st.metric("Scheduled minutes", plan.total_scheduled_minutes)
    st.metric("Skipped tasks", len(plan.unscheduled_tasks))

    st.subheader("Daily plan")
    rows = []
    for item in plan.scheduled_tasks:
        rows.append(
            {
                "Time": f"{item.start_minute // 60:02d}:{item.start_minute % 60:02d}",
                "Task": item.title,
                "Duration": item.duration_minutes,
                "Priority": item.priority,
                "Reason": item.reason,
            }
        )
    st.table(rows)

    if plan.unscheduled_tasks:
        st.subheader("Skipped tasks")
        st.write([task.title for task in plan.unscheduled_tasks])

    if st.session_state.get("conflicts"):
        st.warning("Scheduler warnings")
        for warning in st.session_state.conflicts:
            st.write(f"- {warning}")

    st.subheader("Why this plan was chosen")
    for line in st.session_state.explanations:
        st.write(line)
