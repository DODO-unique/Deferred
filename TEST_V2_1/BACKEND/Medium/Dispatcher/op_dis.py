'''
docstring for OP_DIS.py
Operation dispatcher. This is the heart of the system, where we receive the payload, validate it, and dispatch it to the appropriate operation handler based on the flag and category.

THE MAIN GOALS:
1. Dispatcher is the communication link between the endpoints and the operation manager.
2. Dispatcher chooses what to send from the paylaod to the op man. payload is noise otherwise.
'''

from Utility.pypolice.payload_validator import Payload_validator
from Utility.logger import loggy
from Medium.operation_manager.op_man import create_operation, verify_operation
from Utility.pypolice.master_validator import OPDISPackageValidator, InterDispatchPackaging, IntimatePayload
from Medium.Dispatcher.ta_dis import tasks

def log(log: str) -> None:
    loggy("Dispatcher/OP_DIS", log)

# two paths. Path One and Path Two. 
# Path One is for init category, where we create new operations. Path Two is for hydrate category, where we update existing operations.

# PATH ONE

# a new type validator for package to be sent.

def opdis_path_one(payload: Payload_validator):

    '''
    packages things that are to be forwarded to op man for creating a new operation.
    We then wait for the response which has the op_id as well, return it to the endpoint as instruction.
    endpoint's init if statement would handle the unique instructions schema response.
    '''
    # we extract Pair, and uid for now - to keep it simple for the first MVP
    flag = payload.flag
    cat = payload.cat
    log(f"Creating PATH ONE package with flag: {flag}, cat: {cat}")
    
    package: OPDISPackageValidator = OPDISPackageValidator(
        flag=flag,
        op_id=None
    )

    # Control to op-man
    log("Passing control to op man for operation creation")
    operation_id =  create_operation(init_package=package)
    log("Received respose from op-man, returning to endpoint")
    return operation_id
    




# PATH TWO
def opdis_path_two(payload: Payload_validator):

    '''
    We take payload. Payload has Pair and op_id.
    1. We verify op_id, then forward it to the task dispatcher

    We can't send payload to op-man to verify op_id as it reduces the purpose of the dispatcher itself.
    But I will take that risk. It seperates concerns more clearly.
    '''

    # we extract things and package it the way op-man wants. Mind that we are not sharing the payload to op-man at all.

    flag = payload.flag
    op_id = payload.content.op_id

    hydrate_package: OPDISPackageValidator = OPDISPackageValidator(
        flag=flag,
        op_id=op_id
    )

    # this is a one way road. If there is a response, we simply add that to log and move on.
    message = verify_operation(hydrate_package)
    if isinstance(message, str):
        log(message)


    # Once confirmed, we can go on and share pyalod to tadis. Tadis's returns are what we return in this function.

    user_prompt = payload.content.prompt
    user_delivery = payload.content.deliver_at
    task_package: InterDispatchPackaging = InterDispatchPackaging(
        flag= flag,
        intimate_payload = IntimatePayload(
            prompt= user_prompt,
            delivery= user_delivery
        )
    )
    
    creation_status = tasks(task_package)
    return creation_status