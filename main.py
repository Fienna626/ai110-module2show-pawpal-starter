from pawpal_system import Owner, Pet, Task, Scheduler

def main():
    # Create one owner
    owner = Owner("Jordan")
    print(f"Owner created: {owner.name}")

    # Create two pets
    pet1 = Pet("Mochi", "dog")
    pet2 = Pet("Whiskers", "cat")
    print(f"Pets created: {pet1.name} ({pet1.species}), {pet2.name} ({pet2.species})")

    # Add pets to owner
    owner.add_pet(pet1)
    owner.add_pet(pet2)
    print(f"Owner {owner.name} now has {len(owner.pets)} pets")

    # Create at least 3 tasks
    # Tasks have an optional scheduled_time (HH:MM) and completion flag
    # They are intentionally created out-of-order to exercise sorting logic
    task1 = Task("Morning walk", 30, "high", scheduled_time="09:00", completed=False)
    task2 = Task("Feed breakfast", 10, "medium", scheduled_time="08:00", completed=True)
    task3 = Task("Playtime", 45, "low", scheduled_time="10:30", completed=False)
    task4 = Task("Evening grooming", 20, "medium", scheduled_time="19:00", completed=False)  # Extra task for more demo

    print("Tasks created:")
    print(f"- {task1.title}: {task1.duration_minutes} min, priority {task1.priority}")
    print(f"- {task2.title}: {task2.duration_minutes} min, priority {task2.priority}")
    print(f"- {task3.title}: {task3.duration_minutes} min, priority {task3.priority}")
    print(f"- {task4.title}: {task4.duration_minutes} min, priority {task4.priority}")

    # Add tasks to pets
    pet1.add_task(task1)  # Morning walk for dog
    pet1.add_task(task2)  # Feed breakfast for dog
    pet2.add_task(task3)  # Playtime for cat
    pet2.add_task(task4)  # Evening grooming for cat

    print(f"\nTask storage structure:")
    print(f"Pet {pet1.name} has {len(pet1.tasks)} tasks: {[t.title for t in pet1.tasks]}")
    print(f"Pet {pet2.name} has {len(pet2.tasks)} tasks: {[t.title for t in pet2.tasks]}")

    # Trace data flow across classes
    print("\nData flow trace:")
    print(f"Owner '{owner.name}' contains pets: {[p.name for p in owner.pets]}")
    for pet in owner.pets:
        print(f"  Pet '{pet.name}' contains tasks: {[t.title for t in pet.tasks]}")
        for task in pet.tasks:
            print(f"    Task '{task.title}': duration {task.duration_minutes} min, priority {task.priority}")

    # Verify task creation and retrieval
    print("\nTask creation and retrieval verification:")
    # Retrieve tasks from pets
    all_tasks = []
    for pet in owner.pets:
        all_tasks.extend(pet.tasks)
    print(f"Retrieved {len(all_tasks)} tasks from all pets: {[t.title for t in all_tasks]}")

    # Test scheduler
    print("\nTesting Scheduler:")
    scheduler = Scheduler()
    print("Inspecting Scheduler.generate_schedule method:")
    print("- Sorts tasks by priority (high > medium > low)")
    print("- Schedules tasks sequentially starting from time 0")
    print("- Returns schedule with start/end times and reasons")

    # Demonstrate sorting and filtering
    print("\nSorting tasks by scheduled_time (HH:MM):")
    sorted_by_time = scheduler.sort_by_time(all_tasks)
    print([f"{t.scheduled_time} - {t.title}" for t in sorted_by_time])

    print("\nFiltering tasks (completed=False):")
    incomplete_tasks = scheduler.filter_tasks(all_tasks, completed=False)
    print([t.title for t in incomplete_tasks])

    print("\nFiltering tasks for pet 'Mochi':")
    mochis_tasks = scheduler.filter_tasks(all_tasks, pet_name="Mochi")
    print([t.title for t in mochis_tasks])

    schedule = scheduler.generate_schedule(all_tasks)
    print(f"\nGenerated schedule for {len(all_tasks)} tasks:")

    # Display schedule starting from 8:00 AM
    base_minutes = 8 * 60  # 8:00 AM
    for item in schedule:
        start_total = base_minutes + item['start_time']
        end_total = base_minutes + item['end_time']
        start_hour = start_total // 60
        start_min = start_total % 60
        end_hour = end_total // 60
        end_min = end_total % 60
        print(f"- {item['task']}: {start_hour:02d}:{start_min:02d} - {end_hour:02d}:{end_min:02d} ({item['reason']})")

    # High-risk areas explanation
    print("\nHigh-risk student confusion areas:")
    print("1. Owner → Scheduler access patterns:")
    print("   - Owner contains pets, pets contain tasks")
    print("   - Scheduler takes a list of tasks (not owners or pets)")
    print("   - To schedule, collect all tasks from all pets: [task for pet in owner.pets for task in pet.tasks]")
    print("   - Scheduler is separate from Owner - it processes tasks independently")

    print("2. Task storage structure:")
    print("   - Tasks are stored in lists within Pet objects")
    print("   - Each Pet has its own self.tasks = []")
    print("   - Owner doesn't directly store tasks - only pets do")
    print("   - To get all tasks, iterate through owner.pets and collect their tasks")
    print("   - Owner doesn't directly store tasks - only pets do")
    print("   - To get all tasks, iterate through owner.pets and collect their tasks")

if __name__ == "__main__":
    main()