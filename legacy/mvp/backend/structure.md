Layers of the backend:
1. DBs
2. ORMs
3. logic
4. FastAPI

MVP will be largely single user. We will use one DB for it. 
The basic concerns would be:
    1. Confirm contact_ID, confirm Notifications
    2. Aggresively sanitize information
    3. Store information
    4. Done.

Each cycle would look like the above. Vercel would have a function that would trigger one of our local function to check the stats every minute. We will also add a manual button for this 

Logic layer should have a sub-layer only responsible for strict sanitization.
Ideally, fastAPI layer should apply ratelimits
Logic layer should understand that it does make one request do the whole job- there must be 'incomplete' requests that would build satisfy any modification to the DB.

