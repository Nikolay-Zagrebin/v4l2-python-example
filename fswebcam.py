#!/usr/bin/env python3

from fcntl import ioctl
import v4l2
import cv2
import os

os.system('fswebcam  -i 0 -d v4l2:/dev/video0 --save /home/robot/test.jpg')
test = cv2.imread('/home/robot/test.jpg')
test1 = cv2.resize(test, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
cv2.imwrite('/home/robot/test1.jpg', test1)
