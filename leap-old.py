import websocket, json, pyautogui, time

try:
	import thread
except ImportError:
	import _thread as thread

# Global Variables
gameStarted = False # denotes whether the game has started, no keypresses will occur until game is started
lastGestureTime = 0 # denotes last time a gesture keypress was triggered
gestureGracePeriod = 1 # denotes how much time (in seconds) program must wait after a gesture keypress is sent to send another one
grabThreshold = 0.5 # denotes what grab amount is required for the grab to occur
isLeftGrabbed = False # denotes whether the left hand is currently being grabbed
isRightGrabbed = False # denotes whether the right hand is currently being grabbed (used for items)
lastRightGrabTime = 0 # denotes how much time (in seconds) program must wait after grabbing or dropping an item 
leftCenterX = 0 # denotes the origin position in the X direction for the left hand
leftCenterY = 0 # denotes the origin position in the Y direction for the left hand
moveThreshold = 30 # denotes the distance away from the origin the left hand must be in order to move
moveUp = False
moveDown = False
moveLeft = False
moveRight = False
lastMoveTime = 0 # denotes last time a move keypress was triggered
moveGracePeriod = 1 # denotes how much time (in seconds) program must wait after a move keypress is sent to send another one

def on_message(ws, message):
	# Load all the global variables
	global gameStarted, lastGestureTime, gestureGracePeriod, grabThreshold, isLeftGrabbed, isRightGrabbed, lastRightGrabTime, leftCenterX, leftCenterY, moveThreshold, moveUp, moveDown, moveLeft, moveRight, lastMoveTime, moveGracePeriod

	leftHand = False
	rightHand = False
	gesture = False

	currentTime = time.time()

	# Get the JSON data from the Leap Motion Websocket
	result = json.loads(message)

	# Hands Lookup
	if 'hands' in result:
		hands = result['hands']
		if len(hands) > 0:
			for x in range(len(hands)):
				if hands[x]['type'] == "left":
					leftHand = hands[x]
				elif hands[x]['type'] == "right":
					rightHand = hands[x]

	# Right Hand Gesture Lookup
	if 'gestures' in result:
		gestures = result['gestures']
		if len(gestures) > 0 and rightHand:
			if gestures[0]['handIds'][0] == rightHand['id']:
				gesture = gestures[0]

				if currentTime >= lastGestureTime + gestureGracePeriod: 
					# Push the LEFT CTRL key to do the action
					lastGestureTime = currentTime
					print("ctrlleft")
					pyautogui.press('ctrlleft')

	# Left Hand Grab Lookup
	if leftHand:
		if leftHand['grabStrength'] >= grabThreshold:
			isLeftGrabbed = True

			if gameStarted:
				# Closing your hand after game start resets the calibration of the left hand movement control
				leftCenterX = leftHand['palmPosition'][0]
				leftCenterY = leftHand['palmPosition'][1]
		else:
			isLeftGrabbed = False

	# Right Hand Grab Lookup
	if rightHand:
		if not isRightGrabbed and rightHand['grabStrength'] >= grabThreshold:
			# Right hand was previously not grabbed but is now above the grab threshold, process a change
			isRightGrabbed = True

			if gameStarted and (currentTime > lastRightGrabTime + gestureGracePeriod):
				# Push the SPACE key to pick up / drop item
				lastRightGrabTime = currentTime
				print("space")
				pyautogui.press('space')
		elif isRightGrabbed and rightHand['grabStrength'] < grabThreshold:
			# Right hand was previously grabbing an item but is now not above the grab threshold, process a change
			isRightGrabbed = False

			if gameStarted and (currentTime > lastRightGrabTime + gestureGracePeriod):
				#Push the SPACE key to pick up / drop item
				lastRightGrabTime = currentTime
				print("space")
				pyautogui.press('space')

	# Both Hand Grab Lookup (to start program)
	if leftHand and rightHand:
		if isLeftGrabbed and isRightGrabbed and not gameStarted:
			print("Game Started")
			gameStarted = True
			leftCenterX = leftHand['palmPosition'][0]
			leftCenterY = leftHand['palmPosition'][1]

	# Left Hand Position Lookup
	if leftHand and gameStarted and (currentTime > lastMoveTime + moveGracePeriod):
		lastMoveTime = currentTime
		print(result['id'])
		# print(leftCenterX)
		if leftHand['palmPosition'][0] > (leftCenterX + moveThreshold):
			# Positive X direction
			# moveUp = True
			print("up")
			pyautogui.keyUp('down')
			pyautogui.keyDown('up')
		elif leftHand['palmPosition'][0] < (leftCenterX - moveThreshold):
			# Negative X direction
			# moveDown = True
			print("down")
			pyautogui.keyUp('up')
			pyautogui.keyDown('down')
		else:
			pyautogui.keyUp('up')
			pyautogui.keyUp('down')

		if leftHand['palmPosition'][1] > (leftCenterY + moveThreshold):
			# Postive Y direction
			# moveRight = True
			print("right")
			pyautogui.keyUp('left')
			pyautogui.keyDown('right')
		elif leftHand['palmPosition'][1] < (leftCenterX - moveThreshold):
			# Negative Y direction
			# moveLeft = True
			print("left")
			pyautogui.keyUp('right')
			pyautogui.keyDown('left')
		else:
			pyautogui.keyUp('right')
			pyautogui.keyUp('left')
			
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