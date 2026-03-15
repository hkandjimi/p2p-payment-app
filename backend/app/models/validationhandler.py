
from fastapi import HTTPException

ERROR_CODES = {
    "ERR001": {
        "http_status": 400,
        "description": "Missing required field"
    },
    "ERR002": {
        "http_status": 400,
        "description": "Invalid account number format"
    },
    "ERR003": {
        "http_status": 400,
        "description": "Invalid currency"
    },
    "ERR004": {
        "http_status": 400,
        "description": "Invalid amount"
    },
    "ERR005": {
        "http_status": 402,
        "description": "Insufficient funds"
    },
    "ERR006": {
        "http_status": 500,
        "description": "Internal processing error"
    }
}

def raise_api_error(error_code,info=""):

    error = ERROR_CODES[error_code]

    raise HTTPException(
        status_code=error["http_status"],
        detail={
            "status": "FAILED",
            "errorCode": error_code,
            "transactionId": None,
            "message": error["description"]+":"+info if len(info)>0 else error["description"]
        }
    )