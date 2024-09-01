from pydantic import BaseModel,EmailStr,Field
from typing import List, Optional




class ProductBase(BaseModel):
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
    is_home: bool
    is_assurance: bool
    number: str
    main_img: str
    seize: str
    grade: str
    o_in_options: List[bool]
    o_out_options: List[bool]
    o_safe_options: List[bool]
    o_conv_options: List[bool]



class ProductCreate(ProductBase):
    pass

class ProductResponse(ProductBase):
    id: str

    class Config:
        orm_mode = True




class User(BaseModel):
    id: str
    name: str
    email: EmailStr
    password: str
    phone: str
    address: str
    postcode: str
    birth: str

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str
    phone: str
    address: str
    postcode: str
    birth: str

class UserResponse(BaseModel):
    id: str
    name: str
    email: EmailStr
    phone: str
    address: str
    postcode: str
    birth: str

    class Config:
        orm_mode = True


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class InterestProduct(BaseModel):
    product_id: str
    user_id: Optional[str] = Field(None, description="User ID of the product interest")


class UserInterestProduct(BaseModel):
    id: str
    product_id: str
    user_id: str