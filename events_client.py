from google_analytics_client import GoogleAnalyticsClient

class EventClient:

    def __init__(self, google_analytics_client = GoogleAnalyticsClient()):
        self.google_analytics_client = google_analytics_client

    def send_events(self, event_list, user_agent):
        print user_agent
        self.google_analytics_client.send_events(event_list=event_list, user_agent=user_agent)
