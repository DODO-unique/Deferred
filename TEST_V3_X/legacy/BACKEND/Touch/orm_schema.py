'''
this is where we keep our base table structure (s)
These are not created, they are just stored
'''

from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import Column, Text, TIMESTAMP
from sqlalchemy.dialects.postgresql import UUID, ENUM


class Base(DeclarativeBase):
    pass

enum_status = ENUM('pending', 'sent', 'failed', name='enum_status')

class ScheduledMessages(Base):
    __tablename__ = "scheduled_messages"

    id = Column(UUID(as_uuid=True), primary_key=True, server_default="uuid7()")
    email = Column(Text, nullable=False)
    prompt = Column(Text, nullable=False)
    execute_at = Column(TIMESTAMP(timezone=True), nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default="now()")
    job_status = Column(Text, nullable=False, default='pending')
    # OR job_status = Column(Text, nullable=False, server_default="'pending::enum_status")

