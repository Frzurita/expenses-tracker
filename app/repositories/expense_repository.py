from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy.exc import NoResultFound

from app.models.expense import Expense
from app.schemas.expense import ExpenseCreate, ExpenseUpdate


class ExpenseRepository:
    """Repository for expense data access operations."""
    
    def __init__(self, db: Session):
        self.db = db
    
    def create(self, expense: ExpenseCreate) -> Expense:
        """Create a new expense."""
        db_expense = Expense(
            title=expense.title,
            amount=expense.amount,
            description=expense.description
        )
        self.db.add(db_expense)
        self.db.commit()
        self.db.refresh(db_expense)
        return db_expense
    
    def get_by_id(self, expense_id: int) -> Optional[Expense]:
        """Get an expense by ID."""
        return self.db.query(Expense).filter(Expense.id == expense_id).first()
    
    def get_all(self, skip: int = 0, limit: int = 100) -> List[Expense]:
        """Get all expenses with pagination."""
        return self.db.query(Expense).offset(skip).limit(limit).all()
    
    def update(self, expense_id: int, expense_update: ExpenseUpdate) -> Optional[Expense]:
        """Update an existing expense."""
        db_expense = self.get_by_id(expense_id)
        if not db_expense:
            return None
        
        update_data = expense_update.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_expense, field, value)
        
        self.db.commit()
        self.db.refresh(db_expense)
        return db_expense
    
    def delete(self, expense_id: int) -> bool:
        """Delete an expense by ID."""
        db_expense = self.get_by_id(expense_id)
        if not db_expense:
            return False
        
        self.db.delete(db_expense)
        self.db.commit()
        return True

