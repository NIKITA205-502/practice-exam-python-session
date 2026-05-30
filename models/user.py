from datetime import datetime
import re

class User:
    def __init__(self, username, email, role) -> None:
        self.id = None
        self.username = username
        self.email = email
        self.role = role
        self.registration_date = datetime.now()

    def _is_valid_email(self, email) -> bool:
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None

    def update_info(self, username=None, email=None, role=None) -> None:
        if username is not None:
            self.username = username
        if email is not None:
            self.email = email
        if role is not None:
            self.role = role

    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'role': self.role,
            'registration_date': self.registration_date
        }
