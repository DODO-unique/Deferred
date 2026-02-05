from datetime import datetime, timezone
from typing import Optional, Annotated
from pydantic import BaseModel, create_model, field_validator, Field, BeforeValidator
from uuid import UUID


# ----------------------------------------- payload models ----------------------------------------- #

def epoch_to_datetime(epoch: int) -> datetime:
    if epoch > 1e11:
        raise ValueError("epoch must be in seconds")
    datetime_object = datetime.fromtimestamp(epoch, tz=timezone.utc)
    return datetime_object

ISODateTime = Annotated[
            datetime,
            BeforeValidator(epoch_to_datetime)
            ]

class CanonicalTime(BaseModel):
    value: ISODateTime

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

# Like, why did I have two of these  
# class Versions(BaseModel):
#     value: str

#     @field_validator('value')
#     @classmethod
#     def check_version(cls, v: str):
#         all_versions = {'Tv_1.0'}
#         if v not in all_versions:
#             raise ValueError(f"No such version {v}")
#         return v
class VersionsValidator(BaseModel):
    value: str

    @field_validator('value')
    @classmethod
    def check_version(cls, v: str) -> str:
        all_versions = {'Tv_1.0'}
        if v not in all_versions:
            raise ValueError(f"No such version {v}")
        return v
    

class Payload_body(BaseModel):
    prompt: Optional[str]
    deliver_at: Optional[ISODateTime]
    op_id: Optional[UUID]
    # meta
    version: Optional[VersionsValidator]
    creation_time: Optional[CanonicalTime]
    

    
class Payload_content(BaseModel):
    '''
    Docstring for Payload_content
    This should have a pair of cat and flag,
    the corpus/body, ofcourse, and
    any other fields that may be added later
    '''
    prompt: bool
    deliver_at: bool
    op_id: bool
    body: Payload_body
    # any other fields can be added later


class Payload_validator(BaseModel):
    flag: Flag
    cat: Category
    content: Payload_content
    packed_at: CanonicalTime
    version: VersionsValidator


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
        case "creation_time":
            return "creation_time", CanonicalTime
        case _:
            raise ValueError(f"No such instruction property {prop}")
        
# ----------------------------------------- End of instruction state models ----------------------------------------- #

# ----------------------- This is for the Engine/ -------------------

class createInitiation(BaseModel):
    op_id : Optional[UUID] = None
    next_state : str
    completed_steps : dict[str, str]
    version : VersionsValidator

# ----------------------- End of Engine/ -------------------