import pickle
import numpy as np
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
from 전처리 import 종교전처리, 차전처리, 결혼계획전처리, 음주전처리, 운동전처리, 흡연전처리, 지역전처리
from hangle import 지역, 성별,  혈액형, 음주, 흡연, 운동, 결혼유무, 결혼계획, 학력, 직업, 연봉
from hangle import 자산, 차량, 혈액형, 남자외모, 여자외모, 남자패션, 여자패션, 남자성격, 여자성격
import io
import uuid
import boto3
import base64

import pymysql
from collections import ChainMap
import uvicorn
import json

# DB 접속코드 ---------------------
conn = pymysql.connect(host="project-db-stu.ddns.net", port=3307, user='inho',
                       password='k123456789', db='inho', charset='utf8')
cursor = conn.cursor(pymysql.cursors.DictCursor)
### 피클 자리##################################
woman = pickle.load(open("tree_model_man.pkl", 'rb'))
man = pickle.load(open("tree_model_woman.pkl", 'rb'))

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
## 닉네임 중복 처리 기능.
@app.post("/user-data-input/doubleCheck")
async def create_member(info: dict) -> dict:

    user2 = session.query(t_member).filter(t_member.mb_nickname == info["nickname"]).first()
    print(user2)
    # 닉네임
    if user2:
        print("gg")
        return {"doubleCheck" : False}
    else :
        print("zz")
        return {"doubleCheck" : True}

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
        user2.mb_birthdate = info["birth"]
        #닉네임
        user2.mb_nickname = info["nickname"]
        # 지역
        user2.mb_region = info["region"]
        # 지역상세
        user2.mb_region_more = info["detailRegion"]
        # 결혼유무
        user2.mb_marriage_yn = info["married"]
        # 결혼 계획
        user2.mb_marriage_plan = info["marriagePlan"]
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
        # 혈액형
        user2.mb_bloodtype = info["blood"]
        # 운동
        user2.mb_health = info["health"]
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
    print(info["email"])
    user = session.query(t_login).filter(
        (t_login.mb_email == info["email"])).first()
    user_no = user.mb_no
    user_email = user.mb_email
    f_user = session.query(t_member).filter(
        t_member.mb_no == user_no).first()
   # 추천을 누른 회원의 데이터 정보 빼오기
    user성별 =f_user.mb_gender
    data1 = f_user.mb_no
    data2 = f_user.mb_birthdate[:4]
    data3 = f_user.mb_job
    data4 = f_user.mb_height
    data5 = f_user.mb_weight
    data6 = f_user.mb_style
    for i in range(7,62):
        globals()['data'+str(i)]="0"
    if (f_user.mb_region_more)=="r":       
            data7=1 #재혼
            data8=0 #초혼
    else : ###"w"면
            data7=0
            data8=1
    종교전처리jc = 종교전처리()
    #####종교전처리#################################################################
    if 종교전처리jc[f_user.mb_religion] in 종교전처리jc :
        globals()['data'+str(종교전처리jc[종교전처리jc[f_user.mb_religion]])]="1"

    #################차전처리###########################################################
    차전처리jc = 차전처리()    
    if 차전처리jc[f_user.mb_car] in 차전처리jc :
        globals()['data'+str(차전처리jc[차전처리jc[f_user.mb_car]])]="1"
    ##### 결혼계획 전처리#######################################################
    결혼계획전처리jc = 결혼계획전처리()  
    if 결혼계획전처리jc[f_user.mb_marriage_plan] in 결혼계획전처리jc :
        globals()['data'+str(결혼계획전처리jc[결혼계획전처리jc[f_user.mb_marriage_plan]])]="1"
    ##### 음주처리######################################################
    음주전처리jc = 음주전처리()
    if 음주전처리jc[f_user.mb_drink_yn] in 음주전처리jc :
        globals()['data'+str(음주전처리jc[음주전처리jc[f_user.mb_drink_yn]])]="1"
    ######운동전처리 ###############################################################
    운동전처리jc = 운동전처리()
    if 운동전처리jc[f_user.mb_health] in 운동전처리jc :
        globals()['data'+str(운동전처리jc[운동전처리jc[f_user.mb_health]])]="1"
    ####### 흡연전처리 #######################################################
    흡연전처리jc = 흡연전처리()
   
    if 흡연전처리jc[f_user.mb_smoke_yn] in 흡연전처리jc :
        globals()['data'+str(흡연전처리jc[흡연전처리jc[f_user.mb_smoke_yn]])]="1"
    ############## 지역전처리###############################################
    지역전처리jc = 지역전처리()
    if 지역전처리jc[f_user.mb_region] in 지역전처리jc :
        globals()['data'+str(지역전처리jc[지역전처리jc[f_user.mb_region]])]="1"

    arr = np.array([[data1,data2,data3,data4,data5,data6,data7,data8,data9,data10,data11,data12,data13,data14,data15,data16,data17,data18,data19,data20,data21,data22,data23,data24,data25,data26,data27,data28,data29,data30,data31,data32,data33,data34,data35,data36,data37,data38,data39,data40,data41,data42,data43,data44,data45,data46,data47,data48,data49,data50,data51,data52,data53,data54,data55,data56,data57,data58,data59,data60,data61]])
    print(arr)

    if user성별=="m":
        pred = man.predict(arr)
        pred=pred.astype(int)
        print(pred)
    else :
        pred = woman.predict(arr)
        pred=pred.astype(int)
        print(pred)

    회원1 = pred[0]##### 문자열로변환    
