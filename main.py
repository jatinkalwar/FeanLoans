from datetime import datetime, timedelta
import random

from fastapi import Form, UploadFile, File
from motor.motor_asyncio import AsyncIOMotorClient
from starlette.responses import JSONResponse

from codes.Gateway import createorder, getstatus
from codes.Models import app, OTPRequest, otp_coll, OTPVerify, users, UserDetails, UserUpdate, UserLoan, forms, amount, \
    CreateOrder, GetStatus, GetApplication
from codes.extra import generate_15_digit_alpha_token, application_token_gen, get_time
from codes.upload import uploadfile
from datas import getapplicationslist, getagreementlist


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
                                    {'name': 1,'_id': 0 , 'token':1 , "email": 1 , "dob": 1 , "profile": 1  , "aadhar": 1})
    if finddata:
        return JSONResponse(status_code=200,
                            content={"success": True, "message": "OTP verified successfully.", "isfirst": False , "token": finddata["token"] , "email": finddata["email"]  , "name": finddata["name"] , "dob":finddata["dob"] , "profile": finddata["profile"] , "aadhar": finddata["aadhar"] , "create_date": get_time()})
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
    email = rs.email
    token = rs.token
    adhar = rs.adhar
  # Read the uploaded image file content

    # You can save the file or process it here (this is an example of saving it)
    # with open(f"uploaded_{file_content}", "wb") as f:
    #     f.write(file_content)
    res =  uploadfile(file)
    if res != "fail":
        users.update_one({"token": token}, {"$set": {"name": name, "dob": dob , "email":email , "profile": res }})
        return JSONResponse(status_code=200, content={"success": True, "message": "Profile Saved successfully." , "name":name , "dob": dob ,"email": email , "profile": res , "aadhar": adhar})
    else:
        return JSONResponse(status_code=200,
                            content={"success": False, "message": "Something Went Wrong"})



@app.post("/user-update/")
async def upload_image(rs: UserUpdate):
    name = rs.name
    file = rs.profile
    dob = rs.dob
    email = rs.email
    token = rs.token
    adhar = rs.adhar
  # Read the uploaded image file content

    # You can save the file or process it here (this is an example of saving it)
    # with open(f"uploaded_{file_content}", "wb") as f:
    #     f.write(file_content)
    if file is None:
        users.update_one({"token": token}, {"$set": {"name": name, "dob": dob, "email": email}})
        finddata = users.find_one({"token": token},
                                  {'name': 1, '_id': 0, 'token': 1, "email": 1, "dob": 1, "profile": 1, "aadhar": 1})
        return JSONResponse(status_code=200,
                            content={"success": True, "message": "Profile Saved successfully.", "name": name,
                                     "dob": dob, "email": email, "profile": finddata["profile"], "aadhar": adhar})
    res =  uploadfile(file)
    if res != "fail":
        users.update_one({"token": token}, {"$set": {"name": name, "dob": dob , "email":email , "profile": res }})
        return JSONResponse(status_code=200, content={"success": True, "message": "Profile Saved successfully." , "name":name , "dob": dob ,"email": email , "profile": res , "aadhar": adhar})
    else:
        return JSONResponse(status_code=200,
                            content={"success": False, "message": "Something Went Wrong"})

@app.post("/user-loan/")
async def upload_image(rs: UserLoan):
    try:
        aadhar_url = uploadfile(rs.adhar_img)
        pan_url = uploadfile(rs.pan_img)
        # aadhar_url = ""
        # pan_url = "uploadfile(rs.pan_img)"
        finddata = users.find_one({"token": rs.token},
                                  {'mobile': 1, '_id': 0,})

        application_id = application_token_gen()
        forms.insert_one({
            "token": rs.token,
            "mobile": finddata['mobile'],
            "name": rs.name,
            "dob": rs.dob,
            "aadhar": rs.aadhar,
            "company": rs.company_name,
            "employment_type": rs.employment_type,
            "salary": rs.monthly_salary,
            "loan_amount": rs.loan_amount,
            "tenure": rs.tenure,
            "official_email": rs.official_email,
            "designation": rs.designation,
            "company_category": rs.company_category,
            "experience": rs.experience,
            "office_label": rs.office_label,
            "office_address": rs.office_address,
            "office_pincode": rs.office_pincode,
            "office_city": rs.office_city,
            "office_district": rs.office_district,
            "office_state": rs.office_state,
            "alternate_number": rs.alternate_number,
            "gender": rs.gender,
            "marital_status": rs.marital_status,
            "mothers_name": rs.mother_name,
            "father_name": rs.father_name,
            "current_label": rs.current_label,
            "current_address": rs.current_address,
            "current_pincode": rs.current_pincode,
            "current_city": rs.current_city,
            "current_district": rs.current_district,
            "current_state": rs.current_state,
            "aadhar_img": aadhar_url,
            "pan_img": pan_url,
            "first_name": rs.first_name,
            "first_number": rs.first_number,
            "first_label": rs.first_label,
            "first_address": rs.first_address,
            "first_pincode": rs.first_pincode,
            "first_city": rs.first_city,
            "first_district": rs.first_district,
            "first_state": rs.first_state,
            "second_name": rs.second_name,
            "second_number": rs.second_number,
            "second_label": rs.second_label,
            "second_address": rs.second_address,
            "second_pincode": rs.second_pincode,
            "second_city": rs.second_city,
            "second_district": rs.second_district,
            "second_state": rs.second_state,
            "application_no": application_id ,
            "status": False,
            "amount_paid": False,
            "agreement_amount": False,
            "insurance_amount": False,
            "fill_on": get_time()
        })
        finddata = amount.find_one({"payment": "formcharge"},
                                   {'loan1_5': 1, '_id': 0, 'loan6_15': 1, 'loan16_25': 1, 'loan26_50': 1,
                                    'loan51_100': 1})

        global amounts
        if int(rs.loan_amount) < 500000:
                amounts = finddata['loan1_5']
        elif int(rs.loan_amount) < 1500000:
                amounts = finddata['loan6_15']
        elif int(rs.loan_amount) < 2500000:
                amounts = finddata['loan16_25']
        elif int(rs.loan_amount) < 5000000:
                amounts = finddata['loan26_50']
        elif int(rs.loan_amount) < 10000000:
                amounts = finddata['loan51_100']
        return JSONResponse(status_code=200,
                            content={"success": True, "message": "Data Saved" , "id": application_id , "amount": amounts})




    except Exception as e:
        print(e)
        return JSONResponse(status_code=200,
                            content={"success": False, "message": "Something Went Wrong"})

@app.post("/create-order/")
async def create_order(rs: CreateOrder):
    try:
        return await createorder(rs.application , rs.token , rs.type)
    except Exception as e:
        print(e)
        return JSONResponse(status_code=200,
                            content={"success": False, "message": "Something Went Wrong"})


@app.post("/get-status/")
async def get_status(rs: GetStatus):
    try:
        return await getstatus(rs.transaction)
    except Exception as e:
        print(e)
        return JSONResponse(status_code=200,
                            content={"success": False, "message": "Something Went Wrong"})


@app.post("/get-application/")
async def get_application(rs: GetApplication):
    try:
        return await getapplicationslist(rs.token)
    except Exception as e:
        print(e)
        return JSONResponse(status_code=200,
                            content={"success": False, "message": "Something Went Wrong"})

@app.post("/get-agreement/")
async def get_agreement(rs: GetApplication):
    try:
        return await getagreementlist(rs.token)
    except Exception as e:
        print(e)
        return JSONResponse(status_code=200,
                            content={"success": False, "message": "Something Went Wrong"})






