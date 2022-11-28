# coding: utf-8
from sqlalchemy import Table, Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from pydantic import BaseModel
from db import Base
from db import ENGINE


class t_member(Base):
    __tablename__ = 't_members'
    mb_no = Column(Integer, primary_key=True, autoincrement=True)
    mb_email = Column(String(45), ForeignKey(
        "t_logins.mb_email"), nullable=False)
    mb_nickname = Column(String(45), nullable=True)
    mb_gender = Column(String(45), nullable=True)
    mb_region = Column(String(45), nullable=True)
    mb_region_more = Column(String(45), nullable=True)
    mb_birthdate = Column(String(45), nullable=True)
    mb_marriage_yn = Column(String(45), nullable=True)
    mb_photo_yn = Column(String(45), nullable=True)
    mb_photo_cnt = Column(String(45), nullable=True)
    mb_profile = Column(String(500), nullable=True)
    mb_job = Column(String(45), nullable=True)
    mb_job_more = Column(String(45), nullable=True)
    mb_salary = Column(String(45), nullable=True)
    mb_height = Column(String(45), nullable=True)
    mb_weight = Column(String(45), nullable=True)
    mb_religion = Column(String(45), nullable=True)
    mb_car = Column(String(45), nullable=True)
    mb_academic = Column(String(45), nullable=True)
    mb_style = Column(String(45), nullable=True)
    mb_character = Column(String(45), nullable=True)
    mb_hobby = Column(String(45), nullable=True)
    mb_marriage_plan = Column(String(45), nullable=True)
    mb_fashion = Column(String(45), nullable=True)
    mb_asset = Column(String(45), nullable=True)
    mb_food = Column(String(60), nullable=True)
    mb_smoke_yn = Column(String(45), nullable=True)
    mb_drink_yn = Column(String(45), nullable=True)
    mb_health = Column(String(45), nullable=True)
    mb_joindate = Column(DateTime, nullable=True)
    mb_info_update = Column(DateTime, nullable=True)
    mb_age = Column(String(45), nullable=True)

    # login = relationship("t_login", back_populates="member", uselist=False)
    mail = relationship("t_login", back_populates="email")


class member(BaseModel):
    mb_no = int
    mb_email = str
    mb_nickname = str
    mb_gender = str
    mb_region = str
    mb_region_more = str
    mb_birthdate = str
    mb_marriage_yn = str
    mb_photo_yn = str
    mb_photo_cnt = str
    mb_profile = str
    mb_job = str
    mb_job_more = str
    mb_salary = str
    mb_height = str
    mb_weight = str
    mb_religion = str
    mb_car = str
    mb_academic = str
    mb_style = str
    mb_character = str
    mb_hobby = str
    mb_marriage_plan = str
    mb_fashion = str
    mb_asset = str
    mb_food = str
    mb_smoke = str
    mb_drink = str
    mb_health = str
    mb_joindate = str
    mb_info_update = str
    mb_age = str


class t_login(Base):
    __tablename__ = 't_logins'
    mb_no = Column(Integer, primary_key=True, autoincrement=True)
    mb_email = Column(String(45), nullable=False, unique=True)
    mb_pw = Column(String(300), nullable=False)

    # member = relationship("t_member", back_populates="login")
    email = relationship("t_member", back_populates="mail")


class login(BaseModel):
    mb_no = int
    mb_email = str
    mb_pw = str


def main():
    # Table 없으면 생성
    Base.metadata.create_all(bind=ENGINE)


if __name__ == "__main__":
    main()
