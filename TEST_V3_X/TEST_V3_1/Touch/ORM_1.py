from Utility.ErrorHandler import ErrorCodes, initiate_error_handler
from Utility.pypolice.payload_validator import UserName, Mail
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from orm_schema import Users
from sqlalchemy import select, Column
from sqlalchemy.exc import MultipleResultsFound

URL = "postgresql+asyncpg://victor:yomama@localhost:5506/deferred"

engine = create_async_engine(URL)

async def check_user_exists(field: Column[str], value: UserName | Mail) -> bool: #type: ignore
    try:
        async with AsyncSession(engine) as session:
                stmt = select(Users).where(field == value)
                result = await session.execute(stmt)
                is_taken = result.scalar_one_or_none() is not None
                return is_taken
    except MultipleResultsFound as e:
        initiate_error_handler(message="FATAL: Multiple entries of unique field found with the same username. Check DB integrity.", errCode=ErrorCodes.UNEXPECTED_DUPLICATE_ENTRY.value, error=e)
    except Exception as e:
        initiate_error_handler(message="Server error while checking username and email availability.", errCode=ErrorCodes.BROAD_DATABASE_ERROR.value, error=e, traceback=True)
    