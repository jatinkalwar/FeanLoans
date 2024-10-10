from fastapi import FastAPI , Request

from pydantic import BaseModel
from pymongo import MongoClient
from typing import Optional

from starlette.middleware.cors import CORSMiddleware


app = FastAPI(docs_url=None, redoc_url=None, openapi_url=None, title="AntiToolz")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins. Change this to specific origins for more security.
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allows all headers
)
client = MongoClient("mongodb+srv://jatinkalwar:shifaanam@mbomb.ghtntua.mongodb.net")
users = client.msdigital.users
otp_coll = client.msdigital.otp
forms = client.msdigital.forms
amount = client.msdigital.payment
transactiondb = client.msdigital.transaction



#####MODELS API

class OTPRequest(BaseModel):
    number: str


class OTPVerify(BaseModel):
    number: str
    otp: str

class UserDetails(BaseModel):
    token: str
    name: str
    dob: str
    email: str
    profile: str
    adhar:str

class UserUpdate(BaseModel):
    token: str
    name: str
    dob: str
    email: str
    profile: Optional[str] = None
    adhar:str

class UserLoan(BaseModel):
    token: str
    loan_type: str
    name: str
    dob: str
    aadhar: str
    company_name: str
    employment_type: str
    monthly_salary: str
    loan_amount: str
    tenure: str
    official_email: str
    designation: str
    company_category: str
    experience: str
    office_label: str
    office_address: str
    office_pincode: str
    office_city: str
    office_district: str
    office_state: str
    alternate_number: str
    gender: str
    marital_status: str
    mother_name: str
    father_name: str
    current_label: str
    current_address: str
    current_pincode: str
    current_city: str
    current_district: str
    current_state: str
    adhar_img: str
    pan_img: str
    first_name: str
    first_number: str
    first_label: str
    first_address: str
    first_pincode: str
    first_city: str
    first_district: str
    first_state: str

    second_name: str
    second_number: str
    second_label: str
    second_address : str
    second_pincode: str
    second_city: str
    second_district: str
    second_state: str

class CreateOrder(BaseModel):
    application: str
    token: str
    type: str

class GetStatus(BaseModel):
    transaction: str
