import cv2
import numpy as np
import matplotlib.pyplot as plt
def display_lines(image,lines):
    lines_image=np.zeros_like(image)
    if lines is not None:
        for line in lines:
            x1,y1,x2,y2=line.reshape(4)
            cv2.line(lines_image,(x1,y1),(x2,y2),(0,255,0),9)

    return lines_image