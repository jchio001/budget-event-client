from events_client import EventClient
from flask import Flask, request, Response

import json

app = Flask(__name__)


# All this endpoint does is forward events to Google Analytics & stores events locally if the call fails.
@app.route('/events', methods=['POST'])
def post_events(*args, **kwargs):
    event_list = json.loads(request.data)
    EventClient().send_events(event_list=event_list, user_agent = request.headers.get('User-Agent'))
    return Response(status=200)


if __name__ == "__main__":
    app.run()