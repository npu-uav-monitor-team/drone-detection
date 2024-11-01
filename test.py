import cv2
import asyncio
import time
import queue
import subprocess
import os
from core import Core

c = Core()


class VideoStreamProcessor:
    def __del__(self):
        self.__cap.release()

    def __init__(self, url, queue_size):
        self.__url = url
        self.__cap = cv2.VideoCapture(self.__url)
        self.__frames = queue.Queue(queue_size)
        self.__queue_size = queue_size
        self.__frame_width = int(self.__cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.__frame_height = int(self.__cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.__fps = self.__cap.get(cv2.CAP_PROP_FPS)

    def get_properties(self):
        return self.__fps, self.__frame_width, self.__frame_height

    def read_frame(self):
        start = time.time()
        ret, frame = self.__cap.read()
        # self.__frames.put(frame)
        end = time.time()
        print(f"Read Frame Time: {end - start}")
        return ret, frame


class VideoFrameProcessor:
    def __del__(self):
        self.__proc.stdin.close()
        self.__proc.wait()

    def __init__(self, fps, width, height):
        self.__count = 0
        self.__ffmpeg_cmd = [
            'ffmpeg',
            '-y',
            '-f', 'rawvideo',
            '-vcodec', 'rawvideo',
            "-codec", "rawvideo",
            '-pix_fmt', 'bgr24',
            '-s', f'{width}x{height}',
            '-r', '30',
            '-i', '-',
            '-c:v', 'libx264',
            '-pix_fmt', 'yuv420p',
            '-preset', 'ultrafast',
            '-f', 'rtsp',
            "-muxdelay", "0.1",
            'rtsp://192.168.10.90:8554/easy'
            # 'ffmpeg',
            # '-y',
            # '-pix_fmt', 'bgr24',
            # '-s', f'{width}x{height}',
            # '-r', f'{fps}',
            # '-i', 'drone.mp4',  # 指定输入文件路径
            # '-c:v', 'libx264',
            # '-pix_fmt', 'yuv420p',
            # '-preset', 'ultrafast',
            # '-f', 'rtsp',
            # '-muxdelay', '0.1',
            # 'rtsp://127.0.0.1:8554/easy.live'
        ]
        self.__proc = subprocess.Popen(self.__ffmpeg_cmd, stdin=subprocess.PIPE)

    def write_frame(self, frame):
        drawing_image = c.get_drawing_image(frame)

        processed_image, scale = c.pre_process_image(frame)

        c.set_model(c.get_model())
        boxes, scores, labels = c.predict_with_graph_loaded_model(processed_image, scale)

        c.draw_boxes_in_image(drawing_image, boxes, scores)
        self.__count += 1
        print(f"Read Frame No: {self.__count}")

        # # 保存带有识别框的图像
        # output_dir = 'output_images'
        # os.makedirs(output_dir, exist_ok=True)
        # output_path = os.path.join(output_dir, f'frame_{self.__count}.jpg')
        # cv2.imwrite(output_path, drawing_image)
        # print(f"Saved image: {output_path}")

        frame = drawing_image
        start = time.time()
        # frame = cv2.putText(frame, '{}'.format(self.__count), (10, 30), cv2.FONT_HERSHEY_PLAIN, 10, (255, 255, 255), 2)
        # self.__count += 1
        self.__proc.stdin.write(bytes(frame))
        end = time.time()
        print(f"Write Number Time: {end - start}")
        return frame


def read_frame(vsp: VideoStreamProcessor, vfps: VideoFrameProcessor):
    while True:
        ret, frame = vsp.read_frame()
        if not ret:
            break
        vfp.write_frame(frame)
        # cv2.imshow('frame', frame)
        # time.sleep(1)


def main(vsp: VideoStreamProcessor, vfp: VideoFrameProcessor):
    read_frame(vsp, vfp)


if __name__ == '__main__':
    print(f"Starting Processing Video...")

    # 使用本地视频文件进行测试
    # vsp = VideoStreamProcessor(url="drone.mp4", queue_size=1000)

    vsp = VideoStreamProcessor(url="rtsp://192.168.10.2:554/ch1", queue_size=1000)
    fps, width, height = vsp.get_properties()
    vfp = VideoFrameProcessor(fps, width, height)

    main(vsp, vfp)
