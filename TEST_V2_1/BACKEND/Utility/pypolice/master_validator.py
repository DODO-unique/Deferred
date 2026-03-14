from datetime import datetime, timezone
from typing import Annotated, Optional
from pydantic import BaseModel, field_validator, BeforeValidator
from uuid import UUID
from Utility.ErrorHandler import initiate_error_handler, ErrorCodes


# this is the start. Everything in-transit is datetime object.
def epoch_to_datetime(epoch: int | datetime) -> datetime:
    # print(f"epoch value: {repr(epoch)}, type: {type(epoch)}")
    if isinstance(epoch, datetime):
        if epoch.tzinfo is None:
            initiate_error_handler(message="Incorrect temporal type: datetime object must be timezone-aware", errCode=ErrorCodes.INCORRECT_TEMPORAL_TYPE.value, error=ValueError("datetime object must come with timezone"))
        return epoch.astimezone(tz=timezone.utc)
    if not isinstance(epoch, int): #type: ignore
        # holler when not int or datetime
        initiate_error_handler(message="Incorrect temporal type: epoch must be an integer", errCode=ErrorCodes.INCORRECT_TEMPORAL_TYPE.value, error=ValueError("epoch must be an integer"))
    elif epoch > 1e11:
        initiate_error_handler(message="Incorrect temporal type: epoch must be in seconds", errCode=ErrorCodes.INCORRECT_TEMPORAL_FORMAT.value, error=ValueError("epoch must be in seconds"))
    datetime_object = datetime.fromtimestamp(epoch, tz=timezone.utc)
    return datetime_object

ISODateTime = Annotated[
            datetime,
            BeforeValidator(epoch_to_datetime)
            ]

# this is if we are wrapping as {value: ...}
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
        all_versions = {'Tv_1.0', 'Tv_1.1', 'Tv_2.1'}
        if v not in all_versions:
            raise ValueError(f"No such version {v}")
        return v
    

# opdis package validator:
class OPDISPackageValidator(BaseModel):
    flag: Flag
    op_id : UUID | None

class IntimatePayload(BaseModel):
    prompt: Optional[str]
    delivery: Optional[ISODateTime]
    # OTHER FLAGS HERE

# opdis to tadis packaging:
class InterDispatchPackaging(BaseModel):
    flag: Flag
    intimate_payload: IntimatePayload
