__author__ = 'ToothlessRebel'
from threading import Thread, Event


class StoppableThread(Thread):
    def __init__(self):
        super(StoppableThread, self).__init__()
        self._stop = Event()

    def stop(self):
        self._stop.set()

    def stopped(self):
        return self._stop.is_set()