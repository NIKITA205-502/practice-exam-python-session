from datetime import datetime

class Task:
    def __init__(self, title, description, priority, due_date, project_id, assignee_id) -> None:
        self.id = None
        self.title = title
        self.description = description
        self.priority = priority
        self.status = 'pending'
        self.due_date = due_date
        self.project_id = project_id
        self.assignee_id = assignee_id

    def update_status(self, new_status) -> bool:
        if new_status in ['pending', 'in_progress', 'completed']:
            self.status = new_status
            return True
        return False

    def is_overdue(self) -> bool:
        if self.status == 'completed':
            return False
        return datetime.now() > self.due_date

    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'priority': self.priority,
            'status': self.status,
            'due_date': self.due_date,
            'project_id': self.project_id,
            'assignee_id': self.assignee_id
        }
