from starlette.responses import JSONResponse

from codes.Models import forms


async def getapplicationslist(token):
    try:
        # Convert cursor to a list of documents first
        documents = list(forms.find(
            {"token": token, "amount_paid": True},
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



