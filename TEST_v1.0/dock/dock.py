import json
from pathlib import Path
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from uuid import uuid4
from state import TASKS, clear_tasks


ENUM_PATH = Path(__file__).parent / "enums.json"

with open(ENUM_PATH, "r", encoding="utf-8") as f:
    OPERATIONS = json.load(f)

deferred = FastAPI()
deferred.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@deferred.get("/tasks")
def return_uuid(payload: dict | None = None) -> dict:
    uuid_string = str(uuid4())
    clear_tasks()
    TASKS[uuid_string] = payload
    return {"id": uuid_string}

@deferred.post("/tasks/{id}")
def process(payload: dict) -> dict:
    if id not in TASKS.keys():
        raise HTTPException('404', "Wrong id")
        
