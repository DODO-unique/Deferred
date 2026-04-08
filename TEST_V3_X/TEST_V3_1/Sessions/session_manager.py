'''
docstring for session manager

manage sessions. Tasks seperated into functions
'''
from Touch.ORM_2 import fetch_line, new_session, get_session, remove_session
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

    # create a new session!
    result = await new_session(session_token=token, user = select_object) 
    if result:
        log("created new session; returning token to Verification")
        return token
    initiate_error_handler(message="could not create session", errCode=ErrorCodes.CANNOT_CREATE_SESSION.value, error=ValueError("could not create session"))

async def get_session(uname: UserName):
    '''
    get session for a user.
    '''
    select_object = await fetch_line(uname=uname)
    session = await get_session(user_row=select_object)
    if session:
        log("Wrapped session object")
        return { "token" : session.token, "expires_at" : session.expires_at}

    initiate_error_handler(message="could not get session", errCode=ErrorCodes.CANNOT_GET_SESSION.value, error=ValueError("could not get session"))

async def delete_session(uname: UserName):
    '''
    delete session for a user.
    '''
    select_object = await fetch_line(uname=uname)
    result = await remove_session(user_row=select_object)
    if result:
        log("deleted session")
        return True
    initiate_error_handler(message="could not delete session", errCode=ErrorCodes.CANNOT_DELETE_SESSION.value, error=ValueError("could not delete session"))
