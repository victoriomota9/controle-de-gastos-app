from typing import List, Optional
from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime
from models import TransactionType
from decimal import Decimal

class UserBase(BaseModel):
    id : int
    name : str
    email : str
    created_at : datetime
    updated_at : datetime

    model_config = ConfigDict(from_attributes=True)

class CategoryBase(BaseModel):
    id : int
    name : str
    is_default : bool
    description : str
    created_at : datetime
    updated_at : datetime

    model_config = ConfigDict(from_attributes=True)

class TransactionBase(BaseModel):
    id : int 
    type : TransactionType
    amount : Decimal
    transaction_date : datetime
    location : str
    created_at : datetime
    updated_at : datetime

    model_config = ConfigDict(from_attributes=True)

class TransactionResponse(TransactionBase):
    user_id : int
    category_id : int
    user : UserBase
    category : CategoryBase

class CategoryResponse(CategoryBase):
    user_id : Optional[int]
    user : Optional[UserBase]
    transactions : List[TransactionBase]


class UserResponse(UserBase):
    categories : List[CategoryBase]
    transactions : List[TransactionBase]

class UserCreate(BaseModel):
    name : str
    email : str
    password : str 

class CategoryCreate(BaseModel):
    name : str
    description : str

class TransactionCreate(BaseModel):
    category_id : int
    type : TransactionType
    amount : Decimal = Field(gt=0)
    transaction_date : datetime
    location : str
