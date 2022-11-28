
from fastapi import FastAPI
from typing import List
from starlette.middleware.cors import CORSMiddleware
from passlib.context import CryptContext

from db import session
from model import t_member, t_login
import jwt

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
        lg = t_login()
        # lg.mb_name = info["nickname"]
        lg.mb_email = info["email"]
        lg.mb_pw = info["password"]
        lg.mb_pw = pwd_context.hash(lg.mb_pw)

        session.add(lg)
        session.commit()

        mb.mb_no = lg.mb_no

        session.add(mb)
        session.commit()

        member = session.query(t_login).filter(
            t_login.mb_no == mb.mb_no).first()
        print("아이디가 만들어졌습니다")
        print(mb.mb_no)
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

    if not user or not pwd_context.verify(password, user.mb_pw):
        print("비밀번호나 아이디가 틀렸습니다.")
        return {"isAuthenticated": False}
    else:
        print("로그인완료")
        return {"isAuthenticated": True}


# ------------------------상세정보 입력----------------------------------------------
region = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h',
          'i', 'j', 'k', 'l', 'n', 'm', 'o', 'p', 'q', 'z']
region_more = ["region_kangwon", "region_gyungki", "region_chungnam", "region_chungbuk", "region_gwangju", "region_daegu", "region_daejeon",
               "region_busan", "region_seoul", "region_ulsan", "region_incheon", "region_jeonnam", "region_jeju", "region_jeonbuk", "region_hungnam",
               "region_chungbuk", "region_foreign", "region_sejong"]


@app.put("/user-data-input")
async def create_member(info: dict) -> dict:

    mb_data.append(info)
    member = t_member()
    login = session.query(t_login).filter(
        t_login.mb_email == info["mail"]).first()
    update = session.query(t_member).filter(
        t_member.mb_no == login.mb_no).first()

    # 성별
    update.mb_gender = info["gender"]
    # 생년
    update.mb_birthdate = info["birth"]
    # 지역
    update.mb_region = info["region"]
    # 지역상세
    update.mb_region = info["detailRegion"]
    # 결혼유무
    update.mb_marriage_yn = info["married"]
    # 재산
    update.mb_region = info["asset"]
    # 닉네임
    update.mb_nickname = info["nickname"]
    # 몸무게
    update.mb_weight = info["weight"]
    # 키
    update.mb_height = info["height"]
    # 음주여부
    update.mb_drink_yn = info["alcohol"]
    # 흡연여부
    update.mb_smoke_yn = info["smoke"]

    session.add(update)
    session.commit()

    return print(f" 정보가 생성되었습니다.")


# @app.put("/users")
# # users=[{"id": 1, "name": "이름1", "age": 16},{"id": 2, "name": "이름2", "age": 20}]
# async def update_users(users: List[User]):

#     for i in users:
#         user = session.query(t_member).filter(
#             t_member.user_no == i.user_no).first()
#         user.user_id = i.user_id
#         user.user_pw = i.user_pw
#         user.user_age = i.user_age
#         session.commit()

#     return f"{i.user_pw} 정보 변경이 완료 되었습니다."


# @app.delete("/user")
# async def delete_users(user_id: str):

#     user = session.query(t_member).filter(
#         t_member.user_id == user_id).delete()
#     session.commit()

#     return f"삭제가 완료되었습니다."
