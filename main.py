import numpy as np
import pickle
from sqlalchemy import Table, Column, Integer, String, DateTime, ForeignKey
from fastapi import FastAPI, File
from typing import List
from starlette.middleware.cors import CORSMiddleware
from passlib.context import CryptContext
from db import session
from model import t_member, t_login,  t_image
import jwt
import time
from datetime import datetime

from hangle import 지역, 성별, 지역상세, 혈액형, 음주, 흡연, 종교
import io
import uuid
import boto3
import base64

import uvicorn
import json

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
mb_data1 = []


# ------------------------ 회원가입 !-----------------------------------------
login = []


@app.post("/login/easy-auth/sign-up")
async def create_user(info: dict) -> dict:
    member = session.query(t_login.mb_no).filter().first()
    user = session.query(t_login).filter(
        (t_login.mb_email == info["email"])).first()  # 단일 사용자

    if user:
        print("아이디가 중복입니다.")

        return {"repeat": False}

    else:

        login.append(info)
        mb = t_member()
        im = t_image()
        lg = t_login()
        # lg.mb_name = info["nickname"]
        lg.mb_email = info["email"]
        lg.mb_pw = info["password"]
        lg.mb_pw = pwd_context.hash(lg.mb_pw)

        session.add(lg)
        session.commit()

        im.mb_no = lg.mb_no

        session.add(im)
        session.commit()

        mb.mb_no = lg.mb_no
        mb.mb_email = lg.mb_email
        session.add(mb)
        session.commit()

        member = session.query(t_login).filter(
            t_login.mb_no == mb.mb_no).first()
        print("아이디가 만들어졌습니다")
        email = lg.mb_email
        return {"isReady": True, "repeat": True, "email": email}


# --------------------------- 로그인!!--------------------------------------------
@app.post("/login")
async def add_login(info: dict):  # 가입정보를 딕셔너리 형태로 받아옴
    mb_data1.append(info)

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

    mb_data1.append(info)
    info["email"] = info["email"].replace('"', '', 2)
    user1 = session.query(t_login).filter(
        (t_login.mb_email == info["email"])).first()
    user_no = user1.mb_no
    user2 = session.query(t_member).filter(
        (t_member.mb_no == user_no)).first()
    if user2:
        # 성별
        user2.mb_gender = info["gender"]
        # 생년

        user2.mb_birthdate = info["birth"][0:4]
        # 지역
        user2.mb_region = info["region"]
        # 지역상세
        user2.mb_region_more = info["detailRegion"]
        # 결혼유무
        user2.mb_marriage_yn = info["married"]
        # 결혼 계획
        user2.mb_marriage_plan = info["marriagePlan"]
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
        if info["gender"] == 'f':
            sty = list(info["womanAppearance"].values())
            style = sty[0]
            user2.mb_style = style
        else:
            sty = list(info["manAppearance"].values())
            style = sty[0]
            user2.mb_style = style
        # 성격
        if info["gender"] == 'f':
            cha = list(info["womanPersonality"].values())
            character = ','.join(i for i in cha)
            user2.mb_character = character
        else:
            cha = list(info["manPersonality"].values())
            character = ','.join(i for i in cha)
            user2.mb_character = character
        # 패션스타일
        if info["gender"] == 'f':
            fas = list(info["womanFashion"].values())
            fashion = ','.join(i for i in fas)
            user2.mb_fashion = fashion
        else:
            fas = list(info["manFashion"].values())
            fashion = ','.join(i for i in fas)
            user2.mb_fashion = fashion
        # 직업
        user2.mb_job = info["job"]
        # 직업 상세
        user2.mb_job_more = info["jobInfo"]
        # 종교
        user2.mb_religion = info["religion"]
        # 학력
        user2.mb_academic = info["education"]
        # 재산
        user2.mb_asset = info["asset"]
        # 연봉
        user2.mb_salary = info["salary"]
        # 차량
        user2.mb_car = info["vehicle"]
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
    mb_data = []
    info["email"] = info["email"].replace('"', '', 2)
    user = session.query(t_login).filter(
        (t_login.mb_email == info["email"])).first()
    user_no = user.mb_no
    user_email = user.mb_email
    f_user = session.query(t_member).filter(
        t_member.mb_no == user_no).first()
   # 추천을 누른 회원의 데이터 정보 빼오기
    mb_data.append(f_user.mb_no)
    mb_data.append(f_user.mb_email)
    mb_data.append(f_user.mb_nickname)
    mb_data.append(f_user.mb_gender)
    mb_data.append(f_user.mb_region)
    mb_data.append(f_user.mb_region_more)
    mb_data.append(f_user.mb_birthdate)
    mb_data.append(f_user.mb_marriage_yn)
    mb_data.append(f_user.mb_photo_yn)
    mb_data.append(f_user.mb_photo_cnt)
    mb_data.append(f_user.mb_profile)
    mb_data.append(f_user.mb_job)
    mb_data.append(f_user.mb_job_more)
    mb_data.append(f_user.mb_salary)
    mb_data.append(f_user.mb_height)
    mb_data.append(f_user.mb_weight)
    mb_data.append(f_user.mb_religion)
    mb_data.append(f_user.mb_car)
    mb_data.append(f_user.mb_style)
    mb_data.append(f_user.mb_hobby)
    mb_data.append(f_user.mb_marriage_plan)
    mb_data.append(f_user.mb_fashion)
    mb_data.append(f_user.mb_asset)
    mb_data.append(f_user.mb_food)
    mb_data.append(f_user.mb_smoke_yn)
    mb_data.append(f_user.mb_drink_yn)
    mb_data.append(f_user.mb_health)
    mb_data.append(f_user.mb_age)
    print(np.array([mb_data]))

    return {'data': 'ㅋㅋ'}, mb_data  # 머신러닝 준비중

