import time
import threading
import config
from capture import frame_collections
from lol_api import api
from video import after_death
from buffer import Buffer

buffer_ = Buffer(config.FPS * config.SECOND) 
#thread
flag = threading.Event() #bayrak inik
    
if __name__ == "__main__":
    thread1 = threading.Thread(target=frame_collections, args=(config.FPS, config.RESOLUTION, config.JPEG_QUALITY, flag, buffer_))
    thread2 = threading.Thread(target=api, args=(config.FPS, config.RESOLUTION, config.LOL_LOCAL_URL, config.AFTER_DEATH_SECOND, after_death, flag, buffer_))
    thread1.start()
    thread2.start()
    try:
        while True: time.sleep(1)
    except KeyboardInterrupt:
        flag.set()
        thread1.join()
        thread2.join()
        print("Program Kapatıldı")