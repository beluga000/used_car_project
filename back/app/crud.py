from app.schemas import ProductCreate, UserCreate, InterestProduct
from motor.motor_asyncio import AsyncIOMotorClient
from typing import Optional, Dict, Any, List
from bson import ObjectId
import bcrypt
import re 


def serialize_object_id(obj):
    if isinstance(obj, ObjectId):
        return str(obj)
    raise TypeError(f"Type {type(obj)} not serializable")

# 데이터 직렬화 예시
def serialize_data(data):
    if isinstance(data, dict):
        return {key: serialize_data(value) for key, value in data.items()}
    elif isinstance(data, list):
        return [serialize_data(item) for item in data]
    elif isinstance(data, ObjectId):
        return str(data)
    return data

async def create_product(db, product: ProductCreate):
    product_dict = product.dict()
    result = await db.get_collection("used_car_products").insert_one(product_dict)
    product_dict["id"] = str(result.inserted_id)
    return product_dict

# 수입차 화물차 중고차량 개수 조회 개수만 리턴
async def get_product_count(db: AsyncIOMotorClient, category: str = None):
    query = {}
    if category:
        query = {"type": category}
    return await db.get_collection("used_car_products").count_documents(query)

async def get_products(
    db, 
    skip: int = 0, 
    limit: int = 10, 
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
    category: str = None
    
):
    query = {"$and": []}

    if name:
        query["$and"].append({"name": {"$regex": name, "$options": "i"}})

    if grade:
        # 특수 문자를 이스케이프 처리하고 정규식으로 검색
        escaped_grade = re.escape(grade)
        query["$and"].append({"grade": {"$regex": escaped_grade, "$options": "i"}})
    
    if category:
        query["$and"].append({"type": category})

    # 가격 필터링
    try:
        min_price_value = int(min_price.replace(',', '')) if min_price else None
        max_price_value = int(max_price.replace(',', '')) if max_price else None

        if min_price_value is not None and max_price_value is not None:
            query["$and"].append({"price_unit": {"$gte": min_price_value, "$lte": max_price_value}})
        elif min_price_value is not None:
            query["$and"].append({"price_unit": {"$gte": min_price_value}})
        elif max_price_value is not None:
            query["$and"].append({"price_unit": {"$lte": max_price_value}})
    except ValueError:
        pass

    # 주행거리 필터링
    try:
        min_distance_value = int(min_distance.replace(' km', '').replace(',', '')) if min_distance else None
        max_distance_value = int(max_distance.replace(' km', '').replace(',', '')) if max_distance else None

        if min_distance_value is not None and max_distance_value is not None:
            query["$and"].append({"distance_unit": {"$gte": min_distance_value, "$lte": max_distance_value}})
        elif min_distance_value is not None:
            query["$and"].append({"distance_unit": {"$gte": min_distance_value}})
        elif max_distance_value is not None:
            query["$and"].append({"distance_unit": {"$lte": max_distance_value}})
    except ValueError:
        pass

    # 연식 필터링
    if min_year and max_year:
        query["$and"].append({
            "year": {
                "$gte": min_year,
                "$lte": max_year
            }
        })
    elif min_year:
        query["$and"].append({"year": {"$gte": min_year}})
    elif max_year:
        query["$and"].append({"year": {"$lte": max_year}})

    # 제조사 및 모델 필터링
    if manufacturers and types:
        manufacturers_list = manufacturers.split(",")
        types_list = types.split(",")
        query["$and"].append({
            "$and": [
                {"manufacturer": {"$in": manufacturers_list}},
                {"model": {"$in": types_list}}
            ]
        })
    elif manufacturers:
        manufacturers_list = manufacturers.split(",")
        query["$and"].append({"manufacturer": {"$in": manufacturers_list}})
    elif types:
        types_list = types.split(",")
        query["$and"].append({"model": {"$in": types_list}})

    # 쿼리 조건이 없을 경우 빈 쿼리로 설정
    if not query["$and"]:
        query = {}

    total_count = await db.get_collection("used_car_products").count_documents(query)
    page = (skip // limit) + 1
    page_offset = skip
    products = await db.get_collection("used_car_products").find(query).skip(skip).limit(limit).to_list(length=limit)

    for product in products:
        product["id"] = str(product["_id"])
        del product["_id"]

    return {
        "total": total_count,
        "page": page,
        "page_offset": page_offset,
        "limit": limit,
        "products": products
    }

async def get_product_by_id(db, product_id: str):
    product = await db.get_collection("used_car_products").find_one({"_id": ObjectId(product_id)})
    if product:
        product["id"] = str(product["_id"])
    return product

async def create_user(db, user: UserCreate):
    hashed_password = bcrypt.hashpw(user.password.encode('utf-8'), bcrypt.gensalt())
    user_dict = user.dict()
    user_dict['password'] = hashed_password.decode('utf-8')
    result = await db.get_collection("users").insert_one(user_dict)
    user_dict['id'] = str(result.inserted_id)
    return user_dict

async def get_user_by_email(db, email: str) -> Optional[dict]:
    return await db.get_collection("users").find_one({"email": email})

async def validate_user_password(stored_password: str, provided_password: str) -> bool:
    return bcrypt.checkpw(provided_password.encode('utf-8'), stored_password.encode('utf-8'))


#  관심상품 생성
async def create_interest_product(db, interest_product: InterestProduct):
    interest_product_dict = interest_product.dict()
    result = await db.get_collection("interest_products").insert_one(interest_product_dict)
    interest_product_dict["id"] = str(result.inserted_id)  # ObjectId를 문자열로 변환
    return serialize_data(interest_product_dict)


async def get_user_interest_products(db, user_id: str) -> List[dict]:
    collection = db.get_collection("interest_products")
    cursor = collection.find({"user_id": user_id})
    results = await cursor.to_list(length=100)  # 최대 100개의 결과를 조회
    return results

# 관심상품 존재 여부 확인
async def check_interest_product_exists(db, user_id: str, product_id: str) -> bool:
    collection = db.get_collection("interest_products")
    count = await collection.count_documents({"user_id": user_id, "product_id": product_id})
    return count > 0
