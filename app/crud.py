"""
CRUD / service layer.

Encapsulates all database operations for the `Student` entity. Keeping
this logic out of the route handlers gives a clean separation of
responsibilities: routers deal with HTTP concerns, crud deals with
persistence and business rules.
"""

from sqlalchemy.orm import Session

from app.models import Student
from app.schemas import StudentCreate, StudentUpdate


class StudentAlreadyExistsError(Exception):
    """Raised when attempting to create a student with a duplicate email."""


class StudentService:
    """Encapsulates all business logic for student records."""

    def __init__(self, db: Session) -> None:
        self.db = db

    def get_all(self) -> list[Student]:
        """Return every student in the database."""
        return list(self.db.query(Student).order_by(Student.id).all())

    def get_by_id(self, student_id: int) -> Student | None:
        """Return a single student by ID, or None if not found."""
        return self.db.query(Student).filter(Student.id == student_id).first()

    def get_by_email(self, email: str) -> Student | None:
        """Return a single student by email, or None if not found."""
        return self.db.query(Student).filter(Student.email == email).first()

    def create(self, student_in: StudentCreate) -> Student:
        """Create a new student record.

        Raises:
            StudentAlreadyExistsError: if the  email is already taken.
        """
        
        if self.get_by_email(student_in.email) is not None:
            raise StudentAlreadyExistsError(
                f"A student with email '{student_in.email}' already exists."
            )

        student = Student(
            name=student_in.name,
            age=student_in.age,
            grade=student_in.grade,
            email=student_in.email,
        )
        self.db.add(student)
        self.db.commit()
        self.db.refresh(student)
        return student

    def update(self, student_id: int, student_in: StudentUpdate) -> Student | None:
        """Update an existing student. Returns None if the student is not found.

        Raises:
            StudentAlreadyExistsError: if the new email is already taken by
                another student.
        """
        student = self.get_by_id(student_id)
        if student is None:
            return None

        update_data = student_in.model_dump(exclude_unset=True)

        if "email" in update_data and update_data["email"] != student.email:
            existing = self.get_by_email(update_data["email"])
            if existing is not None and existing.id != student.id:
                raise StudentAlreadyExistsError(
                    f"A student with email '{update_data['email']}' already exists."
                )

        for field, value in update_data.items():
            setattr(student, field, value)

        self.db.commit()
        self.db.refresh(student)
        return student

    def delete(self, student_id: int) -> bool:
        """Delete a student by ID. Returns True if deleted, False if not found."""
        student = self.get_by_id(student_id)
        if student is None:
            return False

        self.db.delete(student)
        self.db.commit()
        return True
