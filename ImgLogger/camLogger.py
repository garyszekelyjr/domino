import cv2
import numpy as np
import glob
import re

camera = cv2.VideoCapture(0)
path = 'CamImages/'
for i in range(300):
    return_value, image = camera.read()
    cv2.imwrite(path + 'camrecord' + str(i) + '.png', image)
del(camera)

img_array = []
for filename in sorted(glob.glob(path + '*.png')):
    img = cv2.imread(filename)
    height, width, layers = img.shape
    size = (width,height)
    img_array.append(img)
 
 
out = cv2.VideoWriter('CamRecording.mp4',cv2.VideoWriter_fourcc(*'DIVX'), 15, size ,)
 
for i in range(len(img_array)):
    out.write(img_array[i])
out.release()