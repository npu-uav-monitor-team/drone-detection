from main import VideoStreamProcessor, VideoFrameProcessor
from core import Core
import cv2
import time
import threading

class DroneDetector:
    def __init__(self):
        self.core = Core()
        self.model = self.core.get_model()
        self.core.set_model(self.model)
        
    def detect_and_draw(self, frame):
        """检测目标并在图像上绘制结果"""
        try:
            # 预处理图像并进行检测
            processed_image, scale = self.core.pre_process_image(frame)
            boxes, scores, labels = self.core.predict_with_graph_loaded_model(
                processed_image, scale
            )
            
            # 在图像上绘制检测结果
            if boxes is not None and len(boxes) > 0:
                frame = self.core.draw_boxes_in_image(frame, boxes, scores)
                
            return frame, (boxes, scores, labels)
            
        except Exception as e:
            print(f"检测过程发生错误: {e}")
            return frame, None

class VideoHandler:
    def __init__(self, source):
        """初始化视频处理器"""
        self.vsp = VideoStreamProcessor(url=source, queue_size=100)
        self.vfp = VideoFrameProcessor()
        self.detector = DroneDetector()
        self.is_running = False
        
    def process_frames(self):
        """处理视频帧"""
        self.is_running = True
        frame_count = 0
        
        while self.is_running:
            # 读取并处理帧
            if not self.vsp.read_frame():
                print("无法读取视频帧")
                break
                
            frame = self.vsp.get_frame()
            
            # 目标检测
            frame, detections = self.detector.detect_and_draw(frame)
            
            # 添加帧计数
            frame = self.vfp.write_number(frame)
            
            # 显示结果
            cv2.imshow('Drone Detection', frame)
            
            # 打印检测信息
            if detections:
                boxes, scores, labels = detections
                if boxes is not None:
                    print(f"Frame {frame_count} - Detected {len(boxes)} objects")
            
            frame_count += 1
            
            # 检查退出条件
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            
            time.sleep(0.1)
        
        cv2.destroyAllWindows()

def main():
    # 设置视频源
    source = "drone.mp4"  # 使用视频文件
    # source = "rtsp://127.0.0.1:554/easy.mp4"  # 或使用RTSP流
    
    print("初始化视频处理器...")
    video_handler = VideoHandler(source)
    
    try:
        print("开始处理视频流...")
        # 创建并启动处理线程
        process_thread = threading.Thread(
            target=video_handler.process_frames
        )
        process_thread.start()
        
        # 等待用户输入来停止处理
        input("按回车键停止处理...\n")
        video_handler.is_running = False
        process_thread.join()
        
    except KeyboardInterrupt:
        print("\n检测到键盘中断...")
        video_handler.is_running = False
        process_thread.join()
    
    print("视频处理已结束")

if __name__ == "__main__":
    main()
# from main import VideoStreamProcessor, VideoFrameProcessor
# from core import Core
# import cv2
# import time
# import threading

# class DroneEvaluator:
#     def __init__(self):
#         self.core = Core()
#         self.model = self.core.get_model()
#         self.core.set_model(self.model)
    
#     def evaluate_frame(self, frame):
#         """处理单帧图像并返回检测结果"""
#         try:
#             drawing_image = self.core.get_drawing_image(frame)
#             processed_image, scale = self.core.pre_process_image(frame)
            
#             boxes, scores, labels = self.core.predict_with_graph_loaded_model(
#                 processed_image, scale
#             )
            
#             result_image = self.core.draw_boxes_in_image(drawing_image, boxes, scores)
#             return result_image, (boxes, scores, labels)
            
#         except Exception as e:
#             print(f"评估帧时发生错误: {e}")
#             return frame, None

# class DroneDetector:
#     def __init__(self):
#         self.evaluator = DroneEvaluator()
        
#     def detect_and_draw(self, frame):
#         """检测目标并在图像上绘制结果"""
#         return self.evaluator.evaluate_frame(frame)

# class VideoHandler:
#     def __init__(self, source):
#         """初始化视频处理器"""
#         self.vsp = VideoStreamProcessor(url=source, queue_size=100)
#         self.vfp = VideoFrameProcessor()
#         self.detector = DroneDetector()
#         self.is_running = False
#         self.detection_results = []  # 存储检测结果
        
#     def get_detection_results(self):
#         """获取检测结果"""
#         return self.detection_results
        
#     def process_frames(self):
#         """处理视频帧"""
#         self.is_running = True
#         frame_count = 0
        
#         while self.is_running:
#             # 读取并处理帧
#             if not self.vsp.read_frame():
#                 print("无法读取视频帧")
#                 break
                
#             frame = self.vsp.get_frame()
            
#             # 目标检测
#             frame, detections = self.detector.detect_and_draw(frame)
            
#             # 添加帧计数
#             frame = self.vfp.write_number(frame)
            
#             # 显示结果
#             cv2.imshow('Drone Detection', frame)
            
#             # 打印检测信息
#             if detections:
#                 boxes, scores, labels = detections
#                 if boxes is not None:
#                     self.detection_results.append({
#                         'frame': frame_count,
#                         'boxes': boxes.tolist(),
#                         'scores': scores.tolist(),
#                         'labels': labels.tolist() if labels is not None else None
#                     })
            
#             frame_count += 1
            
#             # 检查退出条件
#             if cv2.waitKey(1) & 0xFF == ord('q'):
#                 break
            
#             time.sleep(0.1)
        
#         cv2.destroyAllWindows()

# class DroneDetectionAPI:
#     def __init__(self, video_source):
#         self.video_handler = VideoHandler(video_source)
#         self.process_thread = None
        
#     def start_detection(self):
#         """开始检测"""
#         self.process_thread = threading.Thread(
#             target=self.video_handler.process_frames
#         )
#         self.process_thread.start()
        
#     def stop_detection(self):
#         """停止检测"""
#         self.video_handler.is_running = False
#         if self.process_thread:
#             self.process_thread.join()
            
#     def get_results(self):
#         """获取检测结果"""
#         return self.video_handler.get_detection_results()

# def main():
#     # 设置视频源
#     source = "drone.mp4"  # 使用视频文件
#     # source = "rtsp://127.0.0.1:554/easy.mp4"  # 或使用RTSP流
    
#     print("初始化视频处理器...")
#     video_handler = VideoHandler(source)
    
#     try:
#         print("开始处理视频流...")
#         # 创建并启动处理线程
#         process_thread = threading.Thread(
#             target=video_handler.process_frames
#         )
#         process_thread.start()
        
#         # 等待用户输入来停止处理
#         input("按回车键停止处理...\n")
#         video_handler.is_running = False
#         process_thread.join()
        
#     except KeyboardInterrupt:
#         print("\n检测到键盘中断...")
#         video_handler.is_running = False
#         process_thread.join()
    
#     print("视频处理已结束")

# if __name__ == "__main__":
#     main()