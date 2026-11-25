import threading
from collections import deque

class Buffer():
    def __init__(self, _maxlen):
        self.deque = deque(maxlen= _maxlen)
        self.lock = threading.Lock()

    def added(self, frame):
        with self.lock:
            self.deque.append(frame)
    def copied(self):
        with self.lock:
            copy = self.deque.copy()
        return copy
    def __len__(self):
        return len(self.deque)