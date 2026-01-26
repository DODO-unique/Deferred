'''
Docstring for TEST_v1.0.dock.pydantic_model

all pydantic data typing here.
'''

from pydantic import BaseModel, field_validator
from typing import Optional
from uuid import UUID

class Category(BaseModel):
    cat: str

    @field_validator('cat')
    @classmethod
    def check_category(cls, v):
        all_cats = {'init'}
        if v not in all_cats:
            raise ValueError(f"No such category {v}")
        return v
    @property
    def value(self):
        return self.cat

class Flag(BaseModel):
    flag: str

    @field_validator('flag')
    @classmethod
    def check_caps(cls, v):
        if not v.isupper():
            raise ValueError("Flag must be all capital")
        return v
    @property
    def value(self):
        return self.flag
    
class Versions(BaseModel):
    version: str

    @field_validator('version')
    @classmethod
    def check_version(cls, v):
        all_versions = {'Tv_1.0'}
        if v not in all_versions:
            raise ValueError(f"No such version {v}")
        return v
    @property
    def value(self):
        return self.version
class Payload_content(BaseModel):
    body: Optional[dict[str, str]] = None
    # any other fields can be added later

class initPayload(BaseModel):
    flag: Flag
    cat: Category
    content: Payload_content
    version: Versions




# ----------------------- This is for the Engine/ -------------------
class createInitiation(BaseModel):
    op_id : Optional[UUID] = None
    next_state : str
    completed_steps : dict[str, str]
    version : Versions

    
