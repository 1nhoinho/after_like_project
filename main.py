from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from passlib.context import CryptContext
from datetime import timedelta, datetime
from hashing import Hasher
from sqlalchemy.orm import Session
from hangle import 성별, 지역, 지역상세, 음주, 흡연, 종교, 직업
from database import session

from jose import jwt
import model


from model import t_login, t_member,UserCreate
from database import engine

model.Base.metadata.create_all(bind=engine)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


app = FastAPI()
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24
SECRET_KEY = "21e7a7483f3348e9ae812e130882056a1d4aeb068e5cf6266e936635a0723601"
ALGORITHM = "HS256"

origins = [
    "http://localhost:3000",
    "localhost:3000"
]

infos = []

#### 머신러닝################################################################################################################





#####################################################################################################
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


############################################################################### 로그인!!!!!! 연습
# @app.get("/login")
# async def read_root() -> dict:
#     return { "data": infos  }
# # @app.post("/login/easy-auth/signup", tags=["todos"])
# # async def add_signin(info: dict) -> dict:
#     infos.append(info)
#     email = info["email"]
#     password = info["password"]
#     user = session.query(t_login).filter(t_login.mb_email==email).first()
#     if user is None:
#         print("이메일이 존재하지않습니다.")
#     else:
#         if Hasher.verify_password(password, user.mb_pw):
#             data = {"sub": email}
#             jwt_token = jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)
            

#             set_cookie(
#                     key="access_token", value=f"Bearer {jwt_token}", httponly=True
#                 )
#             return{"Fasle" :"Fasle"},origins
####################################################################################################
################ 연습@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
# @app.post("/login")
# async def user_login(info: dict) :
#     infos.append(info)
#     ab = session.query(t_login).filter(t_login.mb_email == info["email"]).first() ## 단일 사용자
#     user1 = t_login()
#     user1.mb_email = info["email"]
#     user1.mb_pw = info["password"]
#     data = {"email": "{user1.mb_email}", "password": "{user1.mb_pw}"}


#     user = jsonable_encoder(data)
  
#     if user["email"]== info['email'] and user["password"]== info['password']:

#         encoded_jwt = jwt.encode(user, SECRET_KEY, algorithm=ALGORITHM)
#         print("로그인성공")
#         return {"token": encoded_jwt}

#     else:
#         print("로그인실패")
#         return {"message":"login failed"}
#################################################################################################################   





























############## 로그인 ###################################################################
@app.get("/login")
async def read_root() -> dict:
    return { "data": infos  }        
    
     
@app.post("/login")
async def add_login(info: dict) : # 가입정보를 딕셔너리 형태로 받아옴
    infos.append(info)
    print(info)
    
 
    password = info["password"]

    user = session.query(t_login).filter(t_login.mb_email == info["email"]).first() ## 단일 사용자
   

    if not user or not pwd_context.verify(password, user.mb_pw):
        print("비밀번호나 아이디가 틀렸습니다.")
        return { "isAuthenticated" : False }
    else:
        
        print("로그인완료")
        return { "isAuthenticated" : True }
    
###################################################################################################



## 회원가입!!! 




@app.post("/login/easy-auth/sign-up")
async def add_signin(info: dict) -> dict:
    infos.append(info)
    a = info["email"]
    
    user = session.query(t_login).filter((t_login.mb_email == info["email"])).first() ## 단일 사용자
 

    if user:
        print("아이디가 중복입니다.")
        return { "repeat" :False }
    
    else:
        print("아이디가 만들어졌습니다")
        uname = t_login()
        uname.mb_name = info["nickname"]
        uname.mb_email = info["email"]
        uname.mb_pw = info["password"]
        uname.mb_pw = pwd_context.hash(uname.mb_pw)
        
        session.add(uname)
        session.commit()
        return {"isReady": True, "repeat": True}

@app.get("/login/easy-auth/sign-up")
async def 성공() -> dict:
    # await add_signin()
    user = session.query(t_login).all() ## 단일 사용자
    # data ={"1":1}
    
    # return user, data
    return user
    



##############################################################################################################################

### user-setting 임 ############################################################################################################
@app.get("/user-setting")
async def read_ui() -> dict:
    return { "data": infos  }
@app.post("/user-setting")
async def add_ui(info: dict) -> dict:
    infos.append(info)
    # print(info["gender"]) #걍넣어짐
    # print(info["birth"])
    # print(info["region"])

#######지역상세 줄인거입니다.##################################
    user = (info["regionInfo"])
    print(user.keys())
    결과=[]
    for k, v in user.items():
        k = v
        결과.append(k)
    print(결과)
    리스트지역상세=[s for s in 결과 if '{}'.format(info["region"]) in s]
    print(리스트지역상세)
    regionInfo = '\n'.join(리스트지역상세)
    print(regionInfo)
    
#########################################################################
####### 한글뱉기#########################################################

    gender = 성별()
    region = 지역()
    regionuser = 지역상세()
    print(gender[info["gender"]])
    print(info["birth"])
    print(info["height"])
    print(info["weight"])
    print(region[info["region"]])
    print(regionuser[regionInfo])
  

    
        
   

##############################################################################
#####데이터 저장##################################################################
    member = t_member()
    member.mb_gender = info["gender"] # 성별
    member.mb_birthdate = info["birth"]# 생일
    member.mb_height =  info["height"]#  키  
    member.mb_weight =  info["weight"]#  몸무게  
    member.mb_region = info["region"] # 지역
    member.mb_region_more =regionInfo # 지역상세
    # member.mb_blood = info["blood"]# 혈액형               DB안넣음
    member.mb_drinking_yn = info["alcohol"] # 음주
    # member.mb_smoking_yn = info["smoke"] # 흡연
    member.mb_religion = info["religion"]### 종교   DB확인
    member.mb_job = info["job"]### 직업           
    member.mb_academic = info["education"] #학력
    # member.mb_salary = info["salary"]# 연봉
    # member.mb_asset= info["asset"] # 재산
    member.mb_car= info["vehicle"] # 차소유
    member.mb_marriage_yn = info["married"]# 결혼유무
    member.mb_marriage_plan =info["marriagePlan"] ## 결혼계획
    session.add(member)
    session.commit()
    return { "data": infos}
##############################################################################
######데이터 디비 뱉기#########################################################
@app.post("/user-setting/3")#//1<<<<<<<<<<<<<<<넣어야 찾아짐???왜그럼?
async def read_add(info: dict) -> dict:
    infos.append(info)
    user = session.query(t_member).filter((t_member.mb_no == "3")).first()
    gender = 성별()
    region = 지역()
    regionuser = 지역상세()
    alcohol =음주()
    # somke = 흡연()
    religion=종교()
    job=직업()

    print(gender[user.mb_gender])
    print(user.mb_birthdate)
    print(user.mb_height)
    print(user.mb_weight)
    print(region[user.mb_region])
    print(regionuser[user.mb_region_more])
    print(alcohol[user.mb_drinking_yn])
    # print(somke[user.mb_smoking_yn])
    print(religion[user.mb_religion])
    print(job[user.mb_job])
  



    


    
    return { "data": "하하하"}
#######################################################################################

















