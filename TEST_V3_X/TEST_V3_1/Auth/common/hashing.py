import bcrypt
from Utility.pypolice.master_validator import Password, UserName
from Utility.logger import loggy
from Touch.ORM_1 import fetch_password

def log(msg: str) -> None:
    loggy("Auth/common/hashing.py", msg)

def hash_password(pt_password: Password) -> bytes:
    log(f"pt_password: {pt_password}")
    log(f"pt_password: {pt_password.value}")
    password = pt_password.value.get_secret_value().encode('utf-8')
    salt = bcrypt.gensalt()
    digest = bcrypt.hashpw(password, salt)
    return digest

async def verify_password(pt_password: Password, uname: UserName):
    '''
    This will take plain text password, pass it to hasher, hash the plaintext password, then send it to ORM to check, and then return the response.
    '''
    # first hash the password
    log("hashing password")
    digest = hash_password(pt_password)

    # we share the digest for verification to ORM
    log("sharing digest for verification")
    result = await fetch_password(uname)

    if result is None:
        log("User not found.")
        return False
    
    if bcrypt.checkpw(digest, result.encode('utf-8')):
        log("Password verified.")
        return True
    else:
        log("Password not verified.")
        return False
    

    