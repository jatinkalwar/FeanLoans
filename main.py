from datetime import datetime, timedelta
import random

from fastapi import Form, UploadFile, File
from motor.motor_asyncio import AsyncIOMotorClient
from starlette.responses import JSONResponse

from codes.Models import app, OTPRequest, otp_coll, OTPVerify, users, UserDetails
from codes.extra import generate_15_digit_alpha_token
from codes.upload import uploadfile


async def send_otp(number: str, otp: str):

    print(f"Sending OTP {otp} to {number}")

#####SEND OTP
@app.post("/send-otp/")
async def send_otp_endpoint(request: OTPRequest):
    try:
        number = request.number
        now = datetime.now()

        # Check if the number has exceeded the limit
        existing_entry =  otp_coll.find_one({"number": number})

        if existing_entry:
            request_count = existing_entry.get('count', 0)
            last_request_time = existing_entry['last_request_time']

            if now - last_request_time < timedelta(days=3) and request_count >= 3:
                raise JSONResponse(status_code=200,content={"success": False , "message": "Too many Otp Sent" })

            # Reset the count if more than an hour has passed
            if now - last_request_time >= timedelta(days=3):
                 otp_coll.update_one(
                    {"number": number},
                    {"$set": {"count": 1, "last_request_time": now}}
                )
            else:
                 otp_coll.update_one(
                    {"number": number},
                    {"$inc": {"count": 1}}
                )
        else:
             otp_coll.insert_one({
                "number": number,
                "count": 1,
                "last_request_time": now
            })

        # Generate OTP and send it
        otp = "000000"
        await send_otp(number, otp)
        print(otp)
        # Store the OTP and its expiration
        otp_coll.update_one(
            {"number": number},
            {"$set": {
                "otp": otp,
                "expires_at": now + timedelta(hours=58)
            }}
        )

        return JSONResponse(status_code=200 , content={"success": True , "message": "OTP sent Successfully"})
    except Exception as e:
        print(e)
        return JSONResponse(status_code=200, content={"success": False, "message": "Something went wrong"})


###VERIFY OTP

@app.post("/verify-otp/")
async def verify_otp(request: OTPVerify):
    number = request.number
    otp = request.otp
    now = datetime.now()

    existing_entry =  otp_coll.find_one({"number": number})

    if not existing_entry:
        return JSONResponse(status_code=200, content={"success": False, "message": "OTP not requested or expired."})


    stored_otp = existing_entry.get('otp')
    expires_at = existing_entry.get('expires_at')

    if now > expires_at:
        otp_coll.delete_one({"number": number})  # Remove expired OTP
        return JSONResponse(status_code=200, content={"success": False, "message": "OTP has expired."})


    if otp != stored_otp:
        return JSONResponse(status_code=200, content={"success": False, "message": "Invalid OTP."})


    otp_coll.delete_one({"number": number})  # Remove OTP after successful verification
    finddata = users.find_one({"mobile": number},
                                    {'name': 1,'_id': 0 , 'token':1})
    if finddata:
        return JSONResponse(status_code=200,
                            content={"success": True, "message": "OTP verified successfully.", "isfirst": False , "token": finddata["token"]})
    else:
        token = generate_15_digit_alpha_token()
        ih = users.find_one({"token": token},
                       {'name': 1, '_id': 0, 'token': 1})
        if ih:
            return JSONResponse(status_code=200, content={"success": False, "message": "Invalid OTP."})
        else:
            users.insert_one(
                {"mobile": number, "name": "", "dob": "",
                 "token": token, "active": True, "aadhar": "", "email": "", "profile": "", "extra": ""})

            return JSONResponse(status_code=200, content={"success": True, "message": "OTP verified successfully." , "isfirst": True , "token": token})


@app.post("/user-info/")
async def upload_image(rs: UserDetails):
    name = rs.name
    file = rs.profile
    dob = rs.dob
    email = rs.dob
    token = rs.token
  # Read the uploaded image file content

    # You can save the file or process it here (this is an example of saving it)
    # with open(f"uploaded_{file_content}", "wb") as f:
    #     f.write(file_content)
    res =  uploadfile(file)
    if res != "fail":
        users.update_one({"token": token}, {"$set": {"name": name, "dob": dob , "email":email , "profile": res }})
        return JSONResponse(status_code=200, content={"success": True, "message": "Profile Saved successfully." , "name":name , "dob": dob ,"email": email , "profile": res})
    else:
        return JSONResponse(status_code=200,
                            content={"success": False, "message": "Profile Saved successfully."})



