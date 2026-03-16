import pytest

from pawpal_system import Owner, Pet, Task, Scheduler


def test_sort_by_time_orders_tasks_correctly():
    scheduler = Scheduler()
    tasks = [
        Task("T1", 10, "low", scheduled_time="12:00"),
        Task("T2", 10, "low", scheduled_time="08:30"),
        Task("T3", 10, "low", scheduled_time="09:15"),
        Task("T4", 10, "low"),  # no scheduled_time
    ]

    sorted_tasks = scheduler.sort_by_time(tasks)

    assert [t.title for t in sorted_tasks] == ["T2", "T3", "T1", "T4"]


def test_filter_tasks_by_completed_flag():
    scheduler = Scheduler()
    tasks = [
        Task("T1", 10, "low", completed=True),
        Task("T2", 10, "low", completed=False),
        Task("T3", 10, "low", completed=False),
    ]

    incomplete = scheduler.filter_tasks(tasks, completed=False)
    assert {t.title for t in incomplete} == {"T2", "T3"}


def test_filter_tasks_by_pet_name():
    owner = Owner("Jordan")
    pet_a = Pet("A", "cat")
    pet_b = Pet("B", "dog")
    owner.add_pet(pet_a)
    owner.add_pet(pet_b)

    t1 = Task("T1", 10, "low")
    t2 = Task("T2", 10, "low")
    t3 = Task("T3", 10, "low")

    pet_a.add_task(t1)
    pet_b.add_task(t2)
    pet_a.add_task(t3)

    scheduler = Scheduler()
    pet_a_tasks = scheduler.filter_tasks([t1, t2, t3], pet_name="A")

    assert {t.title for t in pet_a_tasks} == {"T1", "T3"}


def test_generate_schedule_priority_order():
    scheduler = Scheduler()
    tasks = [
        Task("Low", 10, "low"),
        Task("High", 10, "high"),
        Task("Medium", 10, "medium"),
    ]

    schedule = scheduler.generate_schedule(tasks)
    assert [item["task"] for item in schedule] == ["High", "Medium", "Low"]


def test_sort_by_time_expected_failure():
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
