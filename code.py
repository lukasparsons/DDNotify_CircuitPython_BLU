from adafruit_circuitplayground.express import cpx
import usb_cdc
import time

sp = usb_cdc.serials[1]
sp.timeout = 0
cpx.pixels.brightness = 0.009
cpx.pixels.fill((0, 0, 0))
cpx.pixels.show()

messagequeue = []

lycaonpixels = [0, 1]
astridpixels = [2, 3]
resolutepixels = [4, 5]
adonispixels = [6, 7]
tipixels = [8, 9]

BLACK = (0,0,0)
RED = (255, 0, 0)
YELLOW = (255, 150, 0)
GREEN = (0, 255, 0)
CYAN = (0, 255, 255)
BLUE = (0, 0, 255)
PURPLE = (180, 0, 255)
ORANGE = (255, 69, 0)

def activatePlayerLEDs(pixels, color):
	for p in pixels:
		cpx.pixels[p] = color

def turnOffAll():
	cpx.pixels.fill(RED)
	cpx.pixels.fill((0,0,0))

def turnOffRecent():
	for p in messagequeue[len(messagequeue)-1]:
		cpx.pixels[p] = BLACK
	del messagequeue[len(messagequeue)-1]
	time.sleep(0.5)

def breathe():
	activatePlayerLEDs(resolutepixels, PURPLE)

def handleMessage(s):
	if s == 'resolute-du-coreiseuse':
		activatePlayerLEDs(resolutepixels, PURPLE)
		if resolutepixels in messagequeue:
			messagequeue.append(messagequeue.pop(messagequeue.index(resolutepixels)))
		else:
			messagequeue.append(resolutepixels)
	if s == 'adonis-jahran':
		activatePlayerLEDs(adonispixels, ORANGE)
		if adonispixels in messagequeue:
			messagequeue.append(messagequeue.pop(messagequeue.index(adonispixels)))
		else:
			messagequeue.append(adonispixels)
	if s == 'lycaon-ascelin':
		activatePlayerLEDs(lycaonpixels, BLUE)
		if lycaonpixels in messagequeue:
			messagequeue.append(messagequeue.pop(messagequeue.index(lycaonpixels)))
		else:
			messagequeue.append(lycaonpixels)
	if s == 'ti-bronsson':
		activatePlayerLEDs(tipixels, YELLOW)
		if tipixels in messagequeue:
			messagequeue.append(messagequeue.pop(messagequeue.index(tipixels)))
		else:
			messagequeue.append(tipixels)
	if s == 'astrid':
		activatePlayerLEDs(astridpixels, GREEN)
		if astridpixels in messagequeue:
			messagequeue.append(messagequeue.pop(messagequeue.index(astridpixels)))
		else:
			messagequeue.append(astridpixels)
	if s == 'Test Message':
		cpx.pixels.fill(GREEN)
	if s == 'test-channel':
		activatePlayerLEDs(resolutepixels, PURPLE)
		activatePlayerLEDs(adonispixels, ORANGE)
		activatePlayerLEDs(lycaonpixels, BLUE)
		activatePlayerLEDs(tipixels, YELLOW)
		activatePlayerLEDs(astridpixels, GREEN)

def getColorFromPixels(pix):
	if pix == resolutepixels:
		return PURPLE
	if pix == adonispixels:
		return ORANGE
	if pix == lycaonpixels:
		return BLUE
	if pix == tipixels:
		return YELLOW
	if pix == astridpixels:
		return GREEN

while True:
	if cpx.button_a:
		turnOffAll()

	if cpx.button_b:
		if messagequeue:
			turnOffRecent()
		else:
			turnOffAll()
	
	if cpx.touch_A3:
		for p in tipixels:
			cpx.pixels[p] = BLACK
	
	if cpx.touch_A1:
		for p in adonispixels:
			cpx.pixels[p] = BLACK

	if cpx.touch_A7:
		for p in resolutepixels:
			cpx.pixels[p] = BLACK
	
	if cpx.touch_A6:
		for p in astridpixels:
			cpx.pixels[p] = BLACK

	if cpx.touch_A4:
		for p in lycaonpixels:
			cpx.pixels[p] = BLACK

	if sp.in_waiting > 0:
		b = sp.readline(-1)
		if b is not None:
			bs = b.decode('utf-8')
			print(bs)
			handleMessage(bs)



	cpx.pixels.show()