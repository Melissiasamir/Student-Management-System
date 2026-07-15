"""
Student API routes.

Implements the full set of RESTful endpoints for managing student
records, delegating all persistence logic to `StudentService`.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.crud import StudentAlreadyExistsError, StudentService
from app.database import get_db
from app.schemas import StudentCreate, StudentResponse, StudentUpdate

router = APIRouter(prefix="/students", tags=["Students"])


def get_student_service(db: Session = Depends(get_db)) -> StudentService:
    """Dependency that provides a StudentService bound to the request's DB session."""
    return StudentService(db)


@router.post(
    "",
    response_model=StudentResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Add a new student",
    responses={
        409: {"description": "A student with this ID or email already exists."},
        422: {"description": "Validation error."},
    },
)
def create_student(
    student_in: StudentCreate,
    service: StudentService = Depends(get_student_service),
) -> StudentResponse:
    """Create a new student record. The ID is generated automatically."""
    try:
        student = service.create(student_in)
    except StudentAlreadyExistsError as exc:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc)) from exc
    return student


@router.get(
    "",
    response_model=list[StudentResponse],
    status_code=status.HTTP_200_OK,
    summary="Get all students",
)
def read_students(
    service: StudentService = Depends(get_student_service),
) -> list[StudentResponse]:
    """Return every student currently stored in the database."""
    return service.get_all()


@router.get(
    "/{student_id}",
    response_model=StudentResponse,
    status_code=status.HTTP_200_OK,
    summary="Get a student by ID",
    responses={404: {"description": "Student not found."}},
)
def read_student(
    student_id: int,
    service: StudentService = Depends(get_student_service),
) -> StudentResponse:
    """Return a single student by ID, or 404 if not found."""
    student = service.get_by_id(student_id)
    if student is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Student with ID '{student_id}' was not found.",
        )
    return student


@router.put(
    "/{student_id}",
    response_model=StudentResponse,
    status_code=status.HTTP_200_OK,
    summary="Update an existing student",
    responses={
        404: {"description": "Student not found."},
        409: {"description": "A student with this email already exists."},
        422: {"description": "Validation error."},
    },
)
def update_student(
    student_id: int,
    student_in: StudentUpdate,
    service: StudentService = Depends(get_student_service),
) -> StudentResponse:
    """Update an existing student's information."""
    try:
        student = service.update(student_id, student_in)
    except StudentAlreadyExistsError as exc:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc)) from exc

    if student is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Student with ID '{student_id}' was not found.",
        )
    return student


@router.delete(
    "/{student_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a student",
    responses={404: {"description": "Student not found."}},
)
def delete_student(
    student_id: int,
    service: StudentService = Depends(get_student_service),
) -> None:
    """Delete a student by ID. Returns 204 on success, 404 if not found."""
    deleted = service.delete(student_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Student with ID '{student_id}' was not found.",
        )
    return None
