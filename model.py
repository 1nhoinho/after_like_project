from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
# coding: utf-8
from sqlalchemy import Column, Integer, String
from pydantic import BaseModel,EmailStr
from database import Base



class t_login(Base):
    __tablename__ = "t_login"

    mb_no = Column(Integer, primary_key=True, autoincrement=True)
    mb_name = Column(String(255), nullable=False)
    mb_email = Column(String(255),nullable=False)
    mb_pw = Column(String(255), nullable=False)


class t_member(Base):
    __tablename__ = "t_member"
    mb_no= Column(Integer, ForeignKey('t_login.mb_no'),  primary_key=True)
    t_login = relationship("t_login", backref="t_member")
    # mb_no= Column(Integer, primary_key=True)
    mb_gender = Column(String(255),nullable=True)
    mb_region = Column(String(255), nullable=True)
    mb_region_more =Column(String(255), nullable=True)
    mb_birthdate =Column(String(255), nullable=True)
    mb_marriage_yn = Column(String(255),nullable=True)
    mb_photo_yn = Column(String(255),nullable=True)
    mb_photo_cnt = Column(Integer, nullable=True)   #인트형
    mb_profile =Column(String(255), nullable=True)
    mb_job=Column(String(255), nullable=True)
    mb_job_more =Column(String(255), nullable=True)
    mb_salary = Column(Integer,nullable=True)        #인트형
    mb_height = Column(Integer, nullable=True)
    mb_weight = Column(Integer, nullable=True)  
    mb_car =Column(String(255), nullable=True)
    mb_academic =Column(String(255), nullable=True)
    mb_style = Column(String(255),nullable=True)
    mb_charicter = Column(String(255), nullable=True)
    mb_hobby =Column(String(255), nullable=True)
    mb_marriage_plan =Column(String(255), nullable=True)
    mb_fashion = Column(String(255),nullable=True)
    mb_asset = Column(Integer, nullable=True)           ##인트형
    mb_food =Column(String(255), nullable=True)
    mb_smoking_yn =Column(String(255), nullable=True)
    mb_drinking_yn = Column(String(255),nullable=True)
    mb_health_manage = Column(String(255), nullable=True)
    mb_joindate =Column(String(255), nullable=True)
    mb_blood=Column(String(255), nullable=True)   
    mb_religion=Column(String(255), nullable=True)    
    mb_info_update_cnt =Column(String(255), nullable=True)
    

    

class UserCreate(BaseModel):
    mb_name: str
    mb_email: EmailStr
    password: str
    checkPW : str

class Token(BaseModel):
    access_token: str
    token_type: str
    mb_email: str




