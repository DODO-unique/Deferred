'''
Docstring for TEST_v1.0.dock.enums

stores enums, filters and serves functions
'''

from Engine.operation import create, InstructionReturnType
from Utility.logger import loggy
from typing import Callable
from Utility.pydantic_models.protocol_schema import Category


def log(msg: str):
    loggy(local="dock/enums", log=msg)

instructionsType = Callable[[Category], InstructionReturnType]

class FlagRegistry:
    def __init__(self):
        self._registry: dict[str, instructionsType] = {}

    def register(self, name: str) -> Callable[[instructionsType], instructionsType]:
        def wrapper(func: instructionsType) -> instructionsType:
            self._registry[name] = func
            return func
        return wrapper
    
    def execute(self, name: str, cat: Category) -> InstructionReturnType:
        if name in self._registry:
            return self._registry[name](cat)
        raise ValueError("No registered flag and function")
    
registry = FlagRegistry()

@registry.register("CREATE")
def create_ops(cat: Category):
    operation_object = create()
    log(
        "Started a CREATE process, moving control to relevant operation handler"
    )
    instructions = operation_object.executing_filter(cat)
    log(
        "returning instructions (2)"
    )
    return instructions

def call_flags(flag: str, cat: Category) -> InstructionReturnType:
    log(
        "requested execution. Executing call"
    )
    data = registry.execute(name=flag, cat=cat)
    log(
        "returning instructions (3)"
    )
    return data