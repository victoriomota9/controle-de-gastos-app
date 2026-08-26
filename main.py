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
def cadastrar_usuario(user : schemas.UserCreate,
                      db : Session = Depends(get_db)
                      ):

    existing = db.query(models.User).filter(models.User.email == user.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email is being used already.")
    
    db_user = models.User(name=user.name,
                          email=user.email,
                          hashed_password=hash_password(user.password)
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

