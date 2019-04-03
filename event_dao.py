class EventDao():

    def __init__(self, session):
        self.session = session

    def store_invalid_events(self, events):
        self.session\
            .bulk_save_objects(events)\
            .commit()
