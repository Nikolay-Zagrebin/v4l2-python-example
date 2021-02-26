#!/usr/bin/env python3

# ffmpeg -y -pix_fmt bgr0 -f avfoundation -r 20 -t 10 -i 1 -vf scale=w=3840:h=2160 -f rawvideo /dev/null

import sys
import cv2
import time
import subprocess
import numpy as np

w,h = 3840, 2160

def ffmpegGrab():
    """Generator to read frames from ffmpeg subprocess"""
    cmd = [
        'ffmpeg',
        '-pix_fmt', 'bgr0',
        '-f', 'avfoundation',
        '-capture_cursor', '1',
        '-capture_mouse_clicks', '1',
        '-r', '20',
        '-i', '1',
        '-vf','scale=w=3840:h=2160',
        '-f', 'rawvideo',
        'pipe:1'
    ]
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    while True:
        frame = proc.stdout.read(w*h*4)
        yield np.frombuffer(frame, dtype=np.uint8).reshape((h,w,4))

# Get frame generator
gen = ffmpegGrab()

# Get start time
start = time.time()

# Read video frames from ffmpeg in loop
nFrames = 0
while True:
    # Read next frame from ffmpeg
    frame = next(gen)
    nFrames += 1
    frame = cv2.resize(frame,(960,540))

    cv2.imshow('screenshot', frame)

    if cv2.waitKey(1) == ord("q"):
        break

    fps = nFrames/(time.time()-start)
    print(f'FPS: {fps}')


cv2.destroyAllWindows()
out.release()
