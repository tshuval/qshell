import uuid
import datetime
import threading


class Session(threading.local):
    """A thread-local storage for the client"""
    def start(self):
        self._id = str(uuid.uuid4())
        self._started = datetime.datetime.utcnow()

session = Session()
