from Touch.ORM_2 import fetch_line, does_session_exist
from Utility.pypolice.master_validator import UserName
from Utility.logger import loggy
from uuid import uuid4
from Utility.ErrorHandler import initiate_error_handler, ErrorCodes


async def is_session_running(uname: UserName):

    user = await fetch_line(uname)
    is_running = await does_session_exist(user_row=user)
    return is_running