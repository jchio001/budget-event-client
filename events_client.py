from event_utils import get_missing_fields_for_event
from google_analytics_client import GoogleAnalyticsClient


class EventClient:

    def __init__(self, google_analytics_client=GoogleAnalyticsClient()):
        self.google_analytics_client = google_analytics_client

    def send_events(self, event_list, user_agent):
        print user_agent
        valid_event_list = []

        for event in event_list:
            missing_fields = get_missing_fields_for_event(event)
            if missing_fields:
                # TODO: Store this into a database
                print "Missing fields: %s" % missing_fields
            else:
                valid_event_list.append(event)

        self.google_analytics_client.send_events(event_list=valid_event_list, user_agent=user_agent)