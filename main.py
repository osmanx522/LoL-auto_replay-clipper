import time
import threading
import config
from capture import frame_collections
from lol_api import api
from video import after_death
from collections import deque

d = deque(maxlen=config.FPS * config.SECOND)
#thread
lock = threading.Lock()
flag = threading.Event() #bayrak inik
    
if __name__ == "__main__":
    thread1 = threading.Thread(target=frame_collections, args=(config.FPS, config.RESOLUTION, config.JPEG_QUALITY, d, lock, flag))
    thread2 = threading.Thread(target=api, args=(config.FPS, config.RESOLUTION, config.LOL_LOCAL_URL, config.AFTER_DEATH_SECOND, after_death, d, lock, flag))
    thread1.start()
    thread2.start()
    try:
        while True: time.sleep(1)
    except KeyboardInterrupt:
        flag.set()
        thread1.join()
        thread2.join()
        print("Program Kapatıldı")