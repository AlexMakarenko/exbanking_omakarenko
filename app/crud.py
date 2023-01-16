from sqlalchemy.orm import Session

from . import models, schemas


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def update_balance(db: Session, email: str, new_balance: float):
    db_user = db.query(models.User).filter(models.User.email == email).first()
    db_user.balance = new_balance
    db.commit()
    db.refresh(db_user)
    return db_user


def send_amount(db: Session, user: schemas.UserCreate):
    sender = db.query(models.User).filter(models.User.email == user.email).first()
    receiver = db.query(models.User).filter(models.User.email == user.receiver_email).first()
    sender.balance -= user.amount
    receiver.balance += user.amount
    db.commit()
    db.refresh(sender)
    return sender


def create_user(db: Session, user: schemas.UserCreate):
    password = user.password
    db_user = models.User(email=user.email, password=password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
