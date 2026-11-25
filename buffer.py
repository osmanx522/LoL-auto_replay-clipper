import threading
from collections import deque

class Buffer():
    def __init__(self, _maxlen):
        self.deque = deque(maxlen= _maxlen)
        self.lock = threading.Lock()
