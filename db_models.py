from sqlalchemy import Column, Integer, String, ForeignKey, Table, DateTime, create_engine
from sqlalchemy.orm import relationship, backref, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

import datetime as dt
import os
file_path = os.path.dirname(os.path.abspath(__file__))

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
    message_id = Column(String)


class Message(Base):
    __tablename__ = "message"
    message_id = Column(String, primary_key=True)
    message = Column(String)
    time_created = Column(DateTime)
    stream_id = Column(String)


def add_stream(session, stream_id, user_name, viewer_count, user_id, game_name, title, started_at):
    # Check if stream exists
    stream = (session.query(Stream).filter(Stream.stream_id) == stream_id)
    if stream is not None:
        return
    # stream = (session.query(Stream).filter(Stream.stream_id) == stream_id).one_or_none()
    # create a new stream if it doesn't exist
    if stream is None:
        stream = Stream(stream_id=stream_id, user_name=user_name, viewer_count=viewer_count,
                        user_id=user_id, game_name=game_name, title=title, started_at=started_at)
    session.add(stream)

    session.commit()


def main():
    # Connect to the database using SQLAlchemy
    db = os.path.join(file_path, "stream_data.db")
    engine = create_engine(f"sqlite:///{db}")
    Session = sessionmaker()
    Session.configure(bind=engine)
    session = Session()


    """add_stream(session=session, stream_id=23, user_name="zoo", viewer_count=45000, user_id=12, game_name="apex legends",
               title="Stream", started_at=dt.datetime.now())"""

    session.add(Stream(stream_id=25, user_name="zoo", viewer_count=45000, user_id=12, game_name="apex legends",
                       title="Stream", started_at=dt.datetime.now()))
    session.commit()
    print(session.query(Stream).all())


main()
