'''
Docstring for payload_model.py
For Payload validation.
Used in Dock layer only. 
'''

from pydantic import BaseModel
from typing import Optional
from uuid import UUID
from .master_validator import ISODateTime, CanonicalTime, Category, Flag, VersionsValidator, Mail, UserName, Password

# ------------------------------------------- payload models ----------------------------------------------- #

class _Payload_body(BaseModel):
    prompt: Optional[str]
    deliver_at: Optional[ISODateTime]
    op_id: Optional[UUID]
    # META fields:
    creation_time: Optional[ISODateTime]



# op state and uid are linked together very closely.
class Payload_validator(BaseModel):
    flag: Flag
    cat: Category
    uid: UUID
    content: _Payload_body
    packed_at: CanonicalTime
    version: VersionsValidator

'''
a demo payload looks like this:
{
    flag: { value: "CREATE" },
    cat: { value: "init" },
    content: {
            prompt: null,
            deliver_at: null,
            op_id: null,
            creation_time: 1771590063
    },
    packed_at: {
        value: 1771590063
    },
    version: { value: "Tv_1.0" }
}
'''

# ------------------------------------------ End of payload models ----------------------------------------- #


class RegisterPayloadValidator(BaseModel):
    user: UserName
    mail: Mail
    pt_password: Password # plaintext password - secret string extracted by get_secret_value()
