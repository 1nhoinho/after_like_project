from sqlalchemy.orm import Session
from model import UserCreate
from model import t_login
from passlib.context import CryptContext
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# def get_existing_user():
#     return Session.query(t_login).filter(
#         (t_login.mb_name == UserCreate.mb_name) |
#         (t_login.mb_email == UserCreate.mb_email)
#     ).first()


# def get_user(db: Session, info["email"]: str):
#     return db.query(t_login).filter(t_login.mb_name == info["email"]).first()