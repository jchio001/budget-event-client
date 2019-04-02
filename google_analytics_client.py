import os
import requests

ANALYTICS_URL = 'https://www.google-analytics.com/collect'


class GoogleAnalyticsClient:

    def __init__(self, tracking_id=os.environ['event_tracking_id']):
        if not tracking_id:
            raise ValueError('Tracking id must be provided!')

        self.base_event_payload = 'v=1&tid=%s&cid=73&t=event&event&ec=pizza&ea=pizza' % tracking_id

    def send_events(self, event_list, user_agent):
        print event_list
        events_payload = ''
        for event in event_list:
            events_payload += self.base_event_payload

        print events_payload
        if events_payload:
            response = requests.post(url=ANALYTICS_URL, data=events_payload, headers={'User-Agent': user_agent})
            print response.status_code