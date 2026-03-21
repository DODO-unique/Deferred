For Docker:
1. On windows, first start docker desktop. That starts the daemon.
2. Check your running containers: `docker ps`
3. Note the names of these images
4. Start these containers (load images into containers): `docker start <name>`


For psql:
1. once you have your docker started, you would need to enter the psql TTY: `docker exec -it <name> psql -U <username> -d <database>`
   1. A few things you should note. First, this exec executes.
   2. -i is for interaction, -t is for TTY. 
   3. since we are using -t, we have to tell TTY of what, psql.
   4. -U username is... necessary if you have more than one user


**NOTE:** the one in which you perform operations and the one where you created your table classes, keep these modules different. Your table classes and types should be defined in a module (and already created, no need to create them everytime), you then import these classes and use the imports as a reference for sessions, commits, engine etc. 
Also note that you have to think of this in async, so a function should be strictly scoped.
And keep a habit of creating tables AFTER sleep for at least 7 hours in prod DB. Promise me that.

for ORM:
1. DDL -> Base.metadata.create_all, table are classes, classes inherit Base, remember to add `checkfirst=True` to not run into duplicate table creation. It is the universal 'IF NOT EXISTS' of ORMs.
2. **All other statements need a session.** You still need an engine to which you **bind a session maker and session.** Now, you can use methods like add(), .query(), which will stack. 
3. Then you can commit the stack. [it feels like staging? It should]
and... that's it.
BUT, and remember this: table classes are not just blueprints for creation of Tables in SQLA, they are also the frameworks that session follows.
So remember how for insert you go `INSERT INTO <table-name> (<column-names>) VALUE (<values>);`, similarly, we need some reference of the table to add stuff, that we do with making table classes anyway.
BUT, and ik you thought of it, what if you create a different class structure than the actual sql?
That is why things like Alembic exist that sync classes and sql structure.
But for us, stay safe, wear mask 💅
1. when using ORM session.add, in Column you can use server_default where you can directly use the things that the server considers for default.
   so imagine SQL considers uuid7() as a valid default (it does not- uuid7() is not recognized by SQL )
   we can go `(... , server_default="uuid7()")`
   Notice the string is important- in fact, SQLA later wraps it in a text(). Though be vary, try to wrap it in text() as much as you can. Also, you import text from sqlalchemy, not sqlalchemy.orm

   also: `server_default=text("'pending'::enum_status")`
   [BUT this works if type already exists. Otherwise ]
   `::type` means you get to point at type in postgres. So even indexes 👀 
2. SQLA converts datetime objects with tzinfo into TIMESTAMPTZ cleanly, even on retrieval. So trust the process.
   1. Note that it is TIMESTAMPTZ, so timestamp+tz, not timestampz as in plural, no not that.
   2. timstamptz stores stuff in utc by default, so mind that.
3. `default=uuid4` vs `default=uuid4()`: you have to pass a bare function- the latter calls it right away, the former passes the function so it can run there. It is a general python thing. We can apply this elsewhere too; remember how you create dictionaries with values of function names and then do `dictionary['key']()` to call the function? Yeah, ORM is trying to do the same with your arguments. Help it.

for ORM part 2:
How to you use select in ORMs? 
1. import select from `sqlalchemy`
2. do session.execute(select(<table-class-name>).where(<table-class-name>.<table-class-method>)).scalars().all() [just an example]
3. now, for example say you have a class called Users (not the `__tablename__ = 'users'`,the name of the class for ORM. Always), this class has id, uname, uid, etc. Now you have many entries in this. You have to check for a certain username. You can go: `stmt = select(Users).where(Users.uname == test_username)`. 
4. That is your statement file. Now, execute your statement: result = session.execute(stmt)
5. now, result is a `ChunkedIteratorResult` object. This is basically waiting for you to give it some kind of instruction (almost disappointed it exists).
6. so you use one of these on `ChunkedIteratorResult` ->
   1. .all()
   2. .scalars()
   3. .first()
7. before we go into that, look at this flow:
   1. you create a stmt -> execute statment ->
   2. gives you `ChunkedIteratorResult` -> operate it with `scalars()` ->
   3. gives you `ScalarResult` -> operate with `.all()`, etc. _>
   4. gives you [Users, Users] where Users are objects.
8. Now, what was all that? we need to understand what scalars is first. 
scalars()
   1. a general .all() or .first() on `ChunkedIteratorResult` you get objects like: [(Users,), (Users,)]
   2. with scalars(), you get [Users, Users]
   3. In the former, you have to extract each tuple like result[0][0].id instead in scalars() you can just do result[0].id (or not if you are just using scalar_one series) in the same situation.
   4. That's the difference. that's it.
1. Now, scalar has some types in it:
   1. scalar_one() : the first row only, throws NoResultFound error if nothing found. 
   2. scalar_one_or_none() : the first row only, but returns None if nothing found.
   3. scalars().all() : returns all rows
   4. scalars().first(): same as scalar_one_or_none if you think about it but there is one big difference: if there are more than one rows, .first() simply shares first row, scalar_one_or_none screams with `MultipleResultsFound`


in SQL:
1. in postgres, you have to login with a database on terminal to enter that database. or just enter as psql -U <username> and you enter to a postgres DB. there you can do `\l` and cehck other databases. 
2. Then to change databases you can do `\c <dbname>` or if you are a dum dum create a DB: `CREATE DATABASE ppdb;`


In fastAPI:
1. when calling exception_handler you have to still import request even if you are not using it.
2. exception_handler catches all exceptions of the type it is fed- like say exception_hander(KeyError) catches all KeyError exceptions in the relevant code base. But use it for custom exceptions only. 

