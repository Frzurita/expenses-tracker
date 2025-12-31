from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.expense import ExpenseCreate, ExpenseUpdate, ExpenseResponse
from app.repositories.expense_repository import ExpenseRepository

router = APIRouter(prefix="/expenses", tags=["expenses"])


def get_expense_repository(db: Session = Depends(get_db)) -> ExpenseRepository:
    """Dependency to get expense repository."""
    return ExpenseRepository(db)


@router.post(
    "",
    response_model=ExpenseResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new expense",
    description="Create a new expense entry with title, amount, and optional description"
)
def create_expense(
    expense: ExpenseCreate,
    repository: ExpenseRepository = Depends(get_expense_repository)
):
    """Create a new expense."""
    return repository.create(expense)


@router.get(
    "",
    response_model=List[ExpenseResponse],
    summary="List all expenses",
    description="Get a list of all expenses with optional pagination"
)
def list_expenses(
    skip: int = 0,
    limit: int = 100,
    repository: ExpenseRepository = Depends(get_expense_repository)
):
    """Get all expenses."""
    return repository.get_all(skip=skip, limit=limit)


@router.get(
    "/{expense_id}",
    response_model=ExpenseResponse,
    summary="Get expense by ID",
    description="Retrieve a specific expense by its ID"
)
def get_expense(
    expense_id: int,
    repository: ExpenseRepository = Depends(get_expense_repository)
):
    """Get an expense by ID."""
    expense = repository.get_by_id(expense_id)
    if not expense:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Expense with id {expense_id} not found"
        )
    return expense


@router.put(
    "/{expense_id}",
    response_model=ExpenseResponse,
    summary="Update an expense",
    description="Update an existing expense by ID"
)
def update_expense(
    expense_id: int,
    expense_update: ExpenseUpdate,
    repository: ExpenseRepository = Depends(get_expense_repository)
):
    """Update an expense."""
    expense = repository.update(expense_id, expense_update)
    if not expense:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Expense with id {expense_id} not found"
        )
    return expense


@router.delete(
    "/{expense_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete an expense",
    description="Delete an expense by ID"
)
def delete_expense(
    expense_id: int,
    repository: ExpenseRepository = Depends(get_expense_repository)
):
    """Delete an expense."""
    success = repository.delete(expense_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Expense with id {expense_id} not found"
        )
    return None

