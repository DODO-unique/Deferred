'''
Docstring for TEST_v1.0.Engine.operation

Goal is to define what each flag should do in a certain type.
'''

from uuid import uuid4
from datetime import datetime


from Utility.pydantic_models.protocol_schema import VersionsValidator, Category, createInitiation
from Utility.logger import loggy

def log(msg: str):
    loggy(local="Engine/operation", log=msg)

InstructionReturnType = dict[str, bool]

# we will frist take the create flag only
class create:

    def __init__(self):
        self.state = createInitiation(
            op_id = None,
            next_state = "Not Set",
            completed_steps = {},
            version = VersionsValidator(value="Tv_1.0")
        )
    
    def executing_filter(self, cat: Category) -> InstructionReturnType:
        if cat.value == 'init':
            if self.state.next_state == 'Not Set':
                log(
                    "reached initiation state. Forwarding control to _initiation."
                )
                instructions = self._initiation()
                log(
                    "returning instructions (1)"
                )
                return instructions
        
        raise ValueError("Deferred: Can not execute filter for category")


    def _initiation(self) -> InstructionReturnType:
        # generate op_id
        uid = uuid4()

        # store it, change self.state and return the instructions 
        self.state.op_id = uid
        self.state.next_state = 'context'
        self.state.completed_steps['phases_completed'] = 'init'
        self.state.completed_steps['timestamp'] = datetime.now().isoformat()
        self.state.version.value = "Tv_1.0"

        instructions = {
            "payload" : True,
            "time" : True,
            "creation_time" : True,
            "op_id" : True,
            "version" : True
        }


        return instructions
    