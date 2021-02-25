#!/usr/bin/env python3

from fcntl import ioctl
import v4l2
import mmap
import numpy as np
import cv2

NUM_BUFFERS = 10

#   1. Initializing the device
fd = open('/dev/video0', 'rb+', buffering=0)

fmt = v4l2.v4l2_format()    
fmt.type = v4l2.V4L2_BUF_TYPE_VIDEO_CAPTURE
ioctl(fd, v4l2.VIDIOC_G_FMT, fmt)
ioctl(fd, v4l2.VIDIOC_S_FMT, fmt)
        
#   2. Requesting a buffer
req = v4l2.v4l2_requestbuffers()      
req.count = NUM_BUFFERS
req.type = v4l2.V4L2_BUF_TYPE_VIDEO_CAPTURE
req.memory = v4l2.V4L2_MEMORY_MMAP
ioctl(fd, v4l2.VIDIOC_REQBUFS, req)

#   3. Do the memory mapping
buffers = []
for x in range(req.count):
    buf = v4l2.v4l2_buffer()
    buf.type = v4l2.V4L2_BUF_TYPE_VIDEO_CAPTURE
    buf.memory = v4l2.V4L2_MEMORY_MMAP
    buf.index = x           
    ioctl(fd, v4l2.VIDIOC_QUERYBUF, buf)
    buf.buffer = mmap.mmap(fd.fileno(), buf.length, mmap.MAP_SHARED, mmap.PROT_READ | mmap.PROT_WRITE, offset=buf.m.offset)
    buffers.append(buf)

for buf in buffers:
    ioctl(fd, v4l2.VIDIOC_QBUF, buf)

#   4. Tell the camera to start streaming
buf_type = v4l2.v4l2_buf_type(v4l2.V4L2_BUF_TYPE_VIDEO_CAPTURE)
ioctl(fd, v4l2.VIDIOC_STREAMON, buf_type)

#   5. Capture image
img = None
f = 0
while img is None:
    print("Grabbing Frame...")
    buf = buffers[f % NUM_BUFFERS]
    ioctl(fd, v4l2.VIDIOC_DQBUF, buf)
    video_buffer = buffers[buf.index].buffer
    data = video_buffer.read(buf.bytesused)
    video_buffer.seek(0)

    print("Verifing Image..")
    try:
        bayer8_image = np.frombuffer(data, dtype=np.uint8).reshape((292,356))
        img = cv2.cvtColor(bayer8_image, cv2.COLOR_BayerGR2RGB)
        cv2.imwrite('test1.jpg', img)
    except Exception as e:
        print("Invalid image:", e)

    ioctl(fd, v4l2.VIDIOC_QBUF, buf)
    f += 1



#frame = np.frombuffer(mm, dtype=np.uint8).reshape(fmt.fmt.pix.height, fmt.fmt.pix.width, 2)
#frame = cv2.cvtColor(frame, cv2.COLOR_YUV2GRAY_YUY2)

#data = mm.read(buf.bytesused)
#raw_data = open("frame.bin", "wb")
#raw_data.write(data)



#image = cv2.imdecode(np.fromstring(data, dtype=np.uint8), cv2.IMREAD_COLOR)
#cv2.imwrite("image.jpg", image)
