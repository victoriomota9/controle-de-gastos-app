from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload
import models, schemas
from database import engine, SessionLocal
from typing import List
from security import hash_password

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/users/", response_model=schemas.UserResponse)
def registerUser(user_create : schemas.UserCreate,
                      db : Session = Depends(get_db)
                      ):

    existing = db.query(models.User).filter(models.User.email == user_create.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email is being used already.")
    
    db_user = models.User(name=user_create.name,
                          email=user_create.email,
                          hashed_password=hash_password(user_create.password)
                          )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

"""
@app.get("/users/", response_model=List[schemas.UserResponse])
def listar_usuarios(skip: int = 0, limit: int = 20, db : Session = Depends(get_db)):
    stmt = select(models.User).options(
        selectinload(models.User.categories), 
        selectinload(models.User.transactions)
        ).offset(skip).limit(limit)
    users = db.execute(stmt).scalars().all()
    return users
"""
#TODO: MUDAR QUANDO TIVER AUTH
@app.post("/categories/", response_model=schemas.CategoryResponse)
def registerCategory(category_create : schemas.CategoryCreate,
                     db : Session = Depends(get_db)
                     ):
    db_category = models.Category(
        name=category_create.name,
        description=category_create.description
    )
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category

#TODO: QUANDO TIVER AUTH MUDAR O FILTRO
@app.get("/categories/", response_model=List[schemas.CategoryResponse])
def getCategories(skip: int = 0, limit: int = 20, db : Session = Depends(get_db)):
    query = select(models.Category).options(
        selectinload(models.Category.transactions)
    ).offset(skip).limit(limit)
    categories = db.execute(query).scalars().all()
    return categories

@app.post("/transactions", response_model=schemas.TransactionResponse)
def registerTransaction(transaction_create : schemas.TransactionCreate,
                        db : Session = Depends(get_db)):
    db_transaction = models.Transaction(
        user_id = 1, #TODO: TIRAR QUANDO TIVER AUTH
        category_id=transaction_create.category_id,
        type=transaction_create.type,
        amount=transaction_create.amount,
        transaction_date=transaction_create.transaction_date,
        location=transaction_create.location
    )
    db.add(db_transaction)
    db.commit()
    db.refresh(db_transaction)
    return db_transaction

@app.get("/transactions/", response_model=List[schemas.TransactionResponse])
def getTransactionByCategory(
    category_id : int | None = None,
    skip : int = 0,
    limit : int = 20,
    db : Session=Depends(get_db)
    ):
    query = select(models.Transaction).where(models.Transaction.category_id == category_id)
    query = query.offset(skip).limit(limit)
    transactions = db.execute(query).scalars().all()
    return transactions