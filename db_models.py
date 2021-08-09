from sqlalchemy import BigInteger, Column, Integer, String, ForeignKey, Table, DateTime, create_engine, MetaData
from sqlalchemy.orm import relationship, backref, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

import datetime as dt
import os
from dotenv import load_dotenv

load_dotenv()

file_path = os.path.dirname(os.path.abspath(__file__))

Base = declarative_base()

"""stream_message = Table(
    "stream_message",
    Base.metadata,
    Column("stream_id", Integer, ForeignKey("Stream.stream_id")),
    Column("message_id", String, ForeignKey("Message.message_id"))
)
"""


class Stream(Base):
    __tablename__ = "stream"
    stream_id = Column(BigInteger, primary_key=True)
    user_name = Column(String)
    viewer_count = Column(Integer)
    user_id = Column(Integer)
    game_name = Column(String)
    title = Column(String)
    started_at = Column(DateTime)
    message_id = Column(String)


class Message(Base):
    __tablename__ = "message"
    id = Column(Integer, primary_key=True, autoincrement=True)
    message_id = Column(String)
    message = Column(String)
    time_created = Column(DateTime)
    stream_id = Column(String)


def add_stream(session, stream_id, user_name, viewer_count, user_id, game_name, title, started_at):
    # Check if stream exists
    stream = session.query(Stream).filter(Stream.stream_id == stream_id).one_or_none()
    s = session.query(Stream).all()
    if stream is not None:
        return "Stream exists"

    # create a new stream if it doesn't exist
    if stream is None:
        stream = Stream(stream_id=stream_id, user_name=user_name, viewer_count=viewer_count,
                        user_id=user_id, game_name=game_name, title=title, started_at=started_at)
        try:
            session.add(stream)
        except Exception as e:
            print(f"Error as {e}")
            session.rollback()

    session.commit()


def add_message(session, message_id, message, time_created, stream_id):
    # Check if a message exists
    message_check = session.query(Message).filter(Message.stream_id == stream_id).one_or_none()
    s = session.query(Message).all()
    if message_check is not None:
        return "Message already exists"

    # create a new stream if it doesn't exist
    if message_check is None:
        live_message = Message(message_id=message_id, message=message, time_created=time_created, stream_id=stream_id)
        try:
            session.add(live_message)
        except Exception as e:
            session.rollback()
            print(f"Error as {e}")
    session.commit()


def check_stream(session, stream_id):
    stream = session.query(Stream).filter(Stream.stream_id == stream_id).one_or_none()
    if stream is None:
        return stream_id


def main():
    # Connect to the postgres database using SQLAlchemy
    # db = os.path.join(file_path, "stream_data.db")
    # engine = create_engine(f"sqlite:///{db}")
    postgres_username = os.getenv("postgres_username")
    postgres_password = os.getenv("postgres_password")
    postgres_db = os.getenv("postgres_db")
    postgres_host = os.getenv("postgres_host")
    engine = create_engine(
        f'postgresql+psycopg2://{postgres_username}:{postgres_password}@{postgres_host}/{postgres_db}')
    Base.metadata.create_all(engine, checkfirst=True)
    metadata = MetaData()
    Session = sessionmaker()
    Session.configure(bind=engine)
    session = Session()
    # print(session)

    return session


main()
