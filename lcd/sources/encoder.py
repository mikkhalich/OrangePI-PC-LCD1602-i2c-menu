from pyA20.gpio import gpio
from pyA20.gpio import connector
from pyA20.gpio import port

import time
#from time import sleep

# encoder pins
clk_pin = port.PA1
dt_pin = port.PA0
btn_pin = port.PA3

gpio.init()

# pin config
gpio.setcfg(clk_pin, gpio.INPUT)
gpio.setcfg(dt_pin, gpio.INPUT)
gpio.setcfg(btn_pin, gpio.INPUT)

# pin pullup
#gpio.pullup(clk_pin, gpio.PULLUP)
#gpio.pullup(dt_pin, gpio.PULLUP)
#gpio.pullup(btn_pin, gpio.PULLUP)

# encoder pin's state
clkLastState = gpio.input(clk_pin)
clkLast = gpio.input (clk_pin)

# encoder counter
counter = 0
click_flag = 0
click_time = 0


def getEncoderState(prc_encUp, prc_encDown, prc_ShortClick, prc_longClick):
	global clkLastState
	global counter
	global click_flag
	global click_time
	
	try:
		if gpio.input(btn_pin) and click_flag == 0:
			click_flag = 1
			time.sleep(0.05)
			if gpio.input(btn_pin):
				click_time = time.time()
		elif  gpio.input(btn_pin)  == 0 and click_flag == 1:
			click_flag = 0
			if time.time() - click_time > 0.6:
				if prc_longClick != None:
					prc_longClick()
				else:
					print ("long_click")
			elif time.time() - click_time > 0.09:
				if prc_ShortClick != None:
					prc_ShortClick()
				else:
					print ("short_click")
				
				
		clkState = gpio.input(clk_pin)
			
		if clkState != clkLastState:
			dtState = gpio.input(dt_pin)
			if dtState != clkState:
				counter +=1
				time.sleep(0.1)
				if prc_encUp != None:
					prc_encUp(counter)
				else:
					print(counter)
			else:
				counter -=1
				time.sleep(0.1)
				if prc_encDown != None:
					prc_encDown(counter)
				else:
					print(counter)
			
		clkState = clkLastState
		
		
	finally:
		pass
		#print ("Ending")
		
if __name__ == '__main__':
	while True:
		getEncoderState(None, None, None, None)
		time.sleep(0.02)


	
#gpio.add_event_detect(clk_pin, gpio.FALLING, callback = my_callback, bouncetime = 300)
