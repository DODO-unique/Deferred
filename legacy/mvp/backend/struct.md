would go with a simple format:

DB -> ORM -> LOGIC -> FastAPI

it would be:

DB -> touch -> engine -> dock

The first step is to design a simple read operation.
The dock would pass a ticket to engine, engine verifies ticket and converts it to raw index, sends index to touch. 
touch takes the index, searches, gives the result.
Touch does no thinking, it trusts engine completely.
Engine deals with all the logic
dock makes sure it relays only the truth, thus filters craps, firmlly sends requests to engine.
logs are managed by engine.