#!/usr/bin/env python
import time
from reg_reader import *
import threading

def water_time():
#	threading.Timer(60.0, water_time).start()
	while True:
		x = get_plc_img()
		y = x.get('WATERPUMP')
		z = x.get('FUEL')
		if y == 'waterpump_off.png' and z == 'fuel_low.png':
			replay_time = 0
			while replay_time < 9:
				y = x.get('WATERPUMP')
				if y != 'waterpump_off.png':
					break
				time.sleep(90)
				replay_time += 1
			else:
				time_off()	
		elif y == 'waterpump_off.png' and z == 'fuel_norm.png':
			replay_time = 0
			while replay_time < 9:
				y = x.get('WATERPUMP')
				if y != 'waterpump_off.png':
					break
				time.sleep(60)
				replay_time += 1
			else:
				time_off()	
		elif y == 'waterpump_off.png' and z == 'fuel_max.png':
			replay_time = 0
			while replay_time < 9:
				y = x.get('WATERPUMP')
				if y != 'waterpump_off.png':
					break
				time.sleep(30)
				replay_time += 1
			else:
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
