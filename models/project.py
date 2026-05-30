from datetime import datetime

class Project:
    def __init__(self, name, description, start_date, end_date) -> None:
        self.id = None
        self.name = name
        self.description = description
        self.start_date = start_date
        self.end_date = end_date
        self.status = 'active'

    def update_status(self, new_status) -> bool:
        if new_status in ['active', 'completed', 'on_hold']:
            self.status = new_status
            return True
        return False

    def get_progress(self) -> float:
        if self.status == 'completed':
            return 100.0
        total_days = (self.end_date - self.start_date).days
        if total_days <= 0:
            return 0.0
        elapsed = (datetime.now() - self.start_date).days
        progress = (elapsed / total_days) * 100
        if progress > 100:
            return 100.0
        if progress < 0:
            return 0.0
        return progress

    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'start_date': self.start_date,
            'end_date': self.end_date,
            'status': self.status
        }
