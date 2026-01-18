'''
Docstring for TEST_v1.0.dock.endpoints

Serves all the endpoints for the backend
'''

from ..Engine.control import loggy
from fastapi import FastAPI, HTTPException
from uuid import uuid4, UUID
from pydantic_models import initPayload
from enums import call_flags

def log(log: str) -> None:
    loggy("dock/endpoints", log)

deferred = FastAPI()

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
    return uid

@deferred.post("/tasks/{uid}")
def docking(uid: UUID, payload: initPayload):
    # let's quickly check if the id is correct.
    if TASKS.get('uid') != uid:
        raise HTTPException(status_code=400, detail="WRONG UUID")

    # now we play serious. payload is here.
    log(f"Received payload with type: {payload.cat}, flag: {payload.flag}, version: {payload.version}")
    if payload.cat == 'init':
        instructions = call_flags(payload.flag, payload.cat)
        return instructions

