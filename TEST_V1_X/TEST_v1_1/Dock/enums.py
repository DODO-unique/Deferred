'''
Docstring for TEST_v1.0.dock.enums

stores enums, filters and serves functions
'''

from Engine.operation import create
from Utility.logger import loggy

def log(msg: str):
    loggy(local="dock/enums", log=msg)

class FlagRegistry:
    def __init__(self):
        self._registry = {}

    def register(self, name):
        def wrapper(func):
            self._registry[name] = func
            return func
        return wrapper
    
    def execute(self, name, cat, *args, **kwargs):
        if name in self._registry:
            return self._registry[name](cat, *args, **kwargs)
        raise ValueError("No registered flag and function")
    
registry = FlagRegistry()

@registry.register("CREATE")
def create_ops(cat):
    operation_object = create()
    log(
        "Started a CREATE process, moving control to relevant operation handler"
    )
    instructions = operation_object.executing_filter(cat)
    log(
        "returning instructions (2)"
    )
    return instructions

def call_flags(flag: str, cat: str):
    log(
        "requested execution. Executing call"
    )
    data = registry.execute(name=flag, cat=cat)
    log(
        "returning instructions (3)"
    )
    return data