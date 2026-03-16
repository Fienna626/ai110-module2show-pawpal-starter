import streamlit as st
from pawpal_system import Task, Scheduler, Owner, Pet

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

st.markdown(
    """
Welcome to the PawPal+ starter app.

This file is intentionally thin. It gives you a working Streamlit app so you can start quickly,
but **it does not implement the project logic**. Your job is to design the system and build it.

Use this app as your interactive demo once your backend classes/functions exist.
"""
)

with st.expander("Scenario", expanded=True):
    st.markdown(
        """
**PawPal+** is a pet care planning assistant. It helps a pet owner plan care tasks
for their pet(s) based on constraints like time, priority, and preferences.

You will design and implement the scheduling logic and connect it to this Streamlit UI.
"""
    )

with st.expander("What you need to build", expanded=True):
    st.markdown(
        """
At minimum, your system should:
- Represent pet care tasks (what needs to happen, how long it takes, priority)
- Represent the pet and the owner (basic info and preferences)
- Build a plan/schedule for a day that chooses and orders tasks based on constraints
- Explain the plan (why each task was chosen and when it happens)
"""
    )

st.divider()

# --- Persisted state (Streamlit reruns on every interaction) ---
if "owner" not in st.session_state:
    st.session_state.owner = Owner("Jordan")
if "pets" not in st.session_state:
    st.session_state.pets = []
if "selected_pet" not in st.session_state:
    st.session_state.selected_pet = None
if "schedule" not in st.session_state:
    st.session_state.schedule = None

st.subheader("Owner & Pets")
col1, col2 = st.columns([2, 1])
with col1:
    owner_name = st.text_input("Owner name", value=st.session_state.owner.name)
with col2:
    if st.button("Set owner"):
        # Reset state when the owner changes
        st.session_state.owner = Owner(owner_name)
        st.session_state.pets = []
        st.session_state.selected_pet = None
        st.session_state.schedule = None

st.markdown("### Add a pet")
col1, col2 = st.columns(2)
with col1:
    pet_name = st.text_input("Pet name", value="")
with col2:
    species = st.selectbox("Species", ["dog", "cat", "other"])

if st.button("Add pet"):
    if pet_name:
        pet = Pet(pet_name, species)
        st.session_state.pets.append(pet)
        st.session_state.owner.add_pet(pet)
        st.session_state.selected_pet = pet.name
        st.session_state.schedule = None

if st.session_state.pets:
    st.markdown("### Select a pet to add tasks")
    pet_names = [p.name for p in st.session_state.pets]
    selected_name = st.selectbox(
        "Pet", pet_names, index=pet_names.index(st.session_state.selected_pet) if st.session_state.selected_pet in pet_names else 0
    )
    st.session_state.selected_pet = selected_name

    active_pet = next(p for p in st.session_state.pets if p.name == selected_name)

    st.markdown(f"**Tasks for {active_pet.name}**")
    if "task_title" not in st.session_state:
        st.session_state.task_title = ""
    task_title = st.text_input("Task title", value=st.session_state.task_title)
    duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
    priority = st.selectbox("Priority", ["low", "medium", "high"], index=2)

    if st.button("Add task to selected pet"):
        if task_title:
            task = Task(task_title, duration, priority)
            active_pet.add_task(task)
            st.session_state.schedule = None
            st.session_state.task_title = ""

    if active_pet.tasks:
        st.write(f"{active_pet.name}'s tasks:")
        st.table([{"title": t.title, "duration_minutes": t.duration_minutes, "priority": t.priority} for t in active_pet.tasks])
    else:
        st.info("No tasks for this pet yet.")

st.divider()

st.subheader("Build Schedule")
st.caption("Click to generate a schedule based on all pets + tasks.")

if st.button("Generate schedule"):
    # Collect all tasks across the owner
    all_tasks = [task for pet in st.session_state.pets for task in pet.tasks]

    if not all_tasks:
        st.error("No tasks to schedule. Add tasks to your pets first.")
    else:
        scheduler = Scheduler()
        st.session_state.schedule = scheduler.generate_schedule(all_tasks)

if st.session_state.schedule:
    st.success("Schedule generated!")
    st.markdown("### Daily Schedule (Starting from 8:00 AM)")
    base_minutes = 8 * 60  # 8:00 AM
    for item in st.session_state.schedule:
        start_total = base_minutes + item["start_time"]
        end_total = base_minutes + item["end_time"]
        start_hour = start_total // 60
        start_min = start_total % 60
        end_hour = end_total // 60
        end_min = end_total % 60
        st.write(
            f"- **{item['task']}**: {start_hour:02d}:{start_min:02d} - {end_hour:02d}:{end_min:02d} ({item['reason']})"
        )

# --- State reset note ---
st.caption(
    "Tip: Streamlit reruns the script on every interaction. Persist state in `st.session_state` to avoid losing tasks/pets when the UI updates."
)
