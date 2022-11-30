from sqlalchemy import Table, Column, Integer, String, DateTime, ForeignKey
from fastapi import FastAPI
from typing import List
from starlette.middleware.cors import CORSMiddleware
from passlib.context import CryptContext

from db import session
from model import t_member, t_login, t_user
import jwt
import time
from datetime import datetime

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

app = FastAPI()

ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24
SECRET_KEY = "21e7a7483f3348e9ae812e130882056a1d4aeb068e5cf6266e936635a0723601"
ALGORITHM = "HS256"

origins = [
    "http://localhost:3000",
    "localhost:3000"
]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# ----------API 정의------------
mb_data = []


# ------------------------ 회원가입 !-----------------------------------------
login = []


@app.post("/login/easy-auth/sign-up")
async def create_user(info: dict) -> dict:
    member = session.query(t_login.mb_no).filter().first()
    user = session.query(t_login).filter(
        (t_login.mb_email == info["email"])).first()  # 단일 사용자

    if user:
        print("아이디가 중복입니다.")
        print(member)
        return {"repeat": False}

    else:

        login.append(info)
        mb = t_member()
        us = t_user()
        lg = t_login()
        # lg.mb_name = info["nickname"]
        lg.mb_email = info["email"]
        lg.mb_pw = info["password"]
        lg.mb_pw = pwd_context.hash(lg.mb_pw)

        session.add(lg)
        session.commit()

        us.mb_no = lg.mb_no

        session.add(us)
        session.commit()

        member = session.query(t_login).filter(
            t_login.mb_no == us.mb_no).first()
        print("아이디가 만들어졌습니다")
        print(us.mb_no)
        email = lg.mb_email
        print(email)
        return {"isReady": True, "email": email}


# --------------------------- 로그인!!--------------------------------------------
@app.post("/login")
async def add_login(info: dict):  # 가입정보를 딕셔너리 형태로 받아옴
    mb_data.append(info)
    print(info)

    password = info["password"]

    user = session.query(t_login).filter(
        t_login.mb_email == info["email"]).first()  # 단일 사용자
    email = t_login.mb_email
    if not user or not pwd_context.verify(password, user.mb_pw):
        print("비밀번호나 아이디가 틀렸습니다.")
        return {"isAuthenticated": False}
    else:
        print("로그인완료")
        return {"isAuthenticated": True, "email": email}


# ------------------------상세정보 입력----------------------------------------------
@app.put("/user-data-input")
async def create_member(info: dict) -> dict:

    mb_data.append(info)
    info["email"] = info["email"].replace('"', '', 2)
    user1 = session.query(t_login).filter(
        (t_login.mb_email == info["email"])).first()
    user_no = user1.mb_no
    user2 = session.query(t_user).filter(
        (t_user.mb_no == user_no)).first()
    print(user2)
    if user2:
        print(user2)
        # 성별
        user2.mb_gender = info["gender"]
        # 생년

        user2.mb_birthdate = info["birth"][0:4]
        # 지역
        user2.mb_region = info["region"]
        # 지역상세
        user2.mb_region = info["detailRegion"]
        # 결혼유무
        user2.mb_marriage_yn = info["married"]
        # 재산
        user2.mb_region = info["asset"]
        # 닉네임
        user2.mb_nickname = info["nickname"]
        # 몸무게
        user2.mb_weight = info["weight"]
        # 키
        user2.mb_height = info["height"]
        # 음주여부
        user2.mb_drink_yn = info["alcohol"]
        # 흡연여부
        user2.mb_smoke_yn = info["smoke"]
        # 가입 시간
        user2.mb_joindate = time.localtime()
        # 업데이트 시간
        user2.mb_info_update = time.localtime()
        # 나이
        user2.mb_age = datetime.today().year - int(info["birth"][0:4]) + 1

        session.add(user2)
        session.commit()
        print(datetime.today().year)
        return {"isCompleted": True}
    else:
        print("ㅋㅋ")


# --------------상호추천 알고리즘 적용, 추출 ---------------------------------------------

@app.post("/recommend")
async def create_member(info: dict) -> dict:
    return {'data': 'ㅋㅋ'}

    # @app.put("/users")
    # # users=[{"id": 1, "name": "이름1", "age": 16},{"id": 2, "name": "이름2", "age": 20}]
    # async def user1_users(users: List[User]):

    #     for i in users:
    #         user = session.query(t_member).filter(
    #             t_member.user_no == i.user_no).first()
    #         user.user_id = i.user_id
    #         user.user_pw = i.user_pw
    #         user.user_age = i.user_age
    #         session.commit()

    #     return f"{i.user_pw} 정보 변경이 완료 되었습니다."
