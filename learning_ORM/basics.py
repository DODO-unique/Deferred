# we are gonna use create engine to create engine which we willuse to connect to the database
from sqlalchemy import create_engine, text

# this is the sqlalchemy core

# create engine
engine = create_engine('sqlite:///mydb.db', echo=True)

conn = engine.connect()
conn2 = engine.connect()

conn.execute(text("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, name TEXT, age INTEGER)"))

# commit the changes made through conn
conn.commit()

conn2.execute(text("CREATE TABLE IF NOT EXISTS test(id int, name str)"))

# so we can have multiple instances and then commit them later according to our convienience...?
conn2.commit()

# yeup! that works.


# but don't do that 🦤
# one connection instance = one cycle. If you think about it, they can collide, so no.

