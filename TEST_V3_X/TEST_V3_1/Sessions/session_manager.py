'''
docstring for session manager

manage sessions. Tasks seperated into functions
'''
from Touch.ORM_2 import fetch_line
from Utility.pypolice.master_validator import UserName


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
    
    
    pass