# 여기는 나중에 코드 줄여야겠당

# -------------이미지 s3 저장 및 웹으로 보내기 -------------------------------'


@app.put("/user-data-input/user-image-input")
async def create_image(info: dict):

    for i in range(0, 6):
        globals()["img"+str(i)] = info["formData"][i]
        img = globals()["img"+str(i)]   # 이미지 6개 딕셔너리를
        if globals()["img"+str(i)] == f"{''}":
            pass
        else:
            image1 = bytes(img, 'utf-8')  # 바이트로 변환

    ###### 지우지마####

        # print(len(userImage))  # 길이 확인할려고~
            userImage2 = str(image1)  # 스트링으로 다시 바꿔야 인식함
            userimage = userImage2[24:]  # data:image/bmp;base64< 이거 없애야 디코딩됨

            imgdata = base64.b64decode(userimage)  # 디코딩 하자
        # image =Image.open(io.BytesIO(imgdata)) # 이미지 오픈

        # image.show()#이미지보기
            file = io.BytesIO(imgdata)  # 디코딩 이미지 파일로 만들기
            # if img == globals()["img"+str(i)]:
            # 파일에 이름줘야함 {}<<이거써서 이메일같은거 넣으면될듯
            img_list = list(info["imageName"].values())
            file.name = img_list[i]
            print(file.name)

    # url = uuid.uuid1().hex  # 유니크한 네임 줘야함
            url = file.name
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

            # timage = t_image()  # 이미지 주소 디비 저장
            # timage.mb_image1 = url
            # session.add(timage)
            # session.commit()
    info["email"] = info["email"].replace('"', '', 2)
    user = session.query(t_login).filter(
        (t_login.mb_email == info["email"])).first()
    user_no = user.mb_no
    i_user = session.query(t_image).filter(
        t_image.mb_no == user_no).first()
    print(img_list)
    # if i_user.mb_no == user_no:
    # globals()["i_user.mb_image"+str(i+1)] = url
    # print(globals()["i_user.mb_image"+str(i+1)])
    # print(i_user.mb_image1)
    # print(i_user.mb_image2)
    i_user.mb_image1 = img_list[0]
    i_user.mb_image2 = img_list[1]
    i_user.mb_image3 = img_list[2]
    i_user.mb_image4 = img_list[3]
    i_user.mb_image5 = img_list[4]
    i_user.mb_image6 = img_list[5]

    session.add(i_user)
    session.commit()

    del img_list[:]
    return {"isAuthenticated": True}


# -------------- 유저 정보 수정 및 회원탈퇴 ---------------------------
@app.delete("/user-setting")
async def delete_user(info: dict):
    info["email"] = info["email"].replace('"', '', 2)
    print(info["email"])

  #   회원테이블 유저 정보 삭제
    user1 = session.query(t_member).filter_by(mb_email=info["email"]).first()

    session.delete(user1)
    session.commit()
  # 이미지 테이블 유저 정보 삭제
    user = session.query(t_login).filter_by(mb_email=info["email"]).first()
    user.mb_no == t_image.mb_no
    user2 = session.query(t_image).filter_by(mb_no=user.mb_no).first()

    session.delete(user2)
    session.commit()
  # 로그인 테이블 유저 정보 삭제
    user = session.query(t_login).filter_by(mb_email=info["email"]).first()
    user.mb_no == t_image.mb_no

    user1 = session.query(t_image).filter_by(mb_no=user.mb_no).first()

    session.delete(user)
    session.commit()

 # ---------------- 유저 정보 수정 및 정보 보여주는 창 ----------------------


@app.post("/user-setting/user-information-modify")
async def post_user(info: dict):
    info["email"] = info["email"].replace('"', '', 2)
    user = session.query(t_member).filter_by(mb_email=info["email"]).first()

    nickname = user.mb_nickname
    gender = 성별()[user.mb_gender]
    birth = user.mb_birthdate

    return {f"nickname": {nickname}, "gender": {gender}, "birth": {birth}, "email": info["email"]}
    # ------------------------- 메인페이지 유저 정보 보내기----------------------


# @app.post("/")
# async def user(info: dict):
#     info["email"] = info["email"].replace('"', '', 2)
#     user = session.query(t_member).filter((t_member.mb_no ==)).first()
#     gender = 성별()
#     region = 지역()
#     regionuser = 지역상세()
#     alcohol = 음주()
#     somke = 흡연()
#     religion = 종교()
#     job=직업()
#     print(user.mb_nickname)
#     print(gender[user.mb_gender])
    # print(user.mb_birthdate)
    # print(region[user.mb_region])
    # print(regionuser[user.mb_region_more])
    # print(user.mb_height)
    # print(user.mb_weight)
    # print(alcohol[user.mb_drinking_yn])
    # print(somke[user.mb_smoking_yn])
    # print(religion[user.mb_religion])
    # print(job[user.mb_job])

    # return gender[user.mb_gender]

    # if __name__ == '__main__':
    #     uvicorn .run(app, host="0.0.0.0", port=8000)
    #     pass
