'''
boundary_validator.py
'''

from pydantic import BaseModel, BeforeValidator
from typing import Annotated
from email_validator import EmailNotValidError, validate_email
from Utility.pypolice.master_validator import ISODateTime
from Utility.ErrorHandler import initiate_error_handler, ErrorCodes


# we need to sanitize email, prompt, delivery_time.

def process_string(value: str):
    '''
    Just you wait. We will add encryption logic here some day
    '''
    value = value.strip()
    return value

def process_mail(value: str):
    '''
    we will technically only get verified email here (email and login module TBD as of 22nd Feb)
    For now, I am adding from external library (I know we hate it mutually when we have to add external dependencies, but this is for MVP only)
    #Todo: make sure your custom email validator name is not same.
    '''
    try:
        validated_email = validate_email(value, check_deliverability=False)
        email = validated_email.normalized
        return email
    except EmailNotValidError as e: #type: ignore
        initiate_error_handler(message="Invalid email format", errCode=ErrorCodes.INVALID_EMAIL_FORMAT.value, error=e)

# we take the string and make sure it is stripped
class Prompt(BaseModel):
    value: Annotated[str, BeforeValidator(process_string)]


# we take the email string making sure it is an email
class Mail(BaseModel):
    value: Annotated[str, BeforeValidator(process_mail)]


# deilvery_time should be in datetime object with utc time.
class Delivery(BaseModel):
    value: ISODateTime

class CreateFlagPackage(BaseModel):
    prompt: Prompt
    mail: Mail
    delivery: Delivery

