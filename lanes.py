import cv2
import numpy as np
import matplotlib.pyplot as plt



def canny(image):
    gray = cv2.cvtColor(lane_image, cv2.COLOR_BGR2GRAY)
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
            cv2.line(lines_image,(x1,y1),(x2,y2),(255,0,0),10)
    return lines_image



image = cv2.imread('test_image.jpg')

lane_image =np.copy(image)
im=np.copy(image)
#Edge detection: identifying sharp changes in intensity in adjascent pixels 0-black, no intensity 255 max intensity white
#convert to gray sclae because it is easy to process a 1 channel image
canny=canny(lane_image)
#plt.imshow(canny)
#plt.show()
cropped_image=region_of_interest(canny)
lines= cv2.HoughLinesP(cropped_image,2,np.pi/180,100,np.array([]),minLineLength=40, maxLineGap=5)
lines_image = display_lines(lane_image,lines)
combined= cv2.addWeighted(lane_image,0.8,lines_image,1,1)
cv2.imshow('result', combined)
cv2.waitKey(0)#displays image for specified milisecond, 0 means infinitely until any key is pressed
cv2.destroyAllWindows()