###쿼리문#####@@@@@@@@@@@@@@@@@@@@@@@@
    sql회원정보 = f"select * from t_members where mb_no='{회원1}'"
    cursor.execute(query=sql회원정보)
    result1 = cursor.fetchall()
    디비정보 =result1
    print(디비정보)
    # DB를 리스트안에 딕셔너리로 빼오기
    no_user =ChainMap(*디비정보)
    sql회원이미지 = f"select * from t_image where img_no='{39}'" ### 일단 있는이미지 넣었음
    cursor.execute(query=sql회원이미지)
    result2 = cursor.fetchall()
    디비이미지 =result2
    print(디비이미지)
    no_image =ChainMap(*디비이미지)
   

    ### 리스트안 딕셔너리 데이터 찾을려고
 
    usernick = no_user['mb_no']
    userregion = 지역()[no_user['mb_region']]
    userjob = 직업()[no_user['mb_job']]
    userimage1 = no_image['mb_image1']

    print(usernick)
    print(userregion)
    print(userjob)
    print(userimage1)
    

    return {'nickname': usernick, 'region': userregion , "job" : userjob , "image" : userimage1}  # 머신러닝 준비중
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


# 회원 정보창에 프로필 정보 넘겨주기 ----------------------------------------------
@app.post("/user-setting")
async def delete_user(info: dict):
    info["email"] = info["email"].replace('"', '', 2)
    email = info["email"]
    # user1 = session.query(t_member).filter_by(mb_email=info["email"]).first()

    user = f"select * from t_members where mb_no='{email}'"
    cursor.execute(query=user)
    result1 = cursor.fetchall()
    user_data =result1
    print(user_data)
    

 # ---------------- 유저 정보 수정 및 정보 보여주는 창 ----------------------


