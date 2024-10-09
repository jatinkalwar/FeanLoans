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
