'''
Docstring for Endpoints.py
codes land here
'''

# ----------------------------- External Imports --------------------------- #
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
# we would try to avoid JSONResponse as much as possible.
from fastapi.responses import JSONResponse
from uuid import uuid4, UUID

# ----------------------------- Internal Imports --------------------------- #
from Utility.logger import loggy
from Utility.pypolice.payload_validator import Payload_validator
from Medium.Dispatcher.op_dis import opdis_path_one, opdis_path_two
from Utility.ErrorHandler import ErrorHandler, initiate_error_handler, ErrorCodes


# ----------------------------- setup --------------------------- #
def log(log: str) -> None:
    loggy("Dock/Endpoints", log)
deferred = FastAPI()



# ----------------------------- CORS Middleware --------------------------- #

deferred.add_middleware(
    CORSMiddleware,
    allow_origins = ["*"],
    allow_methods = ["*"],
    allow_headers=["*"]
)

# ----------------------------- end CORS Middleware --------------------------- #

uid_record: set[UUID] = set()

@deferred.get("/tasks")
def create_id():
    uid = uuid4()
    uid_record.add(uid)
    return {"id": uid} # FastAPI handles UUID serialisation. We would have used JSONResponse otherwise.

@deferred.post("/tasks/{uid}")
def perform(uid: UUID, payload: Payload_validator):
    if uid not in uid_record:
         initiate_error_handler(message="Unrecognized UID", errCode=ErrorCodes.UNRECOGNIZED_UNIQUE_ID.value, error=KeyError("UID not found in uid_record"))

    # this is interesting because we receive all kinds of payload here. The good news is we don't have to sort it. We simply validate and forward it.

    # we extract flag and cat (not their values yet)
    flag = payload.flag
    cat = payload.cat
    package = payload.packed_at
    version = payload.version
    log(f"Received a request with flag: {flag}, cat: {cat}, package time: {package}, version: {version}")

    # if category is init, we create a new op_id
    if cat.value == "init":
            log("Category init detected. Passing control payload to OPDIS")
            operation_id = opdis_path_one(payload)
            log(f"Received operation_id {operation_id} from OPDIS, returning to frontend")
            return operation_id

    # check if op_id, deliver_at and prompt are present in the content, and if they are, we extract them as well.
    elif payload.content.op_id:
        # these are for create flag only:
        if  payload.content.deliver_at and payload.content.prompt:    
            op_id = payload.content.op_id
            deliver_at = payload.content.deliver_at
            prompt = payload.content.prompt
            log(f"Content has op_id: {op_id}, deliver_at: {deliver_at}, prompt: {prompt}; a CREATE flag.")

            # path two is for all flags except init
            log("Sending payload to PATH TWO")
            creation_status = opdis_path_two(payload)
            return creation_status

     
    else:
        initiate_error_handler(message="Invalid payload content", errCode=ErrorCodes.INVALID_PAYLOAD_CONTENT.value, error=ValueError("Missing required fileds in content"))
        # initiate_error_handler(status_code=400, message="Invalid payload content for non-init category", errCode=ErrorCodes.INVALID_PAYLOAD_CONTENT.value, error=ValueError("Missing required fields in content for non-init category"))
        

@deferred.exception_handler(ErrorHandler)
def Seraphina(request: Request, exc: ErrorHandler):
    return JSONResponse(
        status_code= exc.status_code,
        content= {
             "Error Code": exc.errCode,
             "Error Message": exc.message,
        }
    )