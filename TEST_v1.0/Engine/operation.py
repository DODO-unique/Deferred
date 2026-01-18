'''
Docstring for TEST_v1.0.Engine.operation

Goal is to define what each flag should do in a certain type.
'''

# we will frist take the create flag onlys
def create(cat: str):
    '''
    Docstring for create: handles all create stages and operations, and state
    
    :param cat: sanitized, validated string of category
    :type cat: str, with all caps through pydantic super validation in docking layer
    '''

    if cat == 'init':
        # initiation signal, this means we have to create a op_state. We have to make sure the given id does not take any other signals now. Only what we request.
        # we will do that by making sure we make it obey operation_id op_id. 
        # when defining state, we have to make sure we are defining an op_id, this op_id is required to identify state.
        # the op_id should be global, so we should have a state where op_id is tracked.

