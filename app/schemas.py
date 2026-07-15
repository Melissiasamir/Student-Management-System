"""
Pydantic schemas.

These define the "shape" of data coming in through the API (requests)
and going out of it (responses), and enforce validation rules that
were previously weak or missing in the original CLI project:

- Proper email validation (not just checking for "@")
- Age must be a positive integer
- Required fields cannot be empty/whitespace
- Student IDs are generated automatically by the database
  (auto-increment primary key)
"""

from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator


class StudentBase(BaseModel):
    """Fields shared by create and read schemas."""

    name: str = Field(..., min_length=1, max_length=100, description="Full name of the student")
    age: int = Field(..., gt=0, lt=150, description="Student age; must be a positive, realistic integer")
    grade: str = Field(..., min_length=1, max_length=20, description="Student grade, e.g. 'A' or '10th'")
    email: EmailStr = Field(..., description="A valid, unique email address")

    @field_validator("name", "grade")
    @classmethod
    def not_blank(cls, value: str) -> str:
        """Reject strings that are empty or only whitespace."""
        if not value.strip():
            raise ValueError("Field cannot be empty or whitespace only.")
        return value.strip()


class StudentCreate(StudentBase):
    """Schema used when creating a new student (POST /students)."""

    pass


class StudentUpdate(BaseModel):
    """Schema used when updating a student (PUT /students/{id}).

    All fields are optional so a client can send a partial update;
    any field that is omitted keeps its current value.
    """

    name: str | None = Field(default=None, min_length=1, max_length=100)
    age: int | None = Field(default=None, gt=0, lt=150)
    grade: str | None = Field(default=None, min_length=1, max_length=20)
    email: EmailStr | None = None

    @field_validator("name", "grade")
    @classmethod
    def not_blank(cls, value: str | None) -> str | None:
        if value is not None and not value.strip():
            raise ValueError("Field cannot be empty or whitespace only.")
        return value.strip() if value is not None else value


class StudentResponse(StudentBase):
    """Schema used when returning student data to the client."""

    id: int

    model_config = ConfigDict(from_attributes=True)


class ErrorResponse(BaseModel):
    """Standard error envelope for meaningful error messages."""

    detail: str
