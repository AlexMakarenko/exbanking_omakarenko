from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .database import SessionLocal, engine

models.Base.metadata.drop_all(bind=engine)
models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/create-user", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    elif not user.email:
        raise HTTPException(status_code=400, detail="Email is empty")
    elif len(user.password) < 8:
        raise HTTPException(status_code=400, detail="Minimum length of password is 8 symbols")
    return crud.create_user(db=db, user=user)


@app.post("/deposit", response_model=schemas.User)
def deposit(payload: schemas.ChangeBalance, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=payload.email)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    elif payload.amount < 0:
        raise HTTPException(status_code=400, detail="Incorrect amount")
    return crud.update_balance(db=db, email=payload.email, new_balance=db_user.balance + payload.amount)


@app.post("/withdraw", response_model=schemas.User)
def withdraw(payload: schemas.ChangeBalance, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=payload.email)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    elif db_user.balance < payload.amount:
        raise HTTPException(status_code=400, detail="Low balance")
    elif payload.amount <= 0:
        raise HTTPException(status_code=400, detail="Incorrect amount")
    return crud.update_balance(db=db, email=payload.email, new_balance=db_user.balance - payload.amount)


@app.get("/get-balance", response_model=schemas.UserBalance)
def get_balance(user: schemas.UserBase, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    return {"email": db_user.email, "balance": db_user.balance}


@app.post("/send", response_model=schemas.User)
def send(payload: schemas.SendAmount, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=payload.email)
    db_receiver = crud.get_user_by_email(db, email=payload.receiver_email)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    elif not db_receiver:
        raise HTTPException(status_code=404, detail="Receiver not found")
    elif db_user.balance < payload.amount:
        raise HTTPException(status_code=400, detail="Low balance")
    elif payload.amount <= 0:
        raise HTTPException(status_code=400, detail="Incorrect amount")
    return crud.send_amount(db=db, user=payload)
