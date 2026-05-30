from models.task import Task

class TaskController:
    def __init__(self, db_manager) -> None:
        self.db = db_manager

    def add_task(self, title, description, priority, due_date, project_id, assignee_id) -> int:
        task = Task(title, description, priority, due_date, project_id, assignee_id)
        return self.db.add_task(task)

    def get_task(self, task_id) -> Task | None:
        return self.db.get_task_by_id(task_id)

    def get_all_tasks(self) -> list[Task]:
        return self.db.get_all_tasks()

    def update_task(self, task_id, **kwargs) -> bool:
        return self.db.update_task(task_id, **kwargs)

    def delete_task(self, task_id) -> bool:
        return self.db.delete_task(task_id)

    def search_tasks(self, query) -> list[Task]:
        return self.db.search_tasks(query)

    def update_task_status(self, task_id, new_status) -> bool:
        task = self.db.get_task_by_id(task_id)
        if task is None:
            return False
        return task.update_status(new_status) and self.db.update_task(task_id, status=new_status)

    def get_overdue_tasks(self) -> list[Task]:
        tasks = self.db.get_all_tasks()
        return [t for t in tasks if t.is_overdue()]

    def get_tasks_by_project(self, project_id) -> list[Task]:
        return self.db.get_tasks_by_project(project_id)

    def get_tasks_by_user(self, user_id) -> list[Task]:
        return self.db.get_tasks_by_user(user_id)
