#!/usr/bin/env python3

from fcntl import ioctl
import v4l2
import cv2
import numpy as np
import mmap

#   1. Initializing the device
fd = open('/dev/video0', 'rb+', buffering=0)
fmt = v4l2.v4l2_format()    
fmt.type = v4l2.V4L2_BUF_TYPE_VIDEO_CAPTURE
#fmt.fmt.pix.width = 356
#fmt.fmt.pix.height = 292
#fmt.fmt.pix.pixelformat = v4l2.V4L2_PIX_FMT_SGRBG8
ioctl(fd, v4l2.VIDIOC_G_FMT, fmt)
ioctl(fd, v4l2.VIDIOC_S_FMT, fmt)
        
#   2. Requesting a buffer
req = v4l2.v4l2_requestbuffers()      
req.count = 1
req.type = v4l2.V4L2_BUF_TYPE_VIDEO_CAPTURE
req.memory = v4l2.V4L2_MEMORY_MMAP
ioctl(fd, v4l2.VIDIOC_REQBUFS, req)

#   3. Do the memory mapping
buf = v4l2.v4l2_buffer()
buf.type = v4l2.V4L2_BUF_TYPE_VIDEO_CAPTURE
buf.memory = v4l2.V4L2_MEMORY_MMAP
buf.index = 0           
ioctl(fd, v4l2.VIDIOC_QUERYBUF, buf)

mm = mmap.mmap(fd.fileno(), buf.length, mmap.MAP_SHARED, mmap.PROT_READ | mmap.PROT_WRITE, offset=buf.m.offset)
ioctl(fd, v4l2.VIDIOC_QBUF, buf)

#   4. Tell the camera to start streaming
buf_type = v4l2.v4l2_buf_type(v4l2.V4L2_BUF_TYPE_VIDEO_CAPTURE)
ioctl(fd, v4l2.VIDIOC_STREAMON, buf_type)

#   5. Capture image
buf_ = v4l2.v4l2_buffer()
buf_.type = v4l2.V4L2_BUF_TYPE_VIDEO_CAPTURE
buf_.memory = v4l2.V4L2_MEMORY_MMAP
ioctl(fd, v4l2.VIDIOC_DQBUF, buf_)

frame = np.frombuffer(mm, dtype=np.uint8).reshape(fmt.fmt.pix.height, fmt.fmt.pix.width, 2)
frame = cv2.cvtColor(frame, cv2.COLOR_YUV2GRAY_YUY2)

#data = mm.read(buf.bytesused)
#raw_data = open("frame.bin", "wb")
#raw_data.write(data)

mm.seek(0)
ioctl(fd, v4l2.VIDIOC_STREAMOFF, buf_type)
raw_data.close()
fd.close()

#image = cv2.imdecode(np.fromstring(data, dtype=np.uint8), cv2.IMREAD_COLOR)
#cv2.imwrite("image.jpg", image)
