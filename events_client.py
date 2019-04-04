from event_dao import EventDao
from event_utils import get_missing_fields_for_event
from google_analytics_client import GoogleAnalyticsClient
from models import EventRecord, InvalidEventRecord, session


class EventsClient:

    def __init__(self,
                 google_analytics_client=GoogleAnalyticsClient(),
                 event_dao=EventDao(session=session)):
        self.google_analytics_client = google_analytics_client
        self.event_dao = event_dao

    def send_events(self, event_list, user_agent):
        invalid_db_event_list = []
        valid_event_list = []

        for event in event_list:
            missing_fields = get_missing_fields_for_event(event)
            if missing_fields:
                if 'client_id' not in missing_fields \
                        and 'local_id' not in missing_fields \
                        and self.event_dao.store_record(EventRecord.from_dict(event)):
                    invalid_db_event_list.append(
                        InvalidEventRecord.from_dict(
                            event_dict=event,
                            invalid_reason="Missing fields: %s" % missing_fields,
                            user_agent=user_agent))
            else:
                if self.event_dao.store_record(EventRecord.from_dict(event)):
                    valid_event_list.append(event)

        if valid_event_list:
            self.google_analytics_client.send_events(event_list=valid_event_list, user_agent=user_agent)

        if invalid_db_event_list:
            self.event_dao.store_invalid_events(invalid_db_event_list)

        return list(map(lambda e: e.get('local_id'), valid_event_list))
