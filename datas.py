from starlette.responses import JSONResponse

from codes.Models import forms, amount, users


async def getapplicationslist(token):
    try:
        # Convert cursor to a list of documents first
        documents = list(forms.find(
            {"token": token, "amount_paid": True , "status": False},
            {"status": 1, "fill_on": 1, "_id": 0 , 'application_no':1 , 'mobile':1 , 'name':1 , 'loan_amount':1 , "loan_type": 1}  # Projecting only 'status' and 'time', excluding '_id'
        ))

        # Remove the _id field from each document
        for doc in documents:
            if "_id" in doc:
                del doc["_id"]

        if not documents:
            return JSONResponse(status_code=200, content={
                "success": True,
                "avail": False,
                "message": "No Data Found",
                "data": []
            })

        return JSONResponse(status_code=200, content={
            "success": True,
            "message": "Data Found",
            "avail": True,
            "data": documents  # Return the modified documents
        })
    except Exception as e:
        print(e)
        return JSONResponse(status_code=200, content={
            "success": False,
            "message": "Something Went Wrong"
        })

async def getagreementlist(token):
    try:
        # Convert cursor to a list of documents first
        documents = list(forms.find(
            {"token": token, "amount_paid": True ,"status": True},
            {"fill_on": 1, "_id": 0 , 'application_no':1 , 'mobile':1 , 'name':1 , 'loan_amount':1 , 'agreement_amount':1 , "loan_type":1} ))

        # Remove the _id field from each document
        for doc in documents:
            if "_id" in doc:
                del doc["_id"]
        finddata = amount.find_one({"payment": "file"},
                                   {'agreement': 1, '_id': 0})
        if not documents:
            return JSONResponse(status_code=200, content={
                "success": True,
                "avail": False,
                "message": "No Data Found",
                "amount": finddata['agreement'],
                "data": []
            })

        return JSONResponse(status_code=200, content={
            "success": True,
            "message": "Data Found",
            "avail": True,
            "amount": finddata['agreement'],
            "data": documents  # Return the modified documents
        })
    except Exception as e:
        print(e)
        return JSONResponse(status_code=200, content={
            "success": False,
            "message": "Something Went Wrong"
        })


async def getinsurancelist(token):
    try:
        # Convert cursor to a list of documents first
        documents = list(forms.find(
            {"token": token, "amount_paid": True, "status": True},
            {"fill_on": 1, "_id": 0, 'application_no': 1, 'mobile': 1, 'name': 1, 'loan_amount': 1,
             'insurance_amount': 1, "loan_type": 1}))

        # Remove the _id field from each document
        for doc in documents:
            if "_id" in doc:
                del doc["_id"]
        finddata = amount.find_one({"payment": "file"},
                                   {'insurance': 1, '_id': 0})
        if not documents:
            return JSONResponse(status_code=200, content={
                "success": True,
                "avail": False,
                "message": "No Data Found",
                "amount": finddata['insurance'],
                "data": []
            })

        return JSONResponse(status_code=200, content={
            "success": True,
            "message": "Data Found",
            "avail": True,
            "amount": finddata['insurance'],
            "data": documents  # Return the modified documents
        })
    except Exception as e:
        print(e)
        return JSONResponse(status_code=200, content={
            "success": False,
            "message": "Something Went Wrong"
        })

async def senduserdetail():
    try:
        documents = list(users.find({},
            {"dob": 1, "_id": 0, 'application_no': 1, 'mobile': 1, 'name': 1, 'aadhar': 1,
             'email': 1, "profile": 1 , "create_date":1}))

        # Remove the _id field from each document
        # for doc in documents:
        #     if "_id" in doc:
        #         del doc["_id"]
        # finddata = amount.find_one({"payment": "file"},
        #                            {'insurance': 1, '_id': 0})
        if not documents:
            return JSONResponse(status_code=200, content={
                "success": True,
                "avail": False,
                "message": "No Data Found",

                "data": []
            })

        return JSONResponse(status_code=200, content={
            "success": True,
            "message": "Data Found",
            "avail": True,
            "data": documents  # Return the modified documents
        })
    except Exception as e:
        print(e)
        return JSONResponse(status_code=200, content={
            "success": False,
            "message": "Something Went Wrong"
        })

async def putupdate(type , status , token):
    try:
        if type=="1":
            forms.update_one({"application_no": token},
                                     {"$set": {"status": status,}})
            return JSONResponse(status_code=200, content={
                "success": True,
                "message": "Update SuccessFully"
            })
        elif type=="2":
            forms.update_one({"token": token},
                                     {"$set": {"agreement_amount": status,}})
            return JSONResponse(status_code=200, content={
                "success": True,
                "message": "Update SuccessFully"
            })
        elif type=="3":
            forms.update_one({"token": token},
                                     {"$set": {"insurance_amount": status,}})
            return JSONResponse(status_code=200, content={
                "success": True,
                "message": "Update SuccessFully"
            })
    except Exception as e:
        print(e)
        return JSONResponse(status_code=200, content={
            "success": False,
            "message": "Something Went Wrong"
        })

async def sendformsdetails():
    try:
        documents = list(forms.find({},{
            "token": 1,
            "mobile": 1,
            "name": 1,
            "dob": 1,
            "aadhar":1,
            "loan_type": 1,
            "company": 1,
            "employment_type": 1,
            "salary": 1,
            "loan_amount": 1,
            "tenure": 1,
            "official_email": 1,
            "designation":1,
            "company_category": 1,
            "experience":1,
            "office_label": 1,
            "office_address": 1,
            "office_pincode": 1,
            "office_city": 1,
            "office_district": 1,
            "office_state": 1,
            "alternate_number": 1,
            "gender": 1,
            "marital_status": 1,
            "mothers_name": 1,
            "father_name": 1,
            "current_label": 1,
            "current_address": 1,
            "current_pincode":1,
            "current_city": 1,
            "current_district": 1,
            "current_state": 1,
            "aadhar_img": 1,
            "pan_img": 1,
            "first_name": 1,
            "first_number": 1,
            "first_label": 1,
            "first_address": 1,
            "first_pincode": 1,
            "first_city": 1,
            "first_district": 1,
            "first_state": 1,
            "second_name":1,
            "second_number": 1,
            "second_label": 1,
            "second_address": 1,
            "second_pincode": 1,
            "second_city": 1,
            "second_district": 1,
            "second_state": 1,
            "application_no": 1,
            "status": 1,
            "amount_paid": 1,
            "agreement_amount": 1,
            "insurance_amount": 1,
            "fill_on": 1,
            "_id": 0
        }))
        if not documents:
            return JSONResponse(status_code=200, content={
                "success": True,
                "avail": False,
                "message": "No Data Found",

                "data": []
            })

        return JSONResponse(status_code=200, content={
            "success": True,
            "message": "Data Found",
            "avail": True,
            "data": documents  # Return the modified documents
        })
    except Exception as e:
        print(e)
        return JSONResponse(status_code=200, content={
            "success": False,
            "message": "Something Went Wrong"
        })

