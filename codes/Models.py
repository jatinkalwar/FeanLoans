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
# mongodb+srv://jatinkalwar:shifaanam@mbomb.ghtntua.mongodb.net
client = MongoClient("mongodb+srv://feanloans:msloans@feanloans.tw0rt.mongodb.net/?retryWrites=true&w=majority&appName=feanloans")

users = client.feans.users
otp_coll = client.feans.otp
forms = client.feans.forms
amount = client.feans.payment
transactiondb = client.feans.transaction



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

class UploadImage(BaseModel):
    image: str
    type: str
    token: str

class PutUpdate(BaseModel):
    token: str
    status: bool
    type: str

class PutAmount(BaseModel):
    agreement: str
    insurance: str
    loan1: str
    loan2: str
    loan3: str
    loan4: str
    loan5: str


class GetStatus(BaseModel):
    transaction: str

class GetApplication(BaseModel):
    token: str