@app.post("/user-setting/user-information-modify")
async def post_user(info: dict):
    info["email"] = info["email"].replace('"', '', 2)
    user = session.query(t_member).filter_by(mb_email=info["email"]).first()
    # 닉네임
    nickname = user.mb_nickname
    # 성별
    gender = 성별()[user.mb_gender]
    # 생일
    birth = user.mb_birthdate
    # 지역
    region = 지역()[user.mb_region]
    # 혈액형
    blood = 혈액형()[user.mb_bloodtype]
    # 운동
    health = 운동()[user.mb_health]
    # 음주
    drink = 음주()[user.mb_drink_yn]
    # 흡연
    smoke = 흡연()[user.mb_smoke_yn]
    # 결혼유무
    married = 결혼유무()[user.mb_marriage_yn]
    # 결혼계획
    married_plan = 결혼계획()[user.mb_marriage_plan]
    # 학력
    education = 학력()[user.mb_academic]
    # 직업
    job = 직업()[user.mb_job]
    # 직업상세
    job_more = user.mb_job_more
    # 연봉
    salary = 연봉()[user.mb_salary]
    # 자산
    asset = 자산()[user.mb_asset]
    # 차량
    car = 차량()[user.mb_car]
    # 외모
    style = user.mb_style.split(",")[0]
    if user.mb_gender == 'm':
        style = 남자외모()[user.mb_style]
    else:
        style = 여자외모()[user.mb_style]
        return style
    # 패션
    fashion = user.mb_fashion.split(",")
    fashionlist = []
    if user.mb_gender == "m":
        for i in fashion:
            a = 남자패션()[i]
            fashionlist.append(a)
    else:
        for i in fashion:
            a = 여자패션()[i]
            fashionlist.append(a)
        return fashionlist
    # 성격
    character = user.mb_character.split(",")
    characterlist = []
    if user.mb_gender == "m":
        for i in character:
            a = 남자성격()[i]
            characterlist.append(a)
    else:
        for i in character:
            a = 여자성격()[i]
            characterlist.append(a)
        return characterlist
    print(characterlist)
    # 이미지 테이블 이미지 불러오기
    user2 = user.mb_no
    u_image = session.query(t_image).filter(t_image.mb_no == user2).first()
    i1 = u_image.mb_image1
    i2 = u_image.mb_image2
    i3 = u_image.mb_image3
    i4 = u_image.mb_image4
    i5 = u_image.mb_image5
    i6 = u_image.mb_image6
    i_list = [i1,i2,i3,i4,i5,i6]
    img_list = []
    for i in i_list :
        if i == '' :
            i = 'default'
            img_list.append(i)
        else :
            img_list.append(i)
    image1 = img_list[0]
    image2 = img_list[1]
    image3 = img_list[2]
    image4 = img_list[3]
    image5 = img_list[4]
    image6 = img_list[5]
    print(img_list)
    return [{"nickname": nickname, "gender": gender, "birth": birth, "region": region,
            "blood": blood, "health": health, "drink": drink, "smoke": smoke, "married": married,
             "married_plan": married_plan, "education": education, "job": job, "salary": salary,
             "asset": asset, "car": car, "style": style, "fashion": fashionlist, "character": characterlist, "job_info": job_more,
             "image": {"image1": image1, "image2": image2, "image3": image3, "image4": image4,
                       "image5": image5, "image6": image6}}]

# 프론트에서 나의 이상형, 자기소개글 정보 받기
@app.put("/user-setting/user-information-modify")
async def put_user(info: dict):
    info["email"] = info["email"].replace('"', '', 2)
    if info["wanted"] == None :
        pass
    else :
        user = session.query(t_member).filter_by(mb_email=info["email"]).first()
        user.mb_ideal = info["wanted"]
        ideal = user.mb_ideal
    if info["introduce"] == None :
        pass
    else :
        user = session.query(t_member).filter_by(mb_email=info["email"]).first()
        user.mb_profile = info["introduce"]
        profile = user.mb_profile
    print(ideal, profile)
    
    session.add(user)
    session.commit()

    return "good"

@app.get("/user-setting/user-information-modify")
async def get_user(info: dict):
    info["email"] = info["email"].replace('"', '', 2)
    user = session.query(t_member).filter_by(mb_email=info["email"]).first()
    profile = user.mb_profile
    ideal = user.mb_ideal
    print(profile ,ideal)
    if user :
        return {"introduce": profile, "wanted": ideal}
    else :
        pass

# 프로필 수정에서 자기소개글 정보 넣기
# @app.put("/user-setting/user-information-modify")
# async def put_user(info: dict):
#     info["email"] = info["email"].replace('"', '', 2)
#     user = session.query(t_member).filter_by(mb_email=info["email"]).first()
#     user.mb_profile = info["introduce"]
#     profile = user.mb_profile

#     session.add(user)
#     session.commit()
    
#     return {"introduce" : profile}
    


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
