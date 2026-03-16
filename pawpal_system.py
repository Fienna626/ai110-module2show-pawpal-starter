class Owner:
    def __init__(self, name):
        self.name = name
        self.pets = []

    def add_pet(self, pet):
        self.pets.append(pet)


class Pet:
    def __init__(self, name, species):
        self.name = name
        self.species = species
        self.tasks = []

    def add_task(self, task):
        # Track which pet the task belongs to, useful for filtering later
        task.pet_name = self.name
        self.tasks.append(task)


class Task:
    def __init__(self, title, duration_minutes, priority, scheduled_time=None, completed=False):
        self.title = title
        self.duration_minutes = duration_minutes
        self.priority = priority
        self.scheduled_time = scheduled_time  # optional string like "HH:MM"
        self.completed = completed
        self.pet_name = None


class Scheduler:
    def sort_by_time(self, tasks):
        """Sort tasks by a "HH:MM" time string stored in Task.scheduled_time."""
        def parse_time(task):
            if not getattr(task, "scheduled_time", None):
                return (99, 99)  # place tasks without time at the end
            hour_str, minute_str = task.scheduled_time.split(":")
            return (int(hour_str), int(minute_str))

        return sorted(tasks, key=parse_time)

    def filter_tasks(self, tasks, completed=None, pet_name=None):
        """Filter tasks by completion status and/or owning pet name."""
        filtered = tasks
        if completed is not None:
            filtered = [t for t in filtered if t.completed == completed]
        if pet_name is not None:
            filtered = [t for t in filtered if getattr(t, "pet_name", None) == pet_name]
        return filtered

    def generate_schedule(self, tasks):
        # Sort tasks by priority: high > medium > low
        priority_order = {'high': 3, 'medium': 2, 'low': 1}
        sorted_tasks = sorted(tasks, key=lambda t: priority_order[t.priority], reverse=True)
        
        # Simple scheduling: schedule tasks sequentially starting from time 0
        schedule = []
        current_time = 0  # in minutes from start of day
        for task in sorted_tasks:
            schedule.append({
                'task': task.title,
                'start_time': current_time,
                'end_time': current_time + task.duration_minutes,
                'reason': f"Priority: {task.priority}"
            })
            current_time += task.duration_minutes
        
        return schedule