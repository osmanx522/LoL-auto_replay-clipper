import os
import time
import cv2

def save_mp4(frame_list, fps, resolution):
    code_dir = os.path.dirname(os.path.abspath(__file__))
    clip_dir = os.path.join(code_dir, "klipler")
    os.makedirs(clip_dir, exist_ok=True)


    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    zaman = time.strftime("%Y%m%d_%H%M%S")
    out = cv2.VideoWriter(os.path.join(clip_dir, f"LOL-{zaman}.mp4"), fourcc, fps, resolution)
    
    for frame in frame_list:
        frame_open = cv2.imdecode(frame, cv2.IMREAD_COLOR)
        out.write(frame_open)
    out.release()

def after_death(fps, resolution, frame_list, lock, after_death_second):
    time.sleep(after_death_second)
    with lock:
        list_copy = frame_list.copy()
    save_mp4(list_copy, fps, resolution)
