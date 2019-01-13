from pynput.keyboard import Key, Controller
import time

k = Controller()

time.sleep(1.5)

#You can change the sentence
sent = "Wow steven ur such a kool kid!!!! #tfti"
for i in sent:
    k.press(i)
    #You can customize the below time
    time.sleep(0.05)