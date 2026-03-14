'''
docstring for op_man.py
'''

# PATH ONE

from Utility.pypolice.master_validator import OPDISPackageValidator, Flag
from Utility.ErrorHandler import initiate_error_handler, ErrorCodes, ErrorHandler
from Utility.logger import loggy
from uuid import UUID, uuid4

def log(msg: str) -> None:
    loggy("Medium/Operation_Manager/op_man", msg)

class OperationState:
    def __init__(self, flag: Flag) -> None:
        '''
        only one field for now. New when we add users'''
        self.flag = flag


# store op_id as key because uid can create multiple operations.
_operation_store: dict[UUID, OperationState] = {}


def create_operation(init_package: OPDISPackageValidator):

    '''
    we create a in-memory operation instance here. We then return instructions as on what is needed. This would depend on the flag which we will add slowly later. For now its just CREATE so let's see how that goes.
    '''
    '''
    # the idea is to keep init return the same for all flags.
    # so by that, we expect a format that includes something like this:
    uid
    op_id
    payload
    flag
    cat

    and the state would store:
    op_id 
    uid
    flag
    
    for reference of the state.

    To add this feature, what I would do is make a package that we make in opdis which would be similar to op state format which we can verify in PATH TWO

    for now, we would simply create a state in-memory and return sucess packet.
    '''

    '''
    I will keep the above as a past mistake note.
    UPDATE: I am going to:
    make uid the key so:
     1. Lookup is simpler
     2. uid is still unique identification.
     3. opid still gets generated and stored- structure is maintained.
    '''

    '''
    Oh... but keeping uid as key would mean one uid is hooked to one opid ie one operation. so for a new operation, a user would have to send a fresh response for uid. 
    Wait, is it bad? If we think about it- it would make it all safer... but then doesn't it make uid and op id basically do the same purpose at different levels?
    '''

    '''
    uid won't be passed here. decided. Removing all uid traces.
    '''

    # only unpacking flag and uid here for storage so flags also match. cat does not have to match so I did not call it in for now, its redundant.
    log("received init package for operation creation")
    try:
        flag = init_package.flag
        # create op_id
        op_id = uuid4()
            
        if op_id in _operation_store:
            initiate_error_handler(message="op_id already exists", errCode=ErrorCodes.OPERATION_ID_ALREADY_EXISTS.value, error=KeyError("Key (uid) must be unique"))
        log("No existing operation with the generated op_id. Creating operation state.")
        state = OperationState(flag)
        _operation_store[op_id] = state
        return_block = {
            "op_id" : op_id
        }
        log("Operation state created and stored successfully. Returning operation ID.")
        return return_block

    except ErrorHandler:
        raise

    except Exception as e:
        initiate_error_handler(message="cannot create operation.", errCode=ErrorCodes.CANNOT_CREATE_OPERATION_STATE.value, error=e)



# PATH TWO

def verify_operation(hydrate_package: OPDISPackageValidator):
    '''
    we just check if the hydrate package is in the state
    '''
    flag = hydrate_package.flag
    op_id = hydrate_package.op_id

    if op_id is None:
        # this is for enforcing better typing
        initiate_error_handler(message="No op ID provided", errCode=ErrorCodes.UNRECOGNIZED_OPERATION_ID.value, error=ValueError("Exception not found."))
        # a redundant return for typing.
        return
    
    try: 
        state_instance = _operation_store[op_id]
    except KeyError as e:
        initiate_error_handler(message="Unrecognized operation ID", errCode=ErrorCodes.UNRECOGNIZED_OPERATION_ID.value, error=e)
        return

    if flag == state_instance.flag:
        success = f"Verified operation for op_id: {op_id}. Forwarding to TADIS"
        return success
    
    initiate_error_handler(message="Operation verification failed. flag mismatch.", errCode=ErrorCodes.OPERATION_VERIFICATION_FAILED.value, error=ValueError("flag does not match the operation state."))