from pydantic import BaseModel, Field, EmailStr
from datetime import date
from decimal import Decimal
from typing import List

class DrivingLicense(BaseModel):
    name : str
    dob : date
    license_number : str
    issuing_state : str
    expiry_date : date

class items(BaseModel):
    name : str
    quantity : int = Field(ge=1)
    price : Decimal

class shop_receipt(BaseModel):
    merchant_name : str
    total_amount : Decimal
    date_of_purchase : date
    items : List[items]
    payment_method : str

class work_experience(BaseModel):
    company_name : str
    role : str
    start_date : date
    end_date : date
    
class education(BaseModel):
    institution_name : str
    degree : str
    graduation_year : int

class resume(BaseModel):
    name : str
    email : EmailStr
    phone : str
    skills : List[str]
    education : List[education]
    experience : List[work_experience]

