tasks = []

def get_all_tasks():
    return tasks

def create_task(title:str, priority:int):
    new_task = {"id": len(tasks) + 1, "title": title, "priority": priority}
    tasks.append(new_task)
    return new_task

def get_task_by_id(task_id: int):
    for task in tasks:
        if task["id"] == task_id:
            return task
    return None

def update_task(task_id: int, title: str = None, priority: int = None):
    for task in tasks:
        if task["id"] == task_id:
            if title is not None:
                task["title"] = title
            if priority is not None:
                task["priority"] = priority
            return task
    return None

def delete_task(task_id: int):
    for task in tasks:
        if task["id"] == task_id:
            tasks.remove(task)
            return True
    return False

        