# # screen_segmentation.py
# import cv2

# def segment_screen(frame, num_sections=8):
#     height, width, _ = frame.shape
#     section_width = width // num_sections
#     for i in range(1, num_sections):
#         cv2.line(frame, (i * section_width, 0), (i * section_width, height), (255, 0, 0), 2)
#     return frame
