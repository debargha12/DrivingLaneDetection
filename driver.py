import cv2
import numpy as np
import matplotlib.pyplot as plt
import canny_program
import roi
import display_lines
import average_slope



cap = cv2.VideoCapture('data/sample_video.mp4 ')
while(cap.isOpened()):
    _, frame =cap.read()
    canny_image = canny_program.canny(frame)

    cropped_image = roi.region_of_interest(canny_image)
    lines = cv2.HoughLinesP(cropped_image, 2, np.pi / 180, 100, np.array([]), minLineLength=40, maxLineGap=5)
    average_lines = average_slope.average_slope_intercept(frame, lines)

    lines_image = display_lines.display_lines(frame, average_lines)
    combined = cv2.addWeighted(frame, 0.8, lines_image, 1, 1)
    cv2.imshow('result', combined)
    cv2.waitKey(1)  # displays image for specified milisecond, 0 means infinit