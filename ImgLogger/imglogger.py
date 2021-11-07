import pyautogui
import cv2
import numpy as np
import glob
import re



path = 'ImgLogger/RecImages/'
for i in range(100):
    img = pyautogui.screenshot()
    img = cv2.cvtColor(np.array(img),cv2.COLOR_RGB2BGR)
    cv2.imwrite(path + 'camrecord' + str(i) + '.png', img)

img_array = []
for filename in sorted(glob.glob(path + '*.png')):
    img = cv2.imread(filename)
    height, width, layers = img.shape
    size = (width,height)
    img_array.append(img)
 
 
out = cv2.VideoWriter('ScreenRecord.mp4',cv2.VideoWriter_fourcc(*'DIVX'), 15, size)
 
for i in range(len(img_array)):
    out.write(img_array[i])
out.release()
