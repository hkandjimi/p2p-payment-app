
from fastapi import FastAPI
from app.api.payment import router

from fastapi import FastAPI, Request, status, HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="P2P Payment API")

origins = [
    "http://localhost:8000","http://localhost:4200",  # Allow CORS from local machine/development environment
    "http://127.0.0.1:8000","http://127.0.0.1:4200",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["Authorization", "Content-Type", "Accept"],
    max_age=3600,  # Cache preflight response for 1 hour (3600 seconds)
)


app.include_router(router, prefix="/api")

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """
    Handles RequestValidationError and returns a custom JSON response.
    """
    code = ""
    errors = {
                "status": "FAILED",
                "errorCode": "",
                "transactionId": None,
                "message": ""
            }
    for index,error in enumerate(exc.errors()):
        # Specifically identify missing fields
        if error['type'] == 'missing':
            code=400
            errors["errorCode"] = "ERR001"
            errors["message"]+="Missing required field(s) : "+error['loc'][-1] if "Missing" not in errors["message"] else f", {error['loc'][-1]}"
        else:
        # custome data validation responses
            code=status.HTTP_422_UNPROCESSABLE_ENTITY
            errors["errorCode"] = "ERR008"
            errors["message"]+=("Data validation failed, "+str("(Error "+str(index+1)+") Invalid "+error['loc'][-1]+","+error['msg'])+"; ")
    
    # Return a custom JSON response with status code
    return JSONResponse(
        status_code=code,
        content=jsonable_encoder(errors),
    )