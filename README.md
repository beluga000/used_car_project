# 1. 앱에 대한 설명

이 프로젝트는 중고차 거래 플랫폼의 애플리케이션입니다. FastAPI와 MongoDB를 기반으로 만들어졌으며, 
사용자 계정 관리, 제품 등록, 제품 목록 조회, 관심 상품 등록 등의 주요 기능을 제공합니다. 또한 세션을 사용한 로그인 및 로그아웃 기능과 함께 이미지를 업로드하여 중고차 제품에 등록할 수 있습니다.

### 주요 기능

	•	사용자 관리: 회원가입, 로그인, 로그아웃 및 세션 유효성 검사
	•	중고차 등록 및 조회: 중고차 데이터를 등록, 조회, 조건에 따른 필터링 및 검색
	•	이미지 업로드: 제품 등록 시 이미지 파일을 함께 업로드 가능
	•	관심 상품 관리: 사용자가 관심 있는 제품을 등록하고 조회 가능
 	•	CORS 및 세션 처리: 클라이언트와 서버 간의 안정적인 통신을 보장하고, 사용자의 세션을 유지하여 보안을 강화

# 2. 소스 빌드 및 실행 방법 메뉴얼(DB 스키마 포함)

	•	Python 3.8 이상
	•	MongoDB 데이터베이스 설치
	•	Node JS 설치
	•	Quasar 설치

### 2.1 MongoDB 데이터베이스 설정
MongoDB가 설치된 상태에서 mongod 서비스를 시작하고, 2.2.5 데이터베이스 및 컬렉션을 생성합니다:

### 2.2 소스 빌드 및 실행 방법

#### 2.2.1 소스코드 다운로드 및 빌드 
프로젝트를 클론하거나 다운로드 후, 프로젝트의 back 디렉터리로 이동합니다.

가상환경 설정 및 활성화 진행합니다.

```
# 가상환경 생성
python3 -m venv venv

# 가상환경 활성화 (MacOS/Linux)
source venv/bin/activate

# 가상환경 활성화 (Windows)
venv\Scripts\activate
```

필요한 패키지 설치
```
pip install -r requirements.txt
```

#### 2.2.3 애플리케이션 실행
다음 명령어를 Back 디렉터리 위치에서 실행하여 Fast API 애플리케이션을 시작합니다.
```
uvicorn main:app --reload
```

다음 명령어를 Front/used_car_project 디렉터리 위치에서 실행하여 Quasar 애플리케이션을 시작합니다.
```
npx quasar dev
```


#### 2.2.5 DB 스키마

used_car_products
```
{
  "_id": ObjectId,
  "name": "차량명",
  "price_unit": 15000000, // 가격
  "distance_unit": 50000, // 주행 거리
  "year": 2021, // 제조 연도
  "manufacturer": "현대", // 제조사
  "model": "쏘나타", // 모델명
  "type": "세단", // 차량 종류
  "img": ["경로1", "경로2"] // 업로드한 이미지 경로
}
```

users
```
{
  "_id": ObjectId,
  "name": "사용자명",
  "email": "user@example.com",
  "password": "해시된_비밀번호"
}
```

interest_products
```
{
  "_id": ObjectId,
  "user_id": "사용자 ID",
  "product_id": "상품 ID"
}

```

# 3. 주력으로 사용한 컴포넌트에 대한 설명 및 사용 이유

1️⃣ Fast API

FastAPI는 비동기 처리를 지원하며, Python의 최신 기능을 활용해 고성능 API를 구축할 수 있습니다. 자동으로 생성되는 API 문서화 기능도 뛰어나서 개발 편의성을 높여줍니다.

2️⃣ MongoDB (Motor)

MongoDB는 NoSQL 데이터베이스로, 비정형 데이터를 저장하는 데 적합합니다. 특히 중고차 제품의 다양한 속성들을 스키마 없이 쉽게 저장할 수 있으며, Motor 라이브러리를 통해 비동기 데이터베이스 처리가 가능합니다.

3️⃣ SessionMiddleware

사용자의 로그인 상태를 세션을 통해 유지하고, 이를 통해 지속적인 사용자 경험을 제공합니다.

4️⃣ aiofiles

이미지 업로드 시 비동기 파일 처리를 위한 라이브러리로, FastAPI의 비동기 성능을 유지하면서 파일을 효율적으로 저장할 수 있습니다.

5️⃣ bcrypt

비밀번호를 해시화하여 보안을 강화하며, 사용자 인증 시 안전한 방식으로 비밀번호를 비교할 수 있습니다.


# 4. API 명세(Swagger 사용)

Swagger UI는 애플리케이션이 실행될 때 자동으로 생성됩니다. 모든 API 엔드포인트는 http://localhost:8080/swagger-ui.html에서 확인할 수 있습니다. 아래는 주요 API와 설명입니다.

1️⃣ POST /register: 유저 생성<br>
Request Body (JSON)
```
{
  "name": "사용자명",
  "email": "user@example.com",
  "password": "비밀번호"
}
```
Response
```
{
  "id": "생성된 사용자 ID",
  "name": "사용자명",
  "email": "user@example.com"
}

```
2️⃣ POST /login : 로그인<br>
Request Body (JSON)
```
{
  "email": "user@example.com",
  "password": "비밀번호"
}
```
Response
```
{
  "message": "로그인 성공",
  "username": "사용자명",
  "user_id": "사용자 ID"
}
```

3️⃣ POST /logout: 로그아웃<br>
Response
```
{
  "message": "로그아웃 성공"
}

```

4️⃣ POST /products_insert : 제품 등록<br>
Request Body (JSON)
```
{
  "name": "차량명",
  "price_unit": 15000000,
  "distance_unit": 50000,
  "year": 2021,
  "manufacturer": "현대",
  "model": "쏘나타",
  "type": "세단"
}
```
Response
```
{
  "id": "생성된 제품 ID",
  "name": "차량명",
  "price_unit": 15000000,
  "distance_unit": 50000,
  "year": 2021,
  "manufacturer": "현대",
  "model": "쏘나타",
  "type": "세단"
}
```
5️⃣ GET /products : 제품 목록 조회<br>
Query Parameter : page, limit, name, min_price, max_price, min_distance, max_distance, min_year, max_year, manufacturers, types, grade, category<br>
Response
```
{
  "total": 100,  // 총 제품 수
  "page": 1,
  "products": [
    {
      "id": "제품 ID",
      "name": "차량명",
      "price_unit": 15000000,
      ...
    }
  ]
}

```

6️⃣ POST /create/interest_product : 관심 상품 등록<br>
Request Body (JSON)
```
{
  "product_id": "상품 ID"
}
```
Response
```
{
  "id": "생성된 관심 상품 ID",
  "user_id": "사용자 ID",
  "product_id": "상품 ID"
}
```

7️⃣ GET /user/interest_products : 사용자 관심 상품 조회<br>
```
[
  {
    "id": "관심 상품 ID",
    "user_id": "사용자 ID",
    "product_id": "상품 ID"
  }
]

```
