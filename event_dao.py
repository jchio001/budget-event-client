from sqlalchemy.exc import IntegrityError


class EventDao:

    def __init__(self, session):
        self.session = session

    def store_record(self, event_record):
        try:
            self.session\
                .add(event_record)\

            self.session.commit()
            return True
        except IntegrityError as e:
            return False

    def store_invalid_events(self, events):
        self.session\
            .bulk_save_objects(events)\
            .commit()
