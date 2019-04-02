import os
import requests

from event_utils import required_fields_dict

ANALYTICS_URL = 'https://www.google-analytics.com/collect'


class GoogleAnalyticsClient:

    def __init__(self, tracking_id=os.environ['event_tracking_id']):
        if not tracking_id:
            raise ValueError('Tracking id must be provided!')

        self.base_event_payload = 'v=1&tid=%s&t=event' % tracking_id

    def send_events(self, event_list, user_agent):
        events_payload = ''
        for event in event_list:
            event_payload = self.base_event_payload

            for key, value in event.iteritems():

                event_payload += '&%s=%s' \
                                 % (required_fields_dict[key] if key in required_fields_dict else key, str(value))

            events_payload += (event_payload + '\n')

        if events_payload:
            response = requests.post(url=ANALYTICS_URL, data=events_payload[:-1], headers={'User-Agent': user_agent})
            print response.status_code
