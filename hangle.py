# 1성별

def 성별():
    gender = {"m": "남자",
              "f": "여자"}
    return gender
# 2 생년월일

# 3 몸무게

# 4 키

# 5 지역


def 지역():
    region = {
        "a": "강원도",
        "b": "경기도",
        "c": "경상남도",
        "d": "경상북도",
        "e": "광주",
        "f": "대구",
        "g": "대전",
        "h": "부산",
        "i": "서울",
        "z": "세종",
        "j": "울산",
        "k": "인천",
        "l": "전라남도",
        "n": "전라북도",
        "m": "제주도",
        "o": "충청남도",
        "p": "충청북도",
        "q": "해외"}
    return region


def 지역상세():
    regionuser = {"p01": "괴산군",
                  "p02": "단양군",
                  "p03": "보은군",
                  "p04": "영동군",
                  "p05": "옥천군",
                  "p06": "음성군",
                  "p07": "제천시",
                  "p08": "증평군",
                  "p09": "진천군",
                  "p10": "청주시 상당구",
                  "p11": "청주시 서원구",
                  "p12": "청주시 청원구",
                  "p13": "청주시 흥덕구",
                  "p14": "충주시",
                  "o01": "계룡시",
                  "o02": "공주시",
                  "o03": "금산군",
                  "o04": "논산시",
                  "o05": "당진시",
                  "o06": "보령시",
                  "o07": "부여군",
                  "o08": "서산시",
                  "o09": "서천군",
                  "o10": "아산시",
                  "o11": "예산군",
                  "o12": "천안시 동남구",
                  "o13": "천안시 서북구",
                  "o14": "청양군",
                  "o15": "태안군",
                  "o16": "홍성군",
                  "o00": "기타",
                  "f01": "남구",
                  "f02": "달서구",
                  "f03": "달성군",
                  "f04": "동구",
                  "f05": "북구",
                  "f06": "서구",
                  "f07": "수성구",
                  "f08": "중구",
                  "f00": "기타",
                  "g01": "대덕구",
                  "g02": "동구",
                  "g03": "서구",
                  "g04": "유성구",
                  "g05": "중구",
                  "g00": "기타",
                  "q01": "해외",
                  "e01": "광산구",
                  "e02": "남구",
                  "e03": "동구",
                  "e04": "북구",
                  "e05": "서구",
                  "e00": "기타",
                  "d01": "경산시",
                  "d02": "경주시",
                  "d03": "고령군",
                  "d04": "구미시",
                  "d05": "군위군",
                  "d06": "김천시",
                  "d07": "문경시",
                  "d08": "봉화군",
                  "d09": "상주시",
                  "d10": "성주군",
                  "d11": "안동시",
                  "d12": "영덕군",
                  "d13": "영양군",
                  "d14": "영주시",
                  "d15": "영천시",
                  "d16": "예천군",
                  "d17": "울릉군",
                  "d18": "울진군",
                  "d19": "의성군",
                  "d20": "청도군",
                  "d21": "청송군",
                  "d22": "칠곡군",
                  "d23": "포항시 남구",
                  "d24": "포항시 북구",
                  "d00": "기타",
                  "b01": "가평군",
                  "b02": "고양시 덕양구",
                  "b03": "고양시 일산동구",
                  "b04": "고양시 일산서구",
                  "b05": "과천시",
                  "b06": "광명시",
                  "b07": "광주시",
                  "b08": "구리시",
                  "b09": "군포시",
                  "b10": "김포시",
                  "b11": "남양주시",
                  "b12": "동두천시",
                  "b13": "부천시",
                  "b16": "성남시 분당구",
                  "b17": "성남시 수정구",
                  "b18": "성남시 중원구",
                  "b19": "수원시 권선구",
                  "b20": "수원시 영통구",
                  "b21": "수원시 장안구",
                  "b22": "수원시 팔달구",
                  "b23": "시흥시",
                  "b24": "안산시 단원구",
                  "b25": "안산시 상록수",
                  "b26": "안성시",
                  "b27": "안양시 동안구",
                  "b28": "안양시 만안구",
                  "b29": "양주시",
                  "b30": "양평군",
                  "b31": "여주시",
                  "b32": "연천군",
                  "b33": "오산시",
                  "b34": "용인시 기흥구",
                  "b35": "용인시 수지구",
                  "b36": "용인시 처인구",
                  "b37": "의왕시",
                  "b38": "의정부시",
                  "b39": "이천시",
                  "b40": "파주시",
                  "b41": "평택시",
                  "b42": "포천시",
                  "b43": "하남시",
                  "b44": "화성시",
                  "b00": "기타",
                  "c01": "거제시",
                  "c02": "거창군",
                  "c03": "고성군",
                  "c04": "김해시",
                  "c05": "남해군",
                  "c06": "창원시 마산합포구",
                  "c07": "밀양시",
                  "c08": "사천시",
                  "c09": "산청군",
                  "c10": "양산시",
                  "c11": "의령군",
                  "c12": "진주시",
                  "c13": "창원시 진해구",
                  "c14": "창녕군",
                  "c15": "창원시 성산구",
                  "c16": "통영시",
                  "c17": "하동군",
                  "c18": "함안군",
                  "c19": "함양군",
                  "c20": "합천군",
                  "c21": "창원시 마산회원구",
                  "c22": "창원시 의창구",
                  "c00": "기타",
                  "k01": "강화군",
                  "k02": "계양구",
                  "k03": "미추홀구",
                  "k04": "남동구",
                  "k05": "동구",
                  "k06": "부평구",
                  "k07": "서구",
                  "k08": "연수구",
                  "k09": "옹진군",
                  "k10": "중구",
                  "k00": "기타",
                  "m01": "제주시",
                  "m02": "서귀포시",
                  "n01": "고창군",
                  "n02": "군산시",
                  "n03": "김제시",
                  "n04": "남원시",
                  "n05": "무주군",
                  "n06": "부안군",
                  "n07": "순창군",
                  "n08": "완주군",
                  "n09": "익산시",
                  "n10": "임실군",
                  "n11": "장수군",
                  "n12": "전주시 덕진구",
                  "n13": "전주시 완산구",
                  "n14": "정읍시",
                  "n15": "진안군",
                  "n00": "기타",
                  "l01": "강진군",
                  "l02": "고흥군",
                  "l03": "곡성군",
                  "l04": "광양시",
                  "l05": "구례군",
                  "l06": "나주시",
                  "l07": "담양군",
                  "l08": "목포시",
                  "l09": "무안군",
                  "l10": "보성군",
                  "l11": "순천시",
                  "l12": "신안군",
                  "l13": "여수시",
                  "l14": "영광군",
                  "l15": "영암군",
                  "l16": "완도군",
                  "l17": "장성군",
                  "l18": "장흥군",
                  "l19": "진도군",
                  "l20": "함평군",
                  "l21": "해남군",
                  "l22": "화순군",
                  "l00": "기타",
                  "a01": "강릉시",
                  "a02": "고성군",
                  "a03": "동해시",
                  "a04": "삼척시",
                  "a05": "속초시",
                  "a06": "양구군",
                  "a07": "양양군",
                  "a08": "영월군",
                  "a09": "원주시",
                  "a10": "인제군",
                  "a11": "정선군",
                  "a12": "철원군",
                  "a13": "춘천시",
                  "a14": "태백시",
                  "a15": "평창군",
                  "a16": "홍천군",
                  "a17": "화천군",
                  "a18": "횡성군",
                  "a00": "기타",
                  "z01": "세종",
                  "i01": "강남구",
                  "i02": "강동구",
                  "i03": "강북구",
                  "i04": "강서구",
                  "i05": "관악구",
                  "i06": "광진구",
                  "i07": "구로구",
                  "i08": "금천구",
                  "i09": "노원구",
                  "i10": "도봉구",
                  "i11": "동대문구",
                  "i12": "동작구",
                  "i13": "마포구",
                  "i14": "서대문구",
                  "i15": "서초구",
                  "i16": "성동구",
                  "i17": "성북구",
                  "i18": "송파구",
                  "i19": "양천구",
                  "i20": "영등포구",
                  "i21": "용산구",
                  "i22": "은평구",
                  "i23": "종로구",
                  "i24": "중구",
                  "i25": "중랑구",
                  "i00": "기타",
                  "j01": "남구",
                  "j02": "동구",
                  "j03": "북구",
                  "j04": "울주군",
                  "j05": "중구",
                  "j00": "기타"}

    return regionuser


