import sqlite3
from models.task import Task
from models.project import Project
from models.user import User
from datetime import datetime

class DatabaseManager:
    def __init__(self, db_path="tasks.db") -> None:
        self.db_path = db_path
        self.conn = sqlite3.connect(db_path)
        self.conn.row_factory = sqlite3.Row

    def close(self) -> None:
        if self.conn:
            self.conn.close()

    def create_tables(self) -> None:
        cursor = self.conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS projects (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                description TEXT,
                start_date TEXT NOT NULL,
                end_date TEXT NOT NULL,
                status TEXT DEFAULT 'active'
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                email TEXT NOT NULL,
                role TEXT NOT NULL,
                registration_date TEXT NOT NULL
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT,
                priority INTEGER DEFAULT 2,
                status TEXT DEFAULT 'pending',
                due_date TEXT NOT NULL,
                project_id INTEGER,
                assignee_id INTEGER,
                FOREIGN KEY (project_id) REFERENCES projects(id),
                FOREIGN KEY (assignee_id) REFERENCES users(id)
            )
        ''')
        self.conn.commit()

    def add_task(self, task: Task) -> int:
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT INTO tasks (title, description, priority, status, due_date, project_id, assignee_id)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (task.title, task.description, task.priority, task.status,
              task.due_date.isoformat(), task.project_id, task.assignee_id))
        self.conn.commit()
        return cursor.lastrowid

    def get_task_by_id(self, task_id) -> Task | None:
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM tasks WHERE id = ?', (task_id,))
        row = cursor.fetchone()
        if row is None:
            return None
        return self._row_to_task(row)

    def get_all_tasks(self) -> list[Task]:
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM tasks')
        rows = cursor.fetchall()
        return [self._row_to_task(row) for row in rows]

    def update_task(self, task_id, **kwargs) -> bool:
        allowed = ['title', 'description', 'priority', 'status', 'due_date', 'project_id', 'assignee_id']
        updates = {}
        for key, value in kwargs.items():
            if key in allowed:
                updates[key] = value
        if not updates:
            return False
        set_clause = ', '.join(f'{k} = ?' for k in updates.keys())
        values = list(updates.values())
        if 'due_date' in updates:
            idx = list(updates.keys()).index('due_date')
            values[idx] = values[idx].isoformat() if isinstance(values[idx], datetime) else values[idx]
        values.append(task_id)
        cursor = self.conn.cursor()
        cursor.execute(f'UPDATE tasks SET {set_clause} WHERE id = ?', values)
        self.conn.commit()
        return cursor.rowcount > 0

    def delete_task(self, task_id) -> bool:
        cursor = self.conn.cursor()
        cursor.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
        self.conn.commit()
        return cursor.rowcount > 0

    def search_tasks(self, query) -> list[Task]:
        cursor = self.conn.cursor()
        cursor.execute('''
            SELECT * FROM tasks WHERE title LIKE ? OR description LIKE ?
        ''', (f'%{query}%', f'%{query}%'))
        rows = cursor.fetchall()
        return [self._row_to_task(row) for row in rows]

    def get_tasks_by_project(self, project_id) -> list[Task]:
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM tasks WHERE project_id = ?', (project_id,))
        rows = cursor.fetchall()
        return [self._row_to_task(row) for row in rows]

    def get_tasks_by_user(self, user_id) -> list[Task]:
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM tasks WHERE assignee_id = ?', (user_id,))
        rows = cursor.fetchall()
        return [self._row_to_task(row) for row in rows]

    def add_project(self, project: Project) -> int:
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT INTO projects (name, description, start_date, end_date, status)
            VALUES (?, ?, ?, ?, ?)
        ''', (project.name, project.description, project.start_date.isoformat(),
              project.end_date.isoformat(), project.status))
        self.conn.commit()
        return cursor.lastrowid

    def get_project_by_id(self, project_id) -> Project | None:
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM projects WHERE id = ?', (project_id,))
        row = cursor.fetchone()
        if row is None:
            return None
        return self._row_to_project(row)

    def get_all_projects(self) -> list[Project]:
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM projects')
        rows = cursor.fetchall()
        return [self._row_to_project(row) for row in rows]

    def update_project(self, project_id, **kwargs) -> bool:
        allowed = ['name', 'description', 'start_date', 'end_date', 'status']
        updates = {}
        for key, value in kwargs.items():
            if key in allowed:
                updates[key] = value
        if not updates:
            return False
        set_clause = ', '.join(f'{k} = ?' for k in updates.keys())
        values = list(updates.values())
        for date_field in ['start_date', 'end_date']:
            if date_field in updates:
                idx = list(updates.keys()).index(date_field)
                values[idx] = values[idx].isoformat() if isinstance(values[idx], datetime) else values[idx]
        values.append(project_id)
        cursor = self.conn.cursor()
        cursor.execute(f'UPDATE projects SET {set_clause} WHERE id = ?', values)
        self.conn.commit()
        return cursor.rowcount > 0

    def delete_project(self, project_id) -> bool:
        cursor = self.conn.cursor()
        cursor.execute('DELETE FROM projects WHERE id = ?', (project_id,))
        self.conn.commit()
        return cursor.rowcount > 0

    def add_user(self, user: User) -> int:
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT INTO users (username, email, role, registration_date)
            VALUES (?, ?, ?, ?)
        ''', (user.username, user.email, user.role, user.registration_date.isoformat()))
        self.conn.commit()
        return cursor.lastrowid

    def get_user_by_id(self, user_id) -> User | None:
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM users WHERE id = ?', (user_id,))
        row = cursor.fetchone()
        if row is None:
            return None
        return self._row_to_user(row)

    def get_all_users(self) -> list[User]:
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM users')
        rows = cursor.fetchall()
        return [self._row_to_user(row) for row in rows]

    def update_user(self, user_id, **kwargs) -> bool:
        allowed = ['username', 'email', 'role']
        updates = {}
        for key, value in kwargs.items():
            if key in allowed:
                updates[key] = value
        if not updates:
            return False
        set_clause = ', '.join(f'{k} = ?' for k in updates.keys())
        values = list(updates.values())
        values.append(user_id)
        cursor = self.conn.cursor()
        cursor.execute(f'UPDATE users SET {set_clause} WHERE id = ?', values)
        self.conn.commit()
        return cursor.rowcount > 0

    def delete_user(self, user_id) -> bool:
        cursor = self.conn.cursor()
        cursor.execute('DELETE FROM users WHERE id = ?', (user_id,))
        self.conn.commit()
        return cursor.rowcount > 0

    def _row_to_task(self, row) -> Task:
        task = Task(
            title=row['title'],
            description=row['description'],
            priority=row['priority'],
            due_date=datetime.fromisoformat(row['due_date']),
            project_id=row['project_id'],
            assignee_id=row['assignee_id']
        )
        task.id = row['id']
        task.status = row['status']
        return task

    def _row_to_project(self, row) -> Project:
        project = Project(
            name=row['name'],
            description=row['description'],
            start_date=datetime.fromisoformat(row['start_date']),
            end_date=datetime.fromisoformat(row['end_date'])
        )
        project.id = row['id']
        project.status = row['status']
        return project

    def _row_to_user(self, row) -> User:
        user = User(
            username=row['username'],
            email=row['email'],
            role=row['role']
        )
        user.id = row['id']
        user.registration_date = datetime.fromisoformat(row['registration_date'])
        return user
