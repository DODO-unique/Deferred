'''
docstring of ORM.py

Now, lookie here, this is the good part. 
First we setup the basic things we need in an ORM, and then we can give it the twist we want in it.
'''

# to setup ORM we would need create_engine for creating engine, sessionmaker to create session that bind to this engine, and then create a session instance which we then use to manage our said DB.

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from Touch.orm_schema import ScheduledMessages
from Touch.boundary_validator import CreateFlagPackage
from Utility.ErrorHandler import initiate_error_handler, ErrorCodes
from Utility.logger import loggy

def log(msg: str) -> None:
    loggy("Touch/ORM", msg)

URL = "postgresql://victor:yomama@localhost:5506/deferred"

try:
    ENGINE = create_engine(URL)
    SESSION = sessionmaker(bind=ENGINE)
except Exception as e:
    initiate_error_handler(message="Cannot connect to database", errCode=ErrorCodes.DATABASE_CONNECTION_FAILED.value, error=e)


def create_flag(create_package: CreateFlagPackage):
    # we will trust this blindly, as we have already validated it. Strictly.
    log(f"Creating a new entry in the database with email: {create_package.mail.value}, prompt: {create_package.prompt.value}, and delivery time: {create_package.delivery.value}")
    try:
        with SESSION() as session:
            entry = ScheduledMessages(
                email=create_package.mail.value,
                prompt=create_package.prompt.value,
                execute_at=create_package.delivery.value
            )
            session.add(entry)
            session.commit()
    except Exception as e:
        initiate_error_handler(message="Cannot create a new entry in the database", errCode=ErrorCodes.CANNOT_ADD_ENTRY_TO_DATABASE.value, error=e)
    return "Sucessfully added entry to database."