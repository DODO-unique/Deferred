# this should not touch logic. this is just for audits and structure
from sqlalchemy import text, create_engine
import os

PATH = os.path.join(os.path.dirname(__file__), 'schema.sql')
URL = 'postgresql://victor:yomama@localhost:5506/deferred'

engine = create_engine(URL, echo=True)

with engine.connect() as conn:
    with open(PATH) as f:
        result = conn.execute(text(f.read()))
    conn.commit()
