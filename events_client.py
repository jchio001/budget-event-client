from event_dao import EventDao
from event_utils import get_missing_fields_for_event
from google_analytics_client import GoogleAnalyticsClient
from models import InvalidDbEvent, session


class EventsClient:

    def __init__(self,
                 google_analytics_client=GoogleAnalyticsClient(),
                 event_dao=EventDao(session=session)):
        self.google_analytics_client = google_analytics_client
        self.event_dao = event_dao

    def send_events(self, event_list, user_agent):
        invalid_event_list = []
        valid_event_list = []

        for event in event_list:
            missing_fields = get_missing_fields_for_event(event)
            if missing_fields:
                print "Missing fields: %s" % missing_fields
                invalid_event_list.append(invalid_event_list)
            else:
                valid_event_list.append(event)

        if valid_event_list:
            self.google_analytics_client.send_events(event_list=valid_event_list, user_agent=user_agent)

        if invalid_event_list:
            self.event_dao.store_invalid_events(
                list(map(
                    lambda e: InvalidDbEvent.from_dict(event_dict=e, user_agent=user_agent),
                    invalid_event_list)))
