'''
docstring for function_manager.
Main purpose is to take decisions.
'''

from Utility.pypolice.master_validator import IntimatePayload
from Touch.boundary_validator import CreateFlagPackage, Prompt, Delivery, Mail
from Touch.ORM import create_flag
from Utility.ErrorHandler import initiate_error_handler, ErrorCodes

def create_function(payload: IntimatePayload):
    pay_prompt = payload.prompt
    pay_delivery = payload.delivery
    # user_email = session_emails

    # now, I was thinking we can have different dict paths for each different term. Like prompt has an entirely different handler, delivery has its own handler.

    demo_email = "victorprescott@gmail.com"
    if pay_delivery and pay_prompt and demo_email:
        package = CreateFlagPackage(
            prompt=Prompt(value=pay_prompt),
            mail=Mail(value=demo_email),
            delivery=Delivery(value=pay_delivery),
        )

        result = create_flag(package)
        return result
     
    initiate_error_handler(message="Invalid payload content, missing either prompt, delivery, or email", errCode=ErrorCodes.INVALID_PAYLOAD_CONTENT.value, error=ValueError("Payload must include prompt, delivery, and email"))