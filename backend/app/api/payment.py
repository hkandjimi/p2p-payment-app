
# from fastapi import APIRouter, HTTPException
# import requests
# from app.models.schemas import PaymentRequest
# from pydantic import ValidationError

# router = APIRouter()

# WIREMOCK_URL = "http://wiremock:8080/api/p2p-payment"

# @router.post("/payment")
# def process_payment(request: PaymentRequest): 
#     print(request);
#     if request.amount <= 0:
#         raise HTTPException(status_code=400, 
#                             detail="Invalid account number format ",
#                             headers={"status": "FAILED","ErrorCode": "ERR002", "transactionId": None, "message":"Invalid account number format" })
#     if request.currency != "NAD":
#         raise HTTPException(status_code=400, 
#                             detail="Invalid currency",
#                             headers={"status": "FAILED","ErrorCode": "ERR003", "transactionId": None, "message":"Invalid currency" })
#     if request.amount <= 0:
#         raise HTTPException(status_code=400, 
#                             detail="Invalid amount",
#                             headers={"status": "FAILED","ErrorCode": "ERR004", "transactionId": None, "message":"Missing required field" })
        
#     try:
#         request = PaymentRequest.model_validate_json(request)
#         response = requests.post(WIREMOCK_URL, json=request.dict())
#         return response.json()
#     except ValueError as e:
#         raise HTTPException(status_code=400, 
#                             detail=e.__str__,
#                             headers={"status": "FAILED","ErrorCode": "ERR001", "transactionId": None, "message":"Missing required field" })
#     except ValidationError:
#         raise HTTPException(status_code=400, 
#                             headers={"status": "FAILED","errorCode": "ERR001", "transactionId": None, "message":"Missing required field" })
#     except:
#         raise HTTPException(status_code=500, 
#                             detail="Internal processing error ",
#                             headers={"status": "FAILED","ErrorCode": "ERR006","transactionId": None, "message":"Internal processing error "})

from fastapi import APIRouter, HTTPException
from app.models.schemas import PaymentRequest
from datetime import datetime
import time

from pydantic import BaseModel, ValidationError


from app.services.redis_service import (
    account_exists,
    update_balance,
    get_account_details,
    get_balance,
)

router = APIRouter()

@router.get("/p2p-payment/{account_number}")
def account_details(account_number):
    return get_account_details(account_number)

@router.post("/p2p-payment")
def process_payment(request:PaymentRequest):
    print(request)
    sender_valid = account_exists(request.senderAccountNumber)
    receiver_valid = account_exists(request.receiverAccountNumber)

    if not sender_valid or not receiver_valid:

        if not sender_valid and not receiver_valid:
            message = "Invalid sender and receiver account numbers provided"

        elif not sender_valid:
            message = "Invalid sender account number provided"

        else:
            message = "Invalid receiver account number provided"

        raise HTTPException(
            status_code=500,
            detail={
                "status": "FAILED",
                "errorCode": "ERR007",
                "transactionId": None,
                "message": message
            }
        )
    # Simulated payment processing
    if account_exists(request.receiverAccountNumber) and account_exists(request.senderAccountNumber):
        sender_balance = get_balance(request.senderAccountNumber)
        receiver_balance = get_balance(request.receiverAccountNumber)
        
        transaction = {}
        if sender_balance >= request.amount:
            update_balance(request.senderAccountNumber, sender_balance - request.amount)
            update_balance(request.receiverAccountNumber, receiver_balance + request.amount)
            transaction = {
                "status": "SUCCESS",
                "errorCode": None,
                "transactionId": f"TXN{request.clientReference.replace('-','').replace('REF','')}",
                "message": f"Payment processed successfully. Your new balance N$ {get_balance(request.senderAccountNumber):.2f} "
            }
        else:
            raise HTTPException(
            status_code=402,
            detail={
                "status": "FAILED",
                "errorCode": "ERR005",
                "transactionId": None,
                "message": f"Insufficient funds, Current balance N$ {sender_balance:.2f}"
            }
        )
        # save_account(request.clientReference, transaction)
        return transaction
    
