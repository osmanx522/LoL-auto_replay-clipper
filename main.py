import time
import threading
import config
from capture import frame_collections
from lol_api import api
from video import video_creator
from buffer import Buffer

buffer_ = Buffer(config.FPS * config.SECOND) 
#thread
flag = threading.Event() #bayrak inik

def api_works(event_type):
    threading.Thread(target=video_creator, args=(event_type, buffer_), daemon=True).start()

if __name__ == "__main__":
    thread1 = threading.Thread(target=frame_collections, args=(flag, buffer_))
    thread2 = threading.Thread(target=api, args=(flag, api_works))
    thread1.start()
    thread2.start()
    try:
        while True: time.sleep(1)
    except KeyboardInterrupt:
        flag.set()
        thread1.join()
        thread2.join()
        print("Program Kapatıldı")