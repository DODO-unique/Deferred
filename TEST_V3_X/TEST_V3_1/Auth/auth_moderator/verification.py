'''
This creates sessions as well. So we have to create a relevant session verification function in ORM.

To verify we simply have to check if the credentials are avaialble. Usually only uname and passwords
'''

from Utility.pypolice.master_validator import UserName, Password
from Auth.common.hashing import verify_password
from Auth.common.username_check import check_username
from Utility.ErrorHandler import initiate_error_handler, ErrorCodes

# take uname and password

async def verification(uname: UserName, password: Password):
    # check credentials

    # first uname
    uname_result = await check_username(uname)
    if not uname_result['username_available']:
        # if username not available, then:
        initiate_error_handler(message="Username not found", errCode=ErrorCodes.USER_NOT_FOUND.value, error=ValueError("Username not found"))
    
    # if username is available, check password
    result = await verify_password(pt_password=password, uname=uname)
    if not result:
        initiate_error_handler(message="Incorrect password", errCode=ErrorCodes.INCORRECT_PASSWORD.value, error=ValueError("Incorrect password"))

    # at this point it means the credentials are correct. Verification complete.
    # now we create a session for the user.