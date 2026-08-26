from sqlalchemy import Integer, String, Numeric, ForeignKey, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database import Base
from datetime import datetime
from typing import List, Optional
from enum import Enum
from decimal import Decimal

class TransactionType(Enum):
    INCOME = "income"
    EXPENSE = "expense"


class User(Base):
    __tablename__ = "users"

    id : Mapped[int] = mapped_column(primary_key=True)
    name : Mapped[str]
    email : Mapped[str] = mapped_column(String(255), unique=True)
    hashed_password : Mapped[str] = mapped_column(String(255))
    created_at : Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    ) 
    updated_at : Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )
    categories : Mapped[List["Category"]] = relationship(back_populates="user")
    transactions : Mapped[List["Transaction"]] = relationship(back_populates="user")

class Category(Base):
    __tablename__ = "categories"
    id : Mapped[int] = mapped_column(primary_key=True, index=True)
    name : Mapped[str] = mapped_column(String(100))
    user_id : Mapped[Optional[int]] = mapped_column(ForeignKey("users.id"), nullable=True)
    is_default : Mapped[bool] = mapped_column(default=False)
    description : Mapped[str] = mapped_column(String(255))
    created_at : Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at : Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )
    user : Mapped[Optional["User"]] = relationship(back_populates="categories")
    transactions : Mapped[List["Transaction"]] = relationship(back_populates="category")

class Transaction(Base):
    __tablename__ = "transactions"
    id : Mapped[int] = mapped_column(primary_key=True, index=True)
    user_id : Mapped[int] = mapped_column(ForeignKey("users.id"))
    category_id : Mapped[int] = mapped_column(ForeignKey("categories.id"))
    type : Mapped[TransactionType] = mapped_column() 
    amount : Mapped[Decimal] = mapped_column(Numeric(10,2)) 
    transaction_date : Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    location : Mapped[str] = mapped_column(String(300))
    created_at : Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
        )
    updated_at : Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
        )
    user : Mapped["User"] = relationship(back_populates="transactions")
    category : Mapped["Category"] = relationship(back_populates="trasactions")
    