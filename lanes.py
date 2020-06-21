import cv2
import numpy as np
import matplotlib.pyplot as plt



def canny(image):
    gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    canny = cv2.Canny(blur, 50, 150)
    return canny

def region_of_interest(image):
    height=image.shape[0]
    polygon=np.array([[(200,height),(1100,height),(550,250)]])
    mask = np.zeros_like(image)
    cv2.fillPoly(mask, polygon ,255)#white triangle boundary
    masked_image=cv2.bitwise_and(image,mask)

    return masked_image

def display_lines(image,lines):
    lines_image=np.zeros_like(image)
    if lines is not None:
        for line in lines:
            x1,y1,x2,y2=line.reshape(4)
            cv2.line(lines_image,(x1,y1),(x2,y2),(0,255,0),9)
    return lines_image

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

'''image = cv2.imread('test_image.jpg')

lane_image =np.copy(image)
im=np.copy(image)

canny_image=canny(lane_image)

cropped_image=region_of_interest(canny_image)
lines= cv2.HoughLinesP(cropped_image,2,np.pi/180,100,np.array([]),minLineLength=40, maxLineGap=5)
average_lines= average_slope_intercept(lane_image,lines)

lines_image = display_lines(lane_image,average_lines)
combined= cv2.addWeighted(lane_image,0.8,lines_image,1,1)
cv2.imshow('result', combined)
cv2.waitKey(0)#displays image for specified milisecond, 0 means infinitely until any key is pressed
cv2.destroyAllWindows()
'''

cap = cv2.VideoCapture('data/sample_video.mp4 ')
while(cap.isOpened()):
    _, frame =cap.read()
    canny_image = canny(frame)

    cropped_image = region_of_interest(canny_image)
    lines = cv2.HoughLinesP(cropped_image, 2, np.pi / 180, 100, np.array([]), minLineLength=40, maxLineGap=5)
    average_lines = average_slope_intercept(frame, lines)

    lines_image = display_lines(frame, average_lines)
    combined = cv2.addWeighted(frame, 0.8, lines_image, 1, 1)
    cv2.imshow('result', combined)
    cv2.waitKey(1)  # displays image for specified milisecond, 0 means infinit