def 혈액형():
    blood = {"1": "A형",
             "2": "B형",
             "3": "O형",
             "4": "AB형", }
    return blood


def 음주():
    alcohol = {"a": "음주 안함",
               "b": "월1-2회",
               "c": "주1-2회",
               "d": "주3회이상"}

    return alcohol


def 흡연():
    smoke = {"a": "비흡연",
             "b": "금연",
             "c": "흡연"}
    return smoke


def 종교():
    religion = {"1": "기독교",
                "2": "불교",
                "3": "천주교",
                "4": "원불교",
                "5": "무교",
                "6": "유교",
                "7": "도교",
                "8": "이슬람교",
                "9": "힌두교",
                "0": "기타"}
    return religion


def 음주():
    marriagePlan = {"1m": "1달 이내",
                    "3m": "3달 이내",
                    "6m": "6달 이내",
                    "1y": "1년 이내",
                    "a": "언제든지"}
    return marriagePlan


def 직업():
    jobList = ["기타",
               "경영",
               "마케팅",
               "무역",
               "유통",
               "연구/개발",
               "기계",
               "전기",
               "자동차",
               "서비스",
               "교육",
               "금융",
               "영업",
               "문화/예술",
               "방송",
               "연극/영화",
               "IT",
               "인터넷",
               "디자인",
               "건설",
               "의료/보건",
               "정부/행정",
               "농업",
               "자영업",
               "전문직/특수직",
               "취업준비",
               "창업준비",
               "프리랜서",
               "아르바이트",
               "학생",
               "법률",
               "공기업/기관",
               "군인/군무원",
               "스포츠",
               "사회복지",
               "운송",
               "물류/배송",
               "설치",
               "외국어/번역",
               "보안/경비/경호",
               "뷰티",
               "외식",
               "숙박",
               "조선",
               "판매",
               "증권",
               "회계/세무",
               "고객상담",
               "부동산/임대",
               "신문/잡지",
               "기획",
               "사무/관리",
               "홍보/광고",
               "정비/AS",
               "미용/이용",
               "예식",
               "장례",
               "프랜차이즈",
               "여행",
               "생산/제조",
               "전자",
               "가스/수도",
               "금속/재료",
               "섬유화학",
               "석유화학",
               "정유",
               "식품공학",
               "식품가공/제조",
               "의류",
               "유아/완구",
               "투자",
               "보험",
               "공연",
               "공예",
               "도서/출판",
               "사진",
               "인쇄/인화",
               "음악/악기",
               "엔터테인먼트",
               "게임",
               "만화/웹툰",
               "통신",
               "ICT",
               "반도체",
               "LED/광산업",
               "환경",
               "모바일",
               "로봇",
               "나노",
               "바이오",
               "신소재",
               "신재생에너지",
               "우주/항공",
               "인테리어",
               "토목",
               "설계",
               "제약",
               "종교",
               "어업",
               "축산업",
               "임업",
               "광산업",
               "빅데이터",
               "낙농업"]
    job = {str(i): jobList[i] for i in range(len(jobList))}
    return job


