import websocket, json
# from pyautogui import press, typewrite, hotkey

from pynput.keyboard import Key, Controller
k = Controller()
import time

try:
	import thread
except ImportError:
	import _thread as thread
import time

def on_message(ws, message):
	result = json.loads(message)
	if 'gestures' in result:
		gestures = result['gestures']
		if len(gestures) > 0:
			print(gestures[0]['type'])
			# time.sleep(1)
			g = gestures[0]['type']
			handle_gesture(g)
			# k.type("QWERTY,     ")
			# k.type('Gesture type: ' + g)
			# k.press(Key.enter)

def handle_gesture(g):
	'''goal: check if in Overcooked app, 
	so it won't be typing anywhere. 
	'''
	if False:
		k.type("QWERTY \t")
		k.type('Gesture type: ' + g)
		k.press(Key.enter)
	elif g == "circle":
		k.type("CIRCLE \t")
		k.type('Gesture type: ' + g)
		k.press(Key.enter)
	elif g == "keyTap":
		k.type("KEYTAP \t")
		k.type('Gesture type: ' + g)
		k.press(Key.enter)
	elif g == "swipe":
		k.type("SWIPE \t")
		k.type('Gesture type: ' + g)
		k.press(Key.enter)
	else:
		k.type("NANII \t")
		k.type('Gesture type: ' + g)
		k.press(Key.enter)
	

def on_error(ws, error):
	print(error)

def on_close(ws):
	print("### closed ###")

def on_open(ws):
		ws.send("{\"enableGestures\": true}")
		ws.send("{\"background\": true}")
		ws.send("{\"focused\": true}")

if __name__ == "__main__":
	websocket.enableTrace(True)
	ws = websocket.WebSocketApp("ws://localhost:6437/v6.json",
							  on_message = on_message,
							  on_error = on_error,
							  on_close = on_close)
	ws.on_open = on_open
	ws.run_forever()