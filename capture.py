import mss
import cv2
import time
import numpy as np
import config 

def frame_capture(sct, resolution):
    sct: mss.MSS # Tip belirtici
    ana_ekran = sct.monitors[1]
    screenshot = sct.grab(ana_ekran)
    screenshot_array = np.array(screenshot)
    bgr_color_array = screenshot_array[:, :, :3]
    resize_screenshot = cv2.resize(bgr_color_array, resolution, interpolation=cv2.INTER_AREA)
    return resize_screenshot

def frame_collections(flag, buffer): # ekran görüntüsünü sıra sıra çeker ve kuyruğa ekler
    with mss.MSS() as sct:
        elapsed_time = time.perf_counter()
        frame_count = 0
        while not flag.is_set():
            t0 = time.perf_counter()
            frame = frame_capture(sct, config.RESOLUTION)
            ok, paket = cv2.imencode(".jpg", frame, [cv2.IMWRITE_JPEG_QUALITY, config.JPEG_QUALITY])
            buffer.added(paket)
            frame_count +=1
            if time.perf_counter() - elapsed_time >= 1:
                print(f"FPS:{frame_count} | TargetFPS:{config.FPS} | Queue:{len(buffer)}")
                frame_count = 0
                elapsed_time = time.perf_counter()
            t_difference = time.perf_counter() - t0
            t_wait = (1/config.FPS) - t_difference
            if t_wait > 0:
                time.sleep(t_wait)