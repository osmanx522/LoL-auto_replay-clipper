import os
import time
import cv2
import clipper.config as config
from datetime import datetime
def save_mp4(event_name, frame_list):
    os.makedirs(config.CLIP_DIR, exist_ok=True)


    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    zaman = datetime.now().strftime("%Y_%m_%d_%H%M%S_%f")
    out = cv2.VideoWriter(os.path.join(config.CLIP_DIR, f"LOL[{event_name}]-{zaman}.mp4"), fourcc, config.FPS, config.RESOLUTION)
    
    for frame in frame_list:
        frame_open = cv2.imdecode(frame, cv2.IMREAD_COLOR)
        out.write(frame_open)
    out.release()

def video_creator(event_type, buffer):
    time.sleep(config.AFTER_EVENT_SECOND)
    copy = buffer.copied()
    save_mp4(event_type, copy)
