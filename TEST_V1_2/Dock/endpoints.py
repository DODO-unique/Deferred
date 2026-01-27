'''
Docstring for TEST_v1.0.dock.endpoints

Serves all the endpoints for the backend
'''

from Utility.logger import loggy
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from uuid import uuid4, UUID
from Utility.pydantic_models import initPayload
from Dock.enums import call_flags


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
def docking(uid: UUID, payload: initPayload):
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

    

    if cat == "init":
        instructions = call_flags(flag, cat)
        log(
            "Caught instructions. Dispatching them to frontend"
        )
        return instructions