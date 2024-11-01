from core import Core





c = Core()

image_filename = c.current_path + "/DataSets/Drones/testImages/360.jpg"
image = c.load_image_by_path(image_filename)

drawing_image = c.get_drawing_image(image)

processed_image, scale = c.pre_process_image(image)

c.set_model(c.get_model())
boxes, scores, labels = c.predict_with_graph_loaded_model(processed_image, scale)

detections = c.draw_boxes_in_image(drawing_image, boxes, scores)

c.visualize(drawing_image)

# from core import Core
# import cv2

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
