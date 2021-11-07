from gtts import gTTS
import pyautogui
import random
import cv2

from playsound import playsound
print("Audio or Message or Key or Mouse or video? (1/2/3/4/5): ")
option1 = input()
if option1 == "1":
    print("Play a mp3 or create a text to speach? (1/2): ")
    option2 = input()
    if option2 == "1":
        print("What is the name of the mp3?: ")
        mp3 = input()
        if mp3 == '':
            playsound('Never Gonna Give You Up Original.mp3')
        else:
            playsound(input)
    if option2 == "2":
        print("what do you wanna say?: ")
        blabla = input()
        tts = gTTS(text=blabla, lang='en', tld = 'ie')
        tts.save(r"textVoice.mp3")
        playsound('textVoice.mp3')
if option1 == "2":
    print("What title do you wanna display?")
    title = input()
    print("What Message do you wanna display?")
    msg = input()
    pyautogui.alert(title=title, text = msg)
if option1 == "3":
    print("what type of interaction; press, hold, (1/2): ")
    option3 = input()
    print("what keys if multible seperate by ',': ")
    keys = input()
    keys = keys.split(",")
    if option3 == '1':
        pyautogui.press(keys)
    if option3 == '2':
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
    print("What video do you want to play?")
    vid = input()
    if vid == "":
        cap = cv2.VideoCapture('Chaos/Stormtrooper Hits Head(Star Wars Fail) HD.mp4')
    else:
        cap = cv2.VideoCapture(vid)
    cv2.namedWindow('vid', cv2.WINDOW_AUTOSIZE)
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
