from fastapi import FastAPI, Depends, HTTPException, Request, Response
from app.database import get_db
from app.schemas import ProductCreate, ProductResponse, UserCreate, UserResponse, LoginRequest, InterestProduct
from app.crud import create_product, get_products, get_product_by_id, create_user, get_user_by_email, validate_user_password, get_product_count, create_interest_product, get_user_interest_products, check_interest_product_exists
from starlette.middleware.sessions import SessionMiddleware
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse
from motor.motor_asyncio import AsyncIOMotorClient
from typing import Dict, Any, List
import uuid
import logging

app = FastAPI()

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8002"],  # 허용할 프론트엔드 주소
    allow_credentials=True,
    allow_methods=["*"],  # 모든 HTTP 메서드 허용 (GET, POST 등)
    allow_headers=["*"],  # 모든 헤더 허용
)

app.add_middleware(SessionMiddleware, secret_key="your_secret_key")

logger = logging.getLogger("uvicorn")
logger.setLevel(logging.INFO)

@app.get("/")
def read_root():
    return {"Start": "Python Fast API"}

@app.post("/products_insert/", response_model=ProductResponse)
async def create_product_endpoint(product: ProductCreate, db = Depends(get_db)):
    return await create_product(db, product)

# 수입차 화물차 중고차량 개수 조회
@app.get("/count_products/", response_model=Dict[str, Any])
async def count_products(
    category: str = None,
    db: AsyncIOMotorClient = Depends(get_db)
):
    result = await get_product_count(
        db,
        category=category
    )
    # 개수를 dict로 감싸서 반환
    return {"count": result}

@app.get("/products/", response_model=Dict[str, Any])
async def read_products(
    page: int = 1,
    limit: int = 12,
    name: str = None,
    min_price: str = None,
    max_price: str = None,
    min_distance: str = None,
    max_distance: str = None,
    min_year: str = None,
    max_year: str = None,
    manufacturers: str = None,
    types: str = None,
    grade: str = None,
    category: str = None,
    db = Depends(get_db)
):
    skip = (page - 1) * limit
    result = await get_products(
        db,
        skip=skip,
        limit=limit,
        name=name,
        min_price=min_price,
        max_price=max_price,
        min_distance=min_distance,
        max_distance=max_distance,
        min_year=min_year,
        max_year=max_year,
        manufacturers=manufacturers,
        types=types,
        grade=grade,
        category=category
    )
    return result

@app.get("/products/{product_id}", response_model=ProductResponse)
async def read_product(product_id: str, db = Depends(get_db)):
    product = await get_product_by_id(db, product_id)
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@app.post("/register/", response_model=UserResponse)
async def register_user(user: UserCreate, db = Depends(get_db)):
    existing_user = await get_user_by_email(db, user.email)
    if existing_user:
        raise HTTPException(status_code=400, detail="이미 등록된 이메일입니다.")
    user_data = await create_user(db, user)
    return user_data

@app.post("/login/")
async def login_user(
    login_request: LoginRequest,
    response: Response,
    request: Request,
    db=Depends(get_db)
):
    user = await get_user_by_email(db, login_request.email)
    if not user:
        raise HTTPException(status_code=401, detail="이메일 또는 비밀번호가 잘못되었습니다.")
    
    if not await validate_user_password(user['password'], login_request.password):
        raise HTTPException(status_code=401, detail="이메일 또는 비밀번호가 잘못되었습니다.")

    # UUID 생성 후 세션 키로 사용
    session_key = str(uuid.uuid4())
    
    # 세션에 사용자 정보 저장 (UUID를 세션 ID로 사용)
    request.session['session_id'] = session_key
    request.session['user_id'] = str(user['_id'])
    request.session['username'] = user['name']  # 사용자 이름 저장

    # 로그로 세션 정보 확인
    logger.info(f"Session ID set: {session_key}")
    logger.info(f"User ID set in session: {request.session['user_id']}")

    # 쿠키 설정
    response = JSONResponse({
        "message": "로그인 성공",
        "username": user['name'],  # 사용자 이름 반환
        "user_id": str(user['_id'])  # 사용자 ID 반환
    })
    response.set_cookie(key="session_id", value=session_key, httponly=True, secure=False,  samesite="Lax", path="/" )  

    return response



@app.post("/logout/")
async def logout_user(request: Request, response: Response):
    # 세션 삭제
    request.session.clear()
    
    response = JSONResponse({"message": "로그아웃 성공"})
    response.delete_cookie(key="session_id")
    
    return response

@app.get("/check-session")
async def check_session(request: Request):
    session_id = request.cookies.get("session_id")
    if not session_id or session_id != request.session.get("session_id"):
        raise HTTPException(status_code=401, detail="로그인되지 않았습니다.")
    
    # 세션에 저장된 사용자 정보를 반환
    return {
        "message": "로그인 상태 유지",
        "user_id": request.session.get("user_id"),
        "username": request.session.get("username")
    }


@app.post("/create/interest_product/")
async def create_interest_product_endpoint(
    interest_product: InterestProduct,
    request: Request,
    db = Depends(get_db)
):
    session_id = request.cookies.get("session_id")
    
    # 로그로 세션 정보 확인
    logger.info(f"Session ID from cookie: {session_id}")
    logger.info(f"Session ID in session: {request.session.get('session_id')}")
    
    if not session_id or session_id != request.session.get("session_id"):
        raise HTTPException(status_code=401, detail="로그인되지 않았습니다.")
    
    user_id = request.session.get("user_id")
    if not user_id:
        raise HTTPException(status_code=401, detail="로그인되지 않았습니다.")
    
    # interest_product에 user_id 설정
    interest_product.user_id = user_id
    
    # 중복 확인
    if await check_interest_product_exists(db, user_id, interest_product.product_id):
        raise HTTPException(status_code=400, detail="이미 등록된 상품입니다.")
    
    # 관심 상품 생성
    result = await create_interest_product(db, interest_product)
    return result



@app.get("/user/interest_products/", response_model=List[InterestProduct])
async def get_user_interest_products_endpoint(request: Request, db = Depends(get_db)):
    session_id = request.cookies.get("session_id")
    
    # 로그로 세션 정보 확인
    logger.info(f"Session ID from cookie: {session_id}")
    logger.info(f"Session ID in session: {request.session.get('session_id')}")
    
    if not session_id or session_id != request.session.get("session_id"):
        raise HTTPException(status_code=401, detail="로그인되지 않았습니다.")
    
    user_id = request.session.get("user_id")
    if not user_id:
        raise HTTPException(status_code=401, detail="로그인되지 않았습니다.")
    
    # 관심상품 목록 조회
    interest_products = await get_user_interest_products(db, user_id)
    
    return interest_products
