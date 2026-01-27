from datetime import datetime
from typing import Optional, Annotated
from pydantic import BaseModel, create_model, field_validator, Field, BeforeValidator
from uuid import UUID


# ----------------------------------------- payload models ----------------------------------------- #

ISODateTime = Annotated[
            datetime,
            BeforeValidator(datetime.fromisoformat)
            ]


class Category(BaseModel):
    value: str

    @field_validator('value')
    @classmethod
    def check_category(cls, v: str):
        all_cats = {'init', 'hydrate'}
        if v not in all_cats:
            raise ValueError(f"No such category {v}")
        return v

class Flag(BaseModel):
    value: str

    @field_validator('value')
    @classmethod
    def check_caps(cls, v: str):
        if not v.isupper():
            raise ValueError("Flag must be all capital")
        return v
    
class Versions(BaseModel):
    value: str

    @field_validator('value')
    @classmethod
    def check_version(cls, v: str):
        all_versions = {'Tv_1.0'}
        if v not in all_versions:
            raise ValueError(f"No such version {v}")
        return v
    
class Payload_content(BaseModel):
    body: Optional[dict[str, str | dict[any, any]]] = None # type: ignore
    # any other fields can be added later

class PackcageTime(BaseModel):
    value: ISODateTime
    

class Payload_validator(BaseModel):
    flag: Flag
    cat: Category
    content: Payload_content
    packed_at: PackcageTime
    version: Versions


# ------------------------------------------ End of payload models ----------------------------------------- #



# ----------------------------------------- instruction state models ----------------------------------------- #

'''
instructions = {
    "prompt" : True,
    "deliver_at" : True,
    "creation_time" : True,
    "op_id" : True,
    "version" : True
}
'''
class PromptValidator(BaseModel):
    value: str

class DeliveryValidator(BaseModel):
    value: str

class OpIdValidator(BaseModel):
    value: UUID

class VersionsValidator(BaseModel):
    value: str

    @field_validator('value')
    @classmethod
    def check_version(cls, v: str) -> str:
        all_versions = {'Tv_1.0'}
        if v not in all_versions:
            raise ValueError(f"No such version {v}")
        return v

def create_instruction_state(instructions: dict[str, bool]) -> type[BaseModel]:
    instruction_state_objects: dict[str, tuple[type[BaseModel], Field]] = {} #type: ignore
    for prop, value in instructions.items():
        if value:
            # resolve key to relevant data type pair
            field, validator = resolve_instructions(prop)
            instruction_state_objects[field] = (validator, Field(...))
    # Dynamically create Pydantic model
    InstructionStateModel = create_model( # type: ignore
        'InstructionStateModel',
        **instruction_state_objects #type: ignore
    )
    return InstructionStateModel #type: ignore


def resolve_instructions(prop: str) -> tuple[str, type[BaseModel]]:
    match prop:
        case "prompt":
            return "prompt", PromptValidator
        case "deliver_at":
            return "deliver_at", DeliveryValidator
        case "op_id":
            return "op_id", OpIdValidator
        case "version":
            return "version", VersionsValidator
        case _:
            raise ValueError(f"No such instruction property {prop}")
        
# ----------------------------------------- End of instruction state models ----------------------------------------- #