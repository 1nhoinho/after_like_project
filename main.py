from sqlalchemy import Table, Column, Integer, String, DateTime, ForeignKey
from fastapi import FastAPI, File
from typing import List
from starlette.middleware.cors import CORSMiddleware
from passlib.context import CryptContext

from db import session
from model import t_member, t_login, t_user, t_image
import jwt
import time
from datetime import datetime

import io
import uuid
import boto3
import base64


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

        mb.mb_email = lg.mb_email

        session.add(mb)
        session.commit()

        member = session.query(t_login).filter(
            t_login.mb_no == mb.mb_no).first()
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
    if not user or not pwd_context.verify(password, user.mb_pw):
        print("비밀번호나 아이디가 틀렸습니다.")
        return {"isAuthenticated": False}
    else:
        print("로그인완료")
        return {"isAuthenticated": True, "email": info["email"]}


# ------------------------상세정보 입력----------------------------------------------
@app.put("/user-data-input")
async def create_member(info: dict) -> dict:

    mb_data.append(info)
    info["email"] = info["email"].replace('"', '', 2)
    user1 = session.query(t_login).filter(
        (t_login.mb_email == info["email"])).first()
    user_no = user1.mb_no
    user2 = session.query(t_member).filter(
        (t_member.mb_no == user_no)).first()
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
        # 외모
        if '0' in info["manAppearance"]:
            sty = list(info["manAppearance"].values())
            style = ','.join(i for i in sty)
            user2.mb_style = style
        else:
            sty = list(info["womanAppearance"].values())
            style = ','.join(i for i in sty)
            user2.mb_style = style
        # 성격

        # 가입 시간
        user2.mb_joindate = time.localtime()
        # 업데이트 시간
        user2.mb_info_update = time.localtime()
        # 나이
        user2.mb_age = datetime.today().year - int(info["birth"][0:4]) + 1

        session.add(user2)
        session.commit()
        style = list(info["manAppearance"].values())
        return {"isCompleted": True}

    else:
        print("ㅋㅋ")


# --------------상호추천 알고리즘 적용, 추출 ---------------------------------------------

@app.post("/recommend")
async def create_member(info: dict) -> dict:
    info["email"] = info["email"].replace('"', '', 2)
    print(info["email"])
    user = session.query(t_login).filter(
        (t_login.mb_email == info["email"])).first()
    user_no = user.mb_no
    user_email = user.mb_email
    print(user_no)
    return {'data': 'ㅋㅋ'}

# -------------이미지 s3 저장 및 웹으로 보내기 -------------------------------


@app.put("/user-data-input/user-image-input")
async def create_file(userImage: bytes = File(...)):
   ###### 지우지마####
    print(len(userImage))  # 길이 확인할려고~
    userImage2 = str(userImage)  # 스트링으로 바꿔야 인식함
    userimage = userImage2[24:]  # data:image/bmp;base64< 이거 없애야 디코딩됨

    imgdata = base64.b64decode(userimage)  # 디코딩 하자
    # image =Image.open(io.BytesIO(imgdata)) # 이미지 오픈
    # image.show()#이미지보기
    file = io.BytesIO(imgdata)  # 디코딩 이미지 파일로 만들기
    file.name = "123.png"  # 파일에 이름줘야함 {}<<이거써서 이메일같은거 넣으면될듯

    url = uuid.uuid1().hex  # 유니크한 네임 줘야함

    s3_client = boto3.client(  # aws 접속코드
        service_name="s3",
        region_name="ap-northeast-2",
        aws_access_key_id="AKIAW3XAAHKCN3ZSO6LT",
        aws_secret_access_key="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"
    )

    s3_client.upload_fileobj(  # aws업로드
        file,
        "notfound-404",  # 버킷이름
        url,  # 여기에 주소결정
        ExtraArgs={
            "ContentType": "public-read"
        }
    )

    image_url = url  # 업로드된 이미지의 url이 설정값으로 저장됨
    timage = t_image()  # 이미지 주소 디비 저장
    timage.mb_image = image_url
    session.add(timage)
    session.commit()
    print(image_url)

    return {"True"}
