
from pydantic import BaseModel, Field, model_validator,field_validator
import re
from app.models.validationhandler import raise_api_error

class PaymentRequest(BaseModel):

    clientReference: str
    senderAccountNumber: str
    receiverAccountNumber: str
    amount: float
    currency: str
    reference: str

    @field_validator("senderAccountNumber")
    @classmethod
    def validate_account_number(cls, v):

        if not re.fullmatch(r"\d+", v) or len(str(v))<10:
            raise_api_error("ERR002",info=f"{v} (Sender Account)")

        return v

    @field_validator("receiverAccountNumber")
    @classmethod
    def validate_raccount_number(cls, v):

        if not re.fullmatch(r"\d+", v) or len(str(v))<10:
            raise_api_error("ERR002",info=f"{v} (Receiver Account)")

        return v

    @field_validator("currency")
    @classmethod
    def validate_currency(cls, v):

        if v != "NAD":
            raise_api_error("ERR003")

        return v


    @field_validator("amount")
    @classmethod
    def validate_amount(cls, v):

        if v <= 0:
            raise_api_error("ERR004")

        return v

    @field_validator("reference")
    @classmethod
    def validate_reference(cls, v):

        if len(str(v))>50:
            raise_api_error("ERR006",info=" Reference too long(max 50 characters)")

        return v


class PaymentResponse(BaseModel):

    status: str
    errorCode: str | None
    transactionId: str | None
    message: str
