from sqlalchemy import create_engine, MetaData, Column, Table, Integer, String, Boolean, TIMESTAMP, ForeignKey

# this is the sqlalchemy core

# create engine, this time with postgres
engine = create_engine('postgresql+psycopg2://postgres:victor@localhost:5432/victortestdb', echo=True)

# no conn object here, we 

# if we do the same with meta, which is how it is usually done:

meta = MetaData()

'''
users
-----
id              INTEGER PK
email           VARCHAR UNIQUE NOT NULL
is_active       BOOLEAN NOT NULL
created_at      TIMESTAMP NOT NULL
'''
users = Table(
    "users",
    meta,
    Column('id', Integer, primary_key=True),
    Column('email', String, unique=True, nullable=False),
    Column('is_active', Boolean, nullable=False),
    Column('created_at', TIMESTAMP(timezone=True), nullable=False)
)

'''
products
--------
id              INTEGER PK
name            VARCHAR NOT NULL
price_cents     INTEGER NOT NULL
'''
products = Table(
    "products",
    meta,
    Column('id', Integer, primary_key=True),
    Column('name', String, nullable=False),
    Column('price_cents', Integer, nullable=False)
)


'''
orders
------
id              INTEGER PK
user_id         INTEGER FK → users.id
product_id      INTEGER FK → products.id
quantity        INTEGER NOT NULL
created_at      TIMESTAMP NOT NULL
'''
orders = Table(
    "orders",
    meta,
    Column('id', Integer, primary_key=True),
    Column('user_id', Integer,  ForeignKey("users.id")),
    Column('product_id', Integer, ForeignKey("products.id")),
    Column('quantity', Integer, nullable=False),
    Column('created_at', TIMESTAMP(timezone=True), nullable=False)
)

meta.create_all(engine, checkfirst=True)

