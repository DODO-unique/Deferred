from Utility.pypolice.master_validator import UserName
from Touch.orm_schema import Users
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from Utility.ErrorHandler import initiate_error_handler, ErrorCodes
from uuid import UUID

URL = "postgresql+asyncpg://victor:yomama@localhost:5506/deferred"
engine = create_async_engine(URL)

async def fetch_line(uname: UserName) -> Users | None:
    '''
    expects verified username. Returns the object.
    '''
    try:
        async with AsyncSession(engine) as session:
            stmt = select(Users).where(Users.uname == uname.value)
            line_object = await session.execute(stmt)
            return line_object.scalar_one_or_none()
    except Exception as e:
        initiate_error_handler(message="could not fetch user", errCode=ErrorCodes.BROAD_DATABASE_ERROR.value, error=e)

async def new_session(session_token: UUID, user: Users) -> bool | None:
    try:
        async with AsyncSession(engine) as session:
            new_session_entry = Users(token = session_token, user_id = user)
            session.add(new_session_entry)
            await session.commit()
            return True
    except Exception as e:
        initiate_error_handler(message="could not create session", errCode=ErrorCodes.BROAD_DATABASE_ERROR.value, error=e)