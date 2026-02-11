"""Todo service for CRUD operations."""
from typing import List, Optional
from sqlmodel import Session, select
from database.models.todo import Todo, TodoStatus, TodoPriority
from backend.src.utils.errors import ResourceNotFoundError, ValidationError
from datetime import datetime
import uuid


class TodoService:
    """Service for managing todo operations."""

    def __init__(self, session: Session):
        self.session = session

    def create_todo(
        self,
        user_id: uuid.UUID,
        title: str,
        description: Optional[str] = None,
        priority: TodoPriority = TodoPriority.MEDIUM,
        due_date: Optional[datetime] = None
    ) -> Todo:
        """Create a new todo."""
        if not title or len(title) < 1 or len(title) > 200:
            raise ValidationError("Title must be between 1 and 200 characters")

        if description and len(description) > 1000:
            raise ValidationError("Description must not exceed 1000 characters")

        todo = Todo(
            title=title,
            description=description,
            priority=priority,
            due_date=due_date,
            user_id=user_id,
            status=TodoStatus.PENDING
        )

        self.session.add(todo)
        self.session.commit()
        self.session.refresh(todo)
        return todo

    def get_todos(
        self,
        user_id: uuid.UUID,
        status: Optional[TodoStatus] = None,
        priority: Optional[TodoPriority] = None,
        limit: int = 50,
        offset: int = 0
    ) -> List[Todo]:
        """Get todos for a user with optional filters."""
        query = select(Todo).where(Todo.user_id == user_id)

        if status:
            query = query.where(Todo.status == status)

        if priority:
            query = query.where(Todo.priority == priority)

        query = query.offset(offset).limit(limit).order_by(Todo.created_at.desc())

        todos = self.session.exec(query).all()
        return list(todos)

    def get_todo_by_id(self, user_id: uuid.UUID, todo_id: int) -> Todo:
        """Get a specific todo by ID."""
        todo = self.session.get(Todo, todo_id)

        if not todo:
            raise ResourceNotFoundError("Todo", todo_id)

        if todo.user_id != user_id:
            raise ResourceNotFoundError("Todo", todo_id)

        return todo

    def update_todo(
        self,
        user_id: uuid.UUID,
        todo_id: int,
        title: Optional[str] = None,
        description: Optional[str] = None,
        status: Optional[TodoStatus] = None,
        priority: Optional[TodoPriority] = None,
        due_date: Optional[datetime] = None
    ) -> Todo:
        """Update an existing todo."""
        todo = self.get_todo_by_id(user_id, todo_id)

        if title is not None:
            if len(title) < 1 or len(title) > 200:
                raise ValidationError("Title must be between 1 and 200 characters")
            todo.title = title

        if description is not None:
            if len(description) > 1000:
                raise ValidationError("Description must not exceed 1000 characters")
            todo.description = description

        if status is not None:
            todo.status = status

        if priority is not None:
            todo.priority = priority

        if due_date is not None:
            todo.due_date = due_date

        todo.updated_at = datetime.utcnow()

        self.session.add(todo)
        self.session.commit()
        self.session.refresh(todo)
        return todo

    def delete_todo(self, user_id: uuid.UUID, todo_id: int) -> int:
        """Delete a todo."""
        todo = self.get_todo_by_id(user_id, todo_id)

        self.session.delete(todo)
        self.session.commit()
        return todo_id

    def toggle_todo_status(self, user_id: uuid.UUID, todo_id: int) -> Todo:
        """Toggle todo status between pending and completed."""
        todo = self.get_todo_by_id(user_id, todo_id)

        if todo.status == TodoStatus.PENDING:
            todo.status = TodoStatus.COMPLETED
        else:
            todo.status = TodoStatus.PENDING

        todo.updated_at = datetime.utcnow()

        self.session.add(todo)
        self.session.commit()
        self.session.refresh(todo)
        return todo

    def count_todos(
        self,
        user_id: uuid.UUID,
        status: Optional[TodoStatus] = None
    ) -> int:
        """Count todos for a user."""
        query = select(Todo).where(Todo.user_id == user_id)

        if status:
            query = query.where(Todo.status == status)

        return len(self.session.exec(query).all())
