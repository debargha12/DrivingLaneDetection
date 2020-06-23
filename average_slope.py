import cv2
import numpy as np
import matplotlib.pyplot as plt


def make_coordinates(images, line_parameters):
    slope, intercept = line_parameters
    y1= images.shape[0]
    y2=int(y1*(3/5))
    x1= int((y1-intercept)/slope)
    x2 = int((y2 - intercept) / slope)
    return np.array([x1,y1,x2,y2])

def average_slope_intercept(image, lines):
    """

    :type lines: object
    """
    left_fit, right_fit =[], []
    for line in lines:
        x1,y1,x2,y2=line.reshape(4)
        parameters = np.polyfit((x1,x2),(y1,y2),1)
        #print(parameters)
        slope= parameters[0]
        intercept = parameters[1]
        if slope<0 :
            left_fit.append((slope,intercept))
        else:
            right_fit.append((slope,intercept))
    left_fit_average = np.average(left_fit,axis=0)
    right_fit_average = np.average(right_fit,axis=0)
    left_line = make_coordinates(image, left_fit_average)
    right_line = make_coordinates(image, right_fit_average)
    return np.array([left_line,right_line])