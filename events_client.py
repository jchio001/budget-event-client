from event_utils import get_missing_fields_for_event
from event_dao import EventDao
from models import DbEvent, session


class EventsClient:

    def __init__(self, event_dao=EventDao(session=session)):
        self.event_dao = event_dao

    # TODO: Make user agent a field in the event model
    def send_events(self, event_list, user_agent):
        invalid_event_list = []
        valid_event_list = []

        for event in event_list:
            missing_fields = get_missing_fields_for_event(event)
            if missing_fields:
                # TODO: Store this into a database
                print "Missing fields: %s" % missing_fields
                invalid_event_list.append(invalid_event_list)
            else:
                valid_event_list.append(event)

        self.event_dao.store_events(list(map(DbEvent.from_dict, valid_event_list)))
