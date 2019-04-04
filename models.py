from datetime import datetime
from sqlalchemy import BigInteger, Column, create_engine, String, PrimaryKeyConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

import json
import os

db_url = os.environ['events_db_url']
db = create_engine(db_url)
base = declarative_base()


# This table exists to prevent redundant events from being uploaded.
class EventRecord(base):
    __tablename__ = 'event_record'
    __table_args__ = (
        PrimaryKeyConstraint('client_id', 'local_id', name='eventrecord_unique_client_id_and_local_id_constraint'),
    )

    # This is going to be a UUID generated on the client's side.
    client_id = Column(String, nullable=False, index=True)

    # This is going to a local id used to uniquely identify an event on the client side. This combined with the UUID
    # will be used to prevent duplicate events from being resent.
    local_id = Column(String, nullable=False, index=True)

    @staticmethod
    def from_dict(event_dict):
        event_record = EventRecord()
        event_record.client_id = event_dict.get('client_id')
        event_record.local_id = event_dict.get('local_id')
        return event_record


class InvalidEventRecord(base):
    __tablename__ = 'invalid_event_record'
    __table_args__ = (
        PrimaryKeyConstraint('client_id', 'local_id', name='invaliddbevent_unique_client_id_and_local_id_constraint'),
    )

    # This is going to be a UUID generated on the client's side.
    client_id = Column(String, nullable=False, index=True)

    # This is going to a local id used to uniquely identify an event on the client side. This combined with the UUID
    # will be used to prevent duplicate events from being resent.
    local_id = Column(String, nullable=False, index=True)

    # User-Agent header from the request.
    user_agent = Column(String, nullable=False, index=True)

    # The time at which an event is created on the client.
    client_creation_time = Column(BigInteger, nullable=False, index=True)

    # The time at which an event is inserted into the database.
    db_insertion_time = Column(BigInteger, default=datetime.now(), nullable=False, index=True)

    # All the other fields attached to an event that we don't really want to query on.
    body = Column(String, nullable=False)

    invalid_reason = Column(String, nullable=False)

    @staticmethod
    def from_dict(event_dict, invalid_reason, user_agent):
        db_event = InvalidEventRecord()

        db_event.client_id = event_dict.get('client_id')
        db_event.local_id = event_dict.get('local_id')
        db_event.creation_time = event_dict.get('creation_time')
        db_event.user_agent = user_agent
        db_event.invalid_reason = invalid_reason

        event_dict_copy = event_dict.copy()
        event_dict_copy.pop('client_id', None)
        event_dict_copy.pop('local_id', None)
        event_dict_copy.pop('creation_time', None)

        db_event.body = json.dumps(event_dict_copy)

        return db_event


# Sets up a sqlalchemy session
Session = sessionmaker(db)
session = Session()

# This allows you to run models.py to create the tables!
if __name__ == "__main__":
    base.metadata.create_all(db)