from sqlalchemy import BigInteger, Column, create_engine, String, UniqueConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import func

import json
import os

db_url = os.environ['events_db_url']
db = create_engine('')
base = declarative_base()


class DbEvent(base):
    __tablename__ = 'event'
    __table_args__ = (
        UniqueConstraint('client_id', 'local_id', name='unique_client_id_and_local_id_constraint')
    )

    # This is going to be a UUID generated on the client's side.
    client_id = Column(String, nullable=False)

    # This is going to a local id used to uniquely identify an event on the client side. This combined with the UUID
    # will be used to prevent duplicate events from being resent.
    local_id = Column(String, nullable=False)

    # The time at which an event is created on the client.
    client_creation_time = Column(BigInteger, nullable=False)

    # The time at which an event is inserted into the client.
    db_insertion_time = Column(BigInteger, server_default=func.now().timestamp(), nullable=False)

    # The time at which an event has successfully been uploaded to Google Analytics.
    upload_time = Column(BigInteger, nullable=True)

    # All the other fields attached to an event that we don't really want to query on.
    body = Column(String, nullable=False)

    @staticmethod
    def from_dict(event_dict):
        db_event = DbEvent()

        db_event.client_id = event_dict.get('client_id')
        db_event.local_id = event_dict.get('local_id')
        db_event.creation_time = event_dict.get('creation_time')

        event_dict.pop('client_id', None)
        event_dict.pop('local_id', None)
        event_dict.pop('creation_time', None)

        db_event.body = json.dumps(event_dict)

        return db_event


# Sets up a sqlalchemy session
Session = sessionmaker(db)
session = Session()

# This allows you to run models.py to create the tables!
if __name__ == "__main__":
    base.metadata.create_all(db)