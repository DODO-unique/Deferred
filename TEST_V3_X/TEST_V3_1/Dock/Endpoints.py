'''
Docstring for Dock/Endpoints.py
'''

# -------------------------- External Imports --------------------------- #
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse


# --------------------------- Internal Imports --------------------------- #
from Utility.logger import loggy
from Utility.ErrorHandler import ErrorHandler
from Utility.pypolice.payload_validator import RegisterPayloadValidator
from Auth.auth_moderator import registration

def log(msg: str) -> None:
    loggy("Dock/Endpoints", msg)

deferred = FastAPI()


# ----------------------------- CORS Middleware --------------------------- #

deferred.add_middleware(
    CORSMiddleware,
    allow_origins = ["*"],
    allow_methods = ["*"],
    allow_headers=["*"]
)


deferred.get("/home")
def home():
    return {"message": "YOU ARE CONNECTED"}

@deferred.post("/auth/register")
async def registry(payload: RegisterPayloadValidator):
    uname = payload.user
    mail = payload.mail
    pt_password = payload.pt_password
    log(f"pt_password: {pt_password}")
    log(f"pt_password: {pt_password.value}")
    
    registeration_status = await registration.registration_data(uname, mail, pt_password)
    return registeration_status

@deferred.exception_handler(ErrorHandler)
def Seraphina(request: Request, exc: ErrorHandler):
    return JSONResponse(
        status_code= exc.status_code,
        content= {
             "Error Code": exc.errCode,
             "Error Message": exc.message,
        }
    )