'''
Docstring for TEST_v1.0.dock.endpoints

Serves all the endpoints for the backend
'''

from Utility.logger import loggy
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from uuid import uuid4, UUID
from Utility.pydantic_models.protocol_schema import Payload_validator
from Dock.resolver import call_flags
from pydantic import BaseModel


def log(log: str) -> None:
    loggy("dock/endpoints", log)

deferred = FastAPI()



# ----------------------------- CORS Middleware --------------------------- #

deferred.add_middleware(
    CORSMiddleware,
    allow_origins = ["*"],
    allow_methods = ["*"],
    allow_headers=["*"]
)

# ----------------------------- end CORS Middleware --------------------------- #



# take a single-slot dict, so we don't havae to play with global keyword later
TASKS: dict[str, UUID] = {}

def add_task(uid: UUID):
    if len(TASKS) == 0:
        # only one hard-coded key would always remain
        TASKS["uid"] = uid
    else:
        # not empty? Clear.
        TASKS.clear()

# make endpoints now. First, take basic request in:
@deferred.get("/tasks")
def create_id():
    uid = uuid4()
    add_task(uid)
    return {"id": uid}

@deferred.post("/tasks/{uid}")
def docking(uid: UUID, payload: Payload_validator):
    # let's quickly check if the id is correct.
    if TASKS.get("uid") != uid:
        raise HTTPException(status_code=400, detail="Deferred: WRONG UUID sent by the client")

    # unwrap validated value objects
    cat = payload.cat.value
    flag = payload.flag.value
    version = payload.version.value 
    # now we play serious. payload is here.
    log(
        f"Received payload with type: {cat}, "
        f"flag: {flag}, "
        f"version: {version}"
    )

    # if cat is init, we call CREATE flag and create a new operation
    # We also make sure there is no op_id in the payload for init category

    InstructionStateModel: type[BaseModel]

    if cat == "init":
        if payload.content.op_id:
            raise HTTPException(status_code=400, detail="Deferred: op_id must be False for init category")

        # this triggers a chain of calls that results in instructions being returned.
        inst_collection = call_flags(flag, payload.cat)
        log(
            "Caught instructions. Dispatching them to frontend"
        )
        InstructionStateModel = inst_collection["insturction_type"]
        return inst_collection["instructions"]
    
    if cat == "hydrate":
        if not payload.content.op_id:
            raise HTTPException(status_code=400, detail="Deferred: op_id must be provided for hydrate category")
        
        if payload.content.prompt and payload.content.deliver_at and payload.content.op_id:
            
            # this triggers a chain of calls that results in instructions being returned.

        # now, we validate the payload content
        InstructionStateModel(payload.content.model_dump())