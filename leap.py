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
			# console.log("hello?")
			# time.sleep(1)
			k.type("QWERTY,     ")
			k.type('Gesture type: ' + gestures[0]['type'])
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