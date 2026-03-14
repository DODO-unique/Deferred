Structure:
frontend -> flag | cat
backend boundary -> which flag which cat
operation -> gives operation state
sql boundary -> adds/edits into sql

now, we need filters and seperate concerns. 

A flag | cat piece should come in two different ways:
1. Set operation state
2. Verify operation state


So, let the frontend send flag | cat. We take them and simply forward flag | cat to operation dispatchers. operation dispatchers check flag AND cat, then decide one of the two ways above.
based on the two ways, if it is 1, it is sent to path 1 of operations. if it is 2, it is sent to path 2 of operations. 
operations path 2 verifies state and forwards signal to task dispatchers, task dispatchers, knowing they have been given state-verified tasks, assign tasks forward to engine. Engine has instructions for how each task should work (for CREATE flag with hydrate cat, it would add to DB, for example). Engine is directly connected to Touch module-set which includes ORMs and deterministic pydantic verifiers.

concurrently, there would be some states that act as listeners parellel to this event flow:
1. Logger - logs things.
2. Error Handler - handles errors gracefully.

TODOs:
1. create a states.md file to keep track of all the states that are used, their scope, and their reason for existence.
2. all time in-transit is datetime object- when using that object, unwrap it in the way you want- but transfer stays in a datetime object

Error Handler: Raises errors which are caught by fastAPI error_handler. We also work with enums and create cool codes ✨