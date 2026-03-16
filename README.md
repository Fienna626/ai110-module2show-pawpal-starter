Phase 1: UML Design (Assigned)

[x]Generate UML Design
[x]Map UML to Python classes (pawpal_system.py)
[x]Identify relationships (Owner → Pet → Task → Scheduler)

Phase 2: Core Implementation (Assigned)

[x]Set up code for classes in pawpal_systems.py (Owner, Pet, Task, Scheduler)
[x]Run main.py demo 
[x]Main.py implementation should include One owner, two pets, at least 3 tasks, and testing scheduler.
[x]Trace data flow across classes
- The demo shows the complete data flow:
- Owner contains pets
- Each pet contains tasks
- Scheduler processes all tasks from all pets
[x]Verify task creation and retrieval
- tasks are properly created and can be retrieved from the pet objects.
[x]Inspect at least one class method carefully
- Scheduler method
- Sort tasks by priority: high > medium > low

High‑risk student confusion areas:
[x]Owner → Scheduler access patterns
-  the scheduler takes a flat list of tasks, not owners/pets directly. Tasks must be collected from pets first.
[x]Task storage structure
- Tasks are stored in lists within each Pet object, not directly in Owner.

Phase 3: UI Integration (Assigned)

[x]Integrate backend (pawpal_system.py) into the UI (app.py)
[x]Implement at least one function (examples: adding a pet, scheduling a task, etc.)
[x]Understand st.session_state usage
[x]Identify the common “state reset” bug
- Streamlit reruns the script on every interaction, so without st.session_state everything would reset when you click a button or change input.
This is why we persist pets/tasks in st.session_state: otherwise tasks disappear after each button press. 
[x]Trace one UI action to backend logic

Phase 4: Algorithmic Layer (Assigned)

[x]Pick 2 of the listed algorithms: 
-> Implement Sorting and Filtering
Verify conflict detection behavior
Reason through recurring task logic
Debug at least one edge case

Phase 5: Testing (Spot Check)

[x]Use AI to generate a test suite
[x]Run pytest
[x]Interpret one failing test scenario
- def test_sort_by_time_expected_failure():
    """This test is intentionally written to fail.

    It demonstrates what a failing assertion looks like and how pytest reports it.

    The actual sort order is [T2, T3, T1, T4]. We assert an incorrect order.
    """
    scheduler = Scheduler()
    tasks = [
        Task("T1", 10, "low", scheduled_time="12:00"),
        Task("T2", 10, "low", scheduled_time="08:30"),
        Task("T3", 10, "low", scheduled_time="09:15"),
        Task("T4", 10, "low"),  # no scheduled_time
    ]

    sorted_tasks = scheduler.sort_by_time(tasks)

    # This assertion is deliberately wrong to show a failing example.
    assert [t.title for t in sorted_tasks] == ["T1", "T2", "T3", "T4"]