#!/usr/bin/env python
import time
from reg_reader import *
import threading

replay_time = 0

def water_time():
	threading.Timer(60.0, water_time).start()
	x = get_plc_img()
	y = x.get('WATERPUMP')
	z = x.get('FUEL')
	if y == 'waterpump_off.png' and z == 'fuel_low.png':
		while replay_time < 10:
			y = x.get('WATERPUMP')
			if y != 'waterpump_off.png':
				break
			time.sleep(10)
			replay_time += 3
		time_off()	
	elif y == 'waterpump_off.png' and z == 'fuel_norm.png':
		timeout_60 = time.time() + 600
		while time.time() < timeout_60:
			y = x.get('WATERPUMP')
			if y != 'waterpump_off.png':
				break
		time_off()
	elif y == 'waterpump_off.png' and z == 'fuel_max.png':
		timeout_30 = time.time() + 300
		while time.time() < timeout_30:
			y = x.get('WATERPUMP')
			if y != 'waterpump_off.png':
				break
		time_off()
	else:
		time.sleep(60)
	return True
		
def time_off():
	for i in (10,11):
		send_to_plc(i,0,PLCS.get('WATERPUMP'))
		send_to_plc(i,0,PLCS.get('BOILER'))
		send_to_plc(i,0,PLCS.get('TURBINE'))
		send_to_plc(i,0,PLCS.get('GENERATOR'))
		send_to_plc(i,0,PLCS.get('PYLON'))




def main():
	water_time()

if __name__ == "__main__":
	main()
