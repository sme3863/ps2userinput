#TODO
#change movement handling to allow for more than 8 directions
#write comments...
#cleanup code
#add combination to open onscreen keyboard
#add combination to open applauncher-wheel
#add toggle to faster mouse speed
#


from evdev import InputDevice, InputEvent, list_devices
from select import select
from evdev import UInput, ecodes as e
import time
import sys


def TRIANGLE_KEY(ui,value):
	ui.write(e.EV_KEY,e.KEY_GRAVE,value)

def SQUARE_KEY(ui,value):
	ui.write(e.EV_KEY,e.KEY_TAB,value)

def CIRCLE_KEY(ui,value):
	ui.write(e.EV_KEY,e.KEY_C,value)

def CROSS_KEY(ui,value):
	ui.write(e.EV_KEY,e.BTN_LEFT,value)

def L1_KEY(ui,value):
	ui.write(e.EV_KEY,e.KEY_LEFTALT	,value)

def L2_KEY(ui,value):
	ui.write(e.EV_KEY,e.KEY_LEFTCTRL,value)

def R1_KEY(ui,value):
	ui.write(e.EV_KEY,e.KEY_ENTER,value)

def R2_KEY(ui,value):
	ui.write(e.EV_KEY,e.KEY_LEFTSHIFT,value)

def START_KEY(ui,value):
	print("Start")
	
def SELECT_KEY(ui,value):
	print("Select")

def LEFT_RIGHT_KEY(ui,value):
	return {}

def UP_DOWN_KEY(ui,value):
	return {}

def LEFT_STICK_UP_DOWN(ui,value):
	value = getMouseMovement(value)
	return {0:value}

def LEFT_STICK_LEFT_RIGHT(ui,value):
	value = getMouseMovement(value)
	return {1:value}

def LEFT_STICK_PRESSED(ui,value):
	print("LStick-Pressed")

def RIGHT_STICK_UP_DOWN(ui,value):
	value = getMouseMovement(value)
	return {0:value}

def RIGHT_STICK_LEFT_RIGHT(ui,value):
	value = getMouseMovement(value)
	return {1:value}	


def RIGHT_STICK_PRESSED(ui,value):
	ui.write(e.EV_KEY,e.KEY_DEL,value)



def getMouseMovement(value):
	value = value - NEUTRAL_POSITION	
	if(value < 0):
		value = value-1

	value = value/8
	return value


def print_available_devices():
	devices = map(InputDevice, list_devices())
	print("available devices: ")
	for dev in devices:
		print( '%-20s %-32s %s' % (dev.fn, dev.name, dev.phys) )


NEUTRAL_POSITION = 127
BUTTON_PRESSED = 1
BUTTON_RELEASED = 0
BUTTON_TYPE = 1
MOVEMENT_TYPE = 3
options = {
	288:TRIANGLE_KEY,
	291:SQUARE_KEY,
	289:CIRCLE_KEY,
	290:CROSS_KEY,
	294:L1_KEY,
	292:L2_KEY,
	295:R1_KEY,
	293:R2_KEY,
	297:START_KEY,
	296:SELECT_KEY,
	16:LEFT_RIGHT_KEY,
	17:UP_DOWN_KEY,
	1:LEFT_STICK_UP_DOWN,
	0:LEFT_STICK_LEFT_RIGHT,
	298:LEFT_STICK_PRESSED,
	2:RIGHT_STICK_UP_DOWN,
	5:RIGHT_STICK_LEFT_RIGHT,
	299:RIGHT_STICK_PRESSED,
}




mouse_capabilities = {
    e.EV_REL : (e.REL_X, e.REL_Y), 
    e.EV_KEY : (e.BTN_LEFT, e.BTN_RIGHT),
}


if len(sys.argv) != 2:
	exit("need number of device to read from. example: controller is /dev/input/event9 -> python controller.py 9 \nget list of devices with -devices")


try:
	command = sys.argv[1]
	if command == "-devices":
		print_available_devices()
		sys.argv[1] = raw_input("number of controller is /dev/input/event")
	nr = int(sys.argv[1])
except ValueError:
	exit("need number of device to read from. example: controller is /dev/input/event9 -> python controller.py 9 \nget list of devices with -devices")

keyboard = UInput()
mouse = UInput(mouse_capabilities)
device = InputDevice('/dev/input/event'+str(nr))

moveX = 0
moveY = 0

FPS = 30
TIME = .1/FPS


while True:
	time.sleep(TIME)	
	try:
		gen = device.read();
		for event in gen:
			if(event.type == BUTTON_TYPE):
				options[event.code](keyboard,event.value)
				keyboard.syn()
			if(event.type == MOVEMENT_TYPE):
				move = options[event.code](mouse,event.value)
				if(0 in move):
					moveY = move[0]
				elif(1 in move):
					moveX = move[1]

				if(moveX < 0):
					moveX = -1
				elif(moveX > 0):
					moveX = 1
				else:
					moveX = 0
				if(moveY < 0):
					moveY = -1
				elif(moveY > 0):
					moveY = 1
				else:
					moveY = 0
	except IOError:
		pass
	
	mouse.write(e.EV_REL, e.REL_X, moveX)
	mouse.write(e.EV_REL, e.REL_Y, moveY)
	mouse.syn()



