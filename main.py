'''
@author: weiyu
@date:2024/10/28
@Desc: class VideoStreamProcessor:
class VideoFrameProcessor
'''

import cv2
import asyncio
import time
import queue
# from PyGObject import gstreamer
# import gi

class VideoStreamProcessor:
    def __init__(self, url, queue_size):
        self.__url = url
        self.__cap = cv2.VideoCapture(self.__url)
        self.__frames = queue.Queue(queue_size)
        self.__queue_size = queue_size

    def read_frame(self):
        start = time.time()
        ret, frame = self.__cap.read()
        self.__frames.put(frame)
        end = time.time()
        print(f"Read Frame Time: {end - start}")
        return ret

    def get_frame(self):
        start = time.time()
        frame = self.__frames.get()
        end = time.time()
        print(f"Get Frame Time: {end - start}")
        return frame


class VideoFrameProcessor:
    def __init__(self):
        self.__count = 0
    def write_number(self, frame):
        start = time.time()
        frame = cv2.putText(frame, '{}'.format(self.__count), (10, 30), cv2.FONT_HERSHEY_PLAIN, 10, (255, 255, 255), 2)
        self.__count += 1
        end = time.time()
        print(f"Write Number Time: {end - start}")
        return frame


def read_frame(vsp :VideoStreamProcessor, vfps :VideoFrameProcessor):
    while True:
        vsp.read_frame()
        frame = vsp.get_frame()
        frame = vfp.write_number(frame)
        cv2.imshow('frame', frame)
        time.sleep(0.1)


def main(vsp :VideoStreamProcessor, vfp :VideoFrameProcessor):
    read_frame(vsp, vfp)

if __name__ == '__main__':
    print(f"Starting Processing Video...")
    vsp = VideoStreamProcessor(url="rtsp://127.0.0.1:554/easy.mp4", queue_size=1000)
    vfp = VideoFrameProcessor()

    main(vsp, vfp)




