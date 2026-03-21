'''
docstring for session manager

manage sessions. Tasks seperated into functions
'''
from Touch.ORM_2 import fetch_line, new_session
from Utility.pypolice.master_validator import UserName
from Utility.logger import loggy
from uuid import uuid4
from Utility.ErrorHandler import initiate_error_handler, ErrorCodes

def log(msg: str) -> None:
    loggy("Sessions/session_manager", msg)

async def create_session(uname: UserName):
    '''
    create session. 
    session has:
    1. id
    2. user_id
    3. token
    4. created_at
    5. expires_at
    # we have to decide the above here and send to ORM, there add an entry.
    out of those 5, some are created automatically. like id, created at, expires_at
    we need to set token.
    We also need to fetch user id which will refer to the user table.
    information relevant to this would be used relationally.
    '''
    # this returns a ScalarResult object. We can pass it as model
    select_object = await fetch_line(uname= uname)

    token = uuid4()
    if select_object is None:
        initiate_error_handler(message="user not found", errCode=ErrorCodes.USER_NOT_FOUND.value, error=ValueError("user not found"))   
        return #redundant

    # create a new session!
    result = await new_session(session_token=token, user = select_object) 
    if result:
        log("created new session; returning token to Verification")
        return token
    initiate_error_handler(message="could not create session", errCode=ErrorCodes.CANNOT_CREATE_SESSION.value, error=ValueError("could not create session"))