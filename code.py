from adafruit_circuitplayground.bluefruit import cpb

from adafruit_ble import BLERadio
from adafruit_ble.advertising.standard import ProvideServicesAdvertisement
from adafruit_ble.services.nordic import UARTService

import time

ble = BLERadio()
uart = UARTService()
advertisement = ProvideServicesAdvertisement(uart)

cpb.pixels.brightness = 0.009
cpb.pixels.fill((0, 0, 0))
cpb.pixels.show()

messagequeue = []

set0 = [0, 1] # lycaon
set1 = [2, 3] # astrid
set2 = [4, 5] # resolute
set3 = [6, 7] # adonis
set4 = [8, 9] # ti

BLACK = (0,0,0)
RED = (255, 0, 0)
YELLOW = (255, 150, 0)
GREEN = (0, 255, 0)
CYAN = (0, 255, 255)
BLUE = (0, 0, 255)
PURPLE = (180, 0, 255)
ORANGE = (255, 69, 0)

def activateLEDs(pixels, color):
	for p in pixels:
		cpb.pixels[p] = color

def turnOffAll():
	cpb.pixels.fill(RED)
	cpb.pixels.fill((0,0,0))

def turnOffRecent():
	for p in messagequeue[len(messagequeue)-1]:
		cpb.pixels[p] = BLACK
	del messagequeue[len(messagequeue)-1]
	time.sleep(0.5)

def breathe():
	activateLEDs(set2, PURPLE)

def handleMessage(s):
	if s == 'set0':
		activateLEDs(set0, BLUE)
		if set0 in messagequeue:
			messagequeue.append(messagequeue.pop(messagequeue.index(set0)))
		else:
			messagequeue.append(set0)
	if s == 'set1':
		activateLEDs(set1, GREEN)
		if set1 in messagequeue:
			messagequeue.append(messagequeue.pop(messagequeue.index(set1)))
		else:
			messagequeue.append(set1)
	if s == 'set2':
		activateLEDs(set2, PURPLE)
		if set2 in messagequeue:
			messagequeue.append(messagequeue.pop(messagequeue.index(set2)))
		else:
			messagequeue.append(set2)
	if s == 'set3':
		activateLEDs(set3, ORANGE)
		if set3 in messagequeue:
			messagequeue.append(messagequeue.pop(messagequeue.index(set3)))
		else:
			messagequeue.append(set3)
	if s == 'set4':
		activateLEDs(set4, YELLOW)
		if set4 in messagequeue:
			messagequeue.append(messagequeue.pop(messagequeue.index(set4)))
		else:
			messagequeue.append(set4)

	if s == 'test-channel':
		activateLEDs(set0, BLUE)
		activateLEDs(set1, GREEN)
		activateLEDs(set2, PURPLE)
		activateLEDs(set3, ORANGE)
		activateLEDs(set4, YELLOW)		

def getColorFromPixels(pix):
	if pix == set0:
		return BLUE
	if pix == set1:
		return GREEN
	if pix == set2:
		return PURPLE
	if pix == set3:
		return ORANGE
	if pix == set4:
		return YELLOW
	

while True:
	ble.start_advertising(advertisement)
	while not ble.connected:
		pass

	ble.stop_advertising()
	print("CONNECTED")

	while ble.connected:

		if uart.in_waiting:
			raw_bytes = uart.read(uart.in_waiting)
			text = raw_bytes.decode().strip()
			print("RX: ", text)
			handleMessage(text)

		if cpb.button_a:
			turnOffAll()

		if cpb.button_b:
			if messagequeue:
				turnOffRecent()
			else:
				turnOffAll()
		
		if cpb.touch_A3:
			for p in set4:
				cpb.pixels[p] = BLACK
		
		if cpb.touch_A1:
			for p in set3:
				cpb.pixels[p] = BLACK

		if cpb.touch_TX:
			for p in set2:
				cpb.pixels[p] = BLACK
		
		if cpb.touch_A6:
			for p in set1:
				cpb.pixels[p] = BLACK

		if cpb.touch_A4:
			for p in set0:
				cpb.pixels[p] = BLACK
		
		cpb.pixels.show()

	print("DISCONNECTED")