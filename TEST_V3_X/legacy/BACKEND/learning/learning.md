For Docker:
1. On windows, first start docker desktop. That starts the daemon.
2. Check your images: `docker ps`
3. Note the names of these images
4. Start these containers (load images into containers): `docker start <name>`


For psql:
1. once you have your docker started, you would need to enter the psql TTY: `docker exec -it <name> psql -U <username> -d <database>`
   1. A few things you should note. First, this exec executes.
   2. -i is for interaction, -t is for TTY. 
   3. since we are using -t, we have to tell TTY of what, psql.
   4. -U username is... necessary if you have more than one user
   5. -d is very important, because if psql decides for you- you can't change databases from inside psql. That is possible in MySQL by `USE <dbname>`



for ORM:
1. DDL -> .create_all, table are classes, Base lies here
2. All other statements need a session in which you work on them. You still need an engine to which you bind a session maker and session. Now, you can use methods like add(), .query(), which will stack. Then you can commit the stack. [it feels like staging? It should]
and... that's it.
BUT, and remember this: table classes are not just blueprints for creation of Tables in SQLA, they are also the frameworks that session follows.
So remember how for insert you go `INSERT INTO <table-name> (<column-names>) VALUE (<values>);`, similarly, we need some reference of the table to add stuff, that we do with making table classes anyway.
BUT, and ik you thought of it, what if you create a different class structure than the actual sql?
That is why things like Alembic exist that sync classes and sql structure.
But for us, stay safe, wear mask 💅
3. when using ORM session.add, in Column you can use server_default where you can directly use the things that the server considers for default.
   so imagine SQL considers uuid7() as a valid default.
   we can go `(... , server_default="uuid7()")`
   Notice the string is important- in fact, SQLA later wraps it in a text(). 

   also: `server_default=text("'pending'::enum_status")`
   `::type` means you get to point at type in postgres. So even indexes 👀 
4. SQLA converts datetime objects with tzinfo into TIMESTAMPTZ cleanly, even on retrieval. So trust the process.
   1. Note that it is TIMESTAMPTZ, so timestamp+tz, not timestampz as in plural, no not that.
   2. timstamptz stores stuff in utc by default, so mind that.
5. `default=uuid4` vs `default=uuid4()`: you have to pass a bare function- the latter calls it right away, the former passes the function so it can run there. It is a general python thing. We can apply this elsewhere too.

in SQL:
1. in postgres, you have to login with a database on terminal to enter that database. Remember that.


In fastAPI:
1. when calling exception_handler you have to still import request even if you are not using it.
2. exception_handler catches all exceptions of the type it is fed- like say exception_hander(KeyError) catches all KeyError exceptions, if 