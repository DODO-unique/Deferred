'''
Docstring for TEST_v1.0.dock.resolver

resolves categories, filters and serves functions
'''

from Engine.operation import create, InstructionReturnType
from Utility.logger import loggy
from typing import Callable, Optional
from Utility.pydantic_models.protocol_schema import Category, Payload_body


def log(msg: str):
    loggy(local="dock/resolver", log=msg)

instructionsType = Callable[[Category, Optional[Payload_body]], InstructionReturnType]

class FlagRegistry:
    def __init__(self):
        self._registry: dict[str, instructionsType] = {}

    def register(self, name: str) -> Callable[[instructionsType], instructionsType]:
        def wrapper(func: instructionsType) -> instructionsType:
            self._registry[name] = func
            return func
        return wrapper
    
    def execute(self, name: str, cat: Category, payload: Payload_body | None) -> InstructionReturnType:
        if name in self._registry:
            return self._registry[name](cat, payload)
        raise ValueError("No registered flag and function")
    
registry = FlagRegistry()

@registry.register("CREATE")
def create_ops(cat: Category, payload: Payload_body | None) -> InstructionReturnType:
    operation_object = create()
    log(
        "Started a CREATE process, moving control to relevant operation handler"
    )
    instructions = operation_object.executing_filter(cat, payload)
    log(
        "returning instructions (2)"
    )
    return instructions

def call_flags(flag: str, cat: Category, payload: Payload_body | None) -> InstructionReturnType:
    log(
        "requested execution. Executing call"
    )
    data = registry.execute(name=flag, cat=cat, payload=payload if payload is not None else None)
    log(
        "returning instructions (3)"
    )
    return data