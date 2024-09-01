from pydantic import BaseModel, EmailStr
from typing import List

class Product(BaseModel):
    id: str
    name: str
    price: str
    price_unit: int
    color: str
    year: str
    distance: str
    distance_unit: int
    fuel: str
    accident: str
    tax_unpaid: str
    img: List[str]
    in_options: List[str]
    out_options: List[str]
    safe_options: List[str]
    conv_options: List[str]
    type: str
    manufacturer: str
    model: str
    is_assurance: bool
    is_home: bool
    number: str
    main_img: str
    seize: str
    grade: str
    o_in_options: List[bool]
    o_out_options: List[bool]
    o_safe_options: List[bool]
    o_conv_options: List[bool]




class User(BaseModel):
    id: str
    name: str
    email: str
    password: str
    phone: str
    address: str
    postcode: str
    birth: str

class LoginRequest(BaseModel):
    email: EmailStr
    password: str



class InterestProduct(BaseModel):
    product_id: str
    user_id: str

class UserInterestProduct(BaseModel):
    id: str
    product_id: str
    user_id: str