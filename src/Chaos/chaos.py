from gtts import gTTS
import pyautogui
import random
import cv2
from playsound import playsound
import sys

option1 = sys.argv[1]
if option1 == "1":
    option2 = sys.argv[2]
    if option2 == "1":
        playsound('Never Gonna Give You Up Original.mp3')
    if option2 == "2":
        text = sys.argv[3]
        text = " ".join(text.split("|"))
        tts = gTTS(text=text, lang='en', tld = 'ie')
        tts.save(r"textVoice.mp3")
        playsound('textVoice.mp3')
if option1 == "2":
    title = " ".join(sys.argv[2].split("|"))
    msg = " ".join(sys.argv[3].split("|"))
    pyautogui.alert(title=title, text = msg)
if option1 == "3":
    option2 = sys.argv[2]
    keys = sys.argv[3]
    keys = keys.split(",")
    if option2 == '1':
        pyautogui.press(keys)
    if option2 == '2':
        for i in keys:
            pyautogui.keyDown(i)
if option1 == "4":
    xmax, ymax = pyautogui.size()
    funct = [pyautogui.easeInQuad, pyautogui.easeOutQuad, pyautogui.easeInOutQuad, pyautogui.easeInBounce, pyautogui.easeInElastic]
    dir = ["left", "right"]
    while(1):
        x = random.randint(0,xmax)
        y = random.randint(0,ymax)
        t = random.uniform(pyautogui.MINIMUM_DURATION, 10)
        f = random.randint(0, len(funct)-1)
        c = random.randint(0,4)
        d = random.randint(0,1)
        r = random.randint(0,3)
        if r == 0:
            pyautogui.moveTo(x, y, t, funct[f])
        if r == 1:
            pyautogui.dragTo(x, y, t, button=dir[d])
        if r == 2:
            pyautogui.click(x, y, clicks = c, button=dir[d])
        if r == 3:
            pyautogui.mouseDown(button=dir[d])
            pyautogui.mouseUp(button=dir[d], x=x, y=y)
        if r == 4:
            pyautogui.click()
            pyautogui.scroll(random.rand(-15, 15))
if option1 == '5':
    cap = cv2.VideoCapture('Stormtrooper Hits Head(Star Wars Fail) HD.mp4')
    cv2.namedWindow("vid", cv2.WINDOW_AUTOSIZE)
    while True:
        ret_val, frame = cap.read()
        if not ret_val:
            break
        try:
            cv2.imshow('vid', frame)
        except:
            pass
        if cv2.waitKey(1) == 27:
            break  # esc to quit
    cv2.destroyAllWindows()
