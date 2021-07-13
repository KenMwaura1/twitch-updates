from sqlalchemy import Column, Integer, String, ForeignKey, Table, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

stream_message = Table(
    "stream_message",
    Base.metadata,
    Column("stream_id", Integer, ForeignKey("Stream.stream_id")),
    Column("message_id", String, ForeignKey("Message.message_id"))
)


class Stream(Base):
    __tablename__ = "stream"
    stream_id = Column(Integer, primary_key=True)
    user_name = Column(String)
    viewer_count = Column(Integer)
    user_id = Column(Integer)
    game_name = Column(String)
    title = Column(String)
    started_at = Column(DateTime)
    message_id = relationship("Message", backref=backref("message")


class Message(Base):
    __tablename__ = "message"
    message_id = Column(String)
    message = Column(string)
    time_created = Column(DateTime)
    stream_id = relationship("Stream", backref=backref("stream"))

def main():
    # Connect to the database using SQLAlchemy