def 학력():
    education = {"1": "초/중학교",
                 "2": "고등학교",
                 "3": "대학교",
                 "4": "대학원",
                 "5": "박사과정",
                 "6": "대학교(2년)",
                 "7": "대학재학",
                 "8": "대학중퇴",
                 "9": "대학원재학",
                 "10": "대학원중퇴",
                 "11": "박사학위",
                 "12": "대학(3년)",
                 "0": "기타"}
    return education


def 연봉():
    salary = {"1": "적음",
              "12": "2천 미만",
              "2": "2천대",
              "3": "3천대",
              "4": "4천대",
              "5": "5천대",
              "6": "6천대",
              "7": "7천대",
              "8": "8천대",
              "90": "9천대",
              "10": "1-3억",
              "13": "3억-5억",
              "14": "5-10억",
              "15": "10-20억",
              "18": "20-30억",
              "16": "30억 이상"}
    return salary


def 자산():
    asset = {
        "3천만원 미만": "b",
        "3천만원~7천만원 미만": "c",
        "7천만원~1억 미만": "d",
        "1억~3억 미만": "e",
        "3억~5억 미만": "f",
        "5억~10억 미만": "g",
        "10억~20억 미만": "h",
        "20억~30억 미만": "m",
        "30억~50억 미만": "i",
        "50억~100억 미만": "j",
        "100억~300억 미만": "k",
        "300억~500억 미만": "l",
        "500억 이상": "n"}
    return asset


def 차량():
    vehicle = {"1": "소형",
               "2": "준중형",
               "3": "중형",
               "4": "대형",
               "5": "수입",
               "6": "SUV",
               "7": "승합",
               "9": "없음",
               "10": "기타"}
    return vehicle


def 취미():
    vehicle = {"0": "기타",
               "1": "반려동물",
               "2": "종교/정치",
               "3": "요리/맛집탐방",
               "4": "사교활동",
               "5": "패션/미용",
               "6": "야외활동",
               "7": "실내활동",
               "8": "문화생활",
               "9": "미디어/온라인",
               "10": "운동"}
    return vehicle


def 운동():
    health = {"a": "숨쉬기 운동",
              "b": "월1-2회",
              "c": "주1-2회",
              "d": "주3회이상"}

    return health


def 남자외모():
    mamapperance = {"1": "#평범함",
                    "2": "#귀여움",
                    "3": "#섹시함",
                    "4": "#꽃미남",
                    "5": "#날씬함",
                    "6": "#듬직함",
                    "7": "#뚱뚱함",
                    "8": "#깔끔함"}
