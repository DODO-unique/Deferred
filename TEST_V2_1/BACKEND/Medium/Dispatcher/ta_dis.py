'''
docstring for tadis. goal is to dispatch tasks based on the category to engine.
'''

from Utility.pypolice.master_validator import InterDispatchPackaging
from Engine.function_manager import create_function
from Utility.logger import loggy

def log(log: str) -> None:
    loggy("Dispatcher/TA_DIS", log)

def tasks(task_package: InterDispatchPackaging):
    '''
    let's define the structure of task_package with reason for each entry:
    1. We need flag- this tells us what the general task is. 
    2. We need prompt and time- of course

    and that's it!
    '''

    # first we unpack
    flag = task_package.flag

    if flag.value == "CREATE":
        # FIXME: Only works for CREATE flag and is for test run.

        # pass control to Engine.
        log("Received CREATE flag in TA_DIS. Passing control to Engine to create function.")
        creation_status = create_function(task_package.intimate_payload)
        return creation_status


    