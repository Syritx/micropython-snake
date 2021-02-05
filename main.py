import machine
import ssd1306
import time


BUTTON_PINS = [5, 4, 0, 14] # D1, D2, D3 and D5 Pins
SCREEN_PINS = [12, 13] # D6 and D7 Pins

class Button:
    button = None
    type = ''
    is_up = False

    def __init__(self, pin, type):
	self.button = machine.Pin(pin, machine.Pin.IN, machine.Pin.PULL_UP)
	self.type = type

class Segment:
    x = 0
    y = 0

    def __init__(self, x, y):
	self.x = x
	self.y = y

x_player = 128/2
y_player = 64/2

x_food = 10
y_food = 10

x_dir = 0
y_dir = 0

segments = []
display = None

def restart_game():
    global display
    segments = []
    x_food = int(rand(127, 1))
    y_food = int(rand(63, 1))

    x_player = int(128/2)
    y_player = int(64/2)
    x_dir = 0
    y_dir = 0
    display.fill(0)
    display.rect(x_player, y_player, 1, 1, 1)
    display.rect(x_food, y_food, 1, 1, 1)
    display.show()


def rand(floor, mod = 0, negative = False):
    from os import urandom as rnd
    
    sign = 1 if ord(rnd(1))%10 > 5 else -1
    sign = sign if negative else 1
    value = 0

    if mod:
	value = float(('{}.{}').format(ord(rnd(1))%floor, ord(rnd(1))%mod))
    else:
	value = int(('{}').format(ord(rnd(1))%floor))

    return sign*value


def start():
    global x_player, y_player, x_food, y_food, x_dir, y_dir, display

    buttons = [Button(BUTTON_PINS[0], 'UP'),
	       Button(BUTTON_PINS[1], 'DOWN'),
	       Button(BUTTON_PINS[2], 'RIGHT'),
	       Button(BUTTON_PINS[3], 'LEFT')]

    x_food = int(rand(127,1))
    y_food = int(rand(63, 1))

    i2c = machine.I2C(scl=machine.Pin(SCREEN_PINS[1]), sda=machine.Pin(SCREEN_PINS[0]))
    display = ssd1306.SSD1306_I2C(128, 64, i2c)

    while True:
	for button in buttons:
	    
	    if button.button.value() == 0:

		if button.type == 'UP':
		     if y_dir != 1:
		   	 y_dir = -1
		   	 x_dir = 0

		elif button.type == 'DOWN':
		    if y_dir != -1:
		    	y_dir = 1
		   	x_dir = 0

		elif button.type == 'LEFT':
		    if x_dir != 1:
		    	x_dir = -1
		    	y_dir = 0

		elif button.type == 'RIGHT':
		    if x_dir != -1:
		    	x_dir = 1
		    	y_dir = 0

	if x_player > 127:
	    x_player = 0
	if x_player < 0:
	    x_player = 127

	if y_player > 63:
	    y_player = 0
	if y_player < 0:
	    y_player = 63

	display.fill(0)

	s_x = 0
	s_y = 0

	if len(segments) > 0:
	    for s in range(len(segments)-1, 0, -1):
		
		s_x = segments[s-1].x
		s_y = segments[s-1].y
		segments[s].x = s_x
		segments[s].y = s_y
		display.rect(int(s_x), int(s_y), 1, 1, 1)
	    
	    segments[0].x = x_player
	    segments[0].y = y_player
		
	display.rect(int(x_player), int(y_player), 1, 1, 1)
	display.rect(x_food, y_food, 1, 1, 1)
	display.show()
	
	x_player += x_dir
	y_player += y_dir

	for s in segments:
	    if x_player == s.x and y_player == s.y:
		restart_game()

	if x_player <= x_food+1 and x_player >= x_food-1 and y_player <= y_food+1 and y_player >= y_food-1:
	    x_food = int(rand(127, 1))
	    y_food = int(rand(63, 1))
	    
	    segments.append(Segment(x_player, y_player))
	    print(x_food)
	    print(y_food)

