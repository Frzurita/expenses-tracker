from datetime import datetime
from decimal import Decimal
from typing import Optional
from pydantic import BaseModel, Field


class ExpenseBase(BaseModel):
    """Base schema for expense with common fields."""
    title: str = Field(..., min_length=1, max_length=200, description="Expense title")
    amount: Decimal = Field(..., gt=0, description="Expense amount (must be positive)")
    description: Optional[str] = Field(None, max_length=1000, description="Expense description")


class ExpenseCreate(ExpenseBase):
    """Schema for creating a new expense."""
    pass


class ExpenseUpdate(BaseModel):
    """Schema for updating an existing expense."""
    title: Optional[str] = Field(None, min_length=1, max_length=200, description="Expense title")
    amount: Optional[Decimal] = Field(None, gt=0, description="Expense amount (must be positive)")
    description: Optional[str] = Field(None, max_length=1000, description="Expense description")


class ExpenseResponse(ExpenseBase):
    """Schema for expense response."""
    id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

