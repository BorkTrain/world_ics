#!/usr/bin/env python
import time

PLCS = {'FUEL':'10.10.1.120','WATERPUMP':'10.10.1.121','BOILER':'10.10.1.122','TURBINE':'10.10.1.123','GENERATOR':'10.10.1.124','PYLON':'10.10.1.125'}

def send_to_plc(reg_loc,reg_value,ip):
	from pymodbus.client.sync import ModbusTcpClient as ModbusClient
	modbusClient = ModbusClient(ip, port=5020)
	modbusClient.write_register(reg_loc,reg_value)
	return True

def read_from_plc(reg_start,reg_stop,ip):
	from pymodbus.client.sync import ModbusTcpClient as ModbusClient
	modbusClient = ModbusClient(ip, port=5020)
	res = modbusClient.read_holding_registers(reg_start,reg_stop).registers
	return res

def get_plc_img():
	res = {}
	# res = {'FUEL':'fuel_off.jpg','WATERPUMP':'waterpump_off.jpg'}
	for plc_name in PLCS:
		plc_ip = PLCS.get(plc_name)
		plc_vals = read_from_plc(1,11,plc_ip)
		if plc_name is 'FUEL':
			res[plc_name] = get_fuel_img(plc_vals)
		elif plc_name is 'WATERPUMP':
			res[plc_name] = get_water_img(plc_vals)
		elif plc_name is 'BOILER':
			res[plc_name] = get_boiler_img(plc_vals)
		elif plc_name is 'TURBINE':
			res[plc_name] = get_turbine_img(plc_vals)
		elif plc_name is 'GENERATOR':
			res[plc_name] = get_generator_img(plc_vals)
		elif plc_name is 'PYLON':
			res[plc_name] = get_pylon_img(plc_vals)
	return res

def get_fuel_img(plc_vals):
	plc_sum = sum(plc_vals)
	plc_res = "fuel_{}.png"
	if plc_sum == 33:
		rate = 'max'
	elif plc_sum == 22:
		rate = 'norm'
	elif plc_sum == 11:
		rate = 'low'
	else:
		rate = 'off'
		for i in (10,11):
			send_to_plc(i,0,PLCS.get('WATERPUMP'))
			send_to_plc(i,0,PLCS.get('BOILER'))
			send_to_plc(i,0,PLCS.get('TURBINE'))
			send_to_plc(i,0,PLCS.get('GENERATOR'))
			send_to_plc(i,0,PLCS.get('PYLON'))
	return plc_res.format(rate)

def get_water_img(plc_vals):
	plc_sum = sum(plc_vals)
	plc_res = "waterpump_{}.png"
	if plc_sum > 9:
		rate = 'on_used'
	elif plc_sum == 9:
		rate = 'on'
	else:
		rate = 'off'
		for i in (10,11):
			send_to_plc(i,0,PLCS.get('BOILER'))
			send_to_plc(i,0,PLCS.get('TURBINE'))
			send_to_plc(i,0,PLCS.get('GENERATOR'))
			send_to_plc(i,0,PLCS.get('PYLON'))
	return plc_res.format(rate)

def get_boiler_img(plc_vals):
	plc_sum = sum(plc_vals)
	plc_res = "boiler_{}.png"
	if plc_sum == 13:
		rate = 'max'
	elif plc_sum == 12:
		rate = 'norm'
	elif plc_sum == 11:
		rate = 'low'
	elif plc_sum < 11 and plc_sum > 3:
		rate = 'on'
	else:
		rate = 'off'
		for i in (10,11):
			send_to_plc(i,0,PLCS.get('TURBINE'))
			send_to_plc(i,0,PLCS.get('GENERATOR'))
			send_to_plc(i,0,PLCS.get('PYLON'))
	return plc_res.format(rate)

def get_turbine_img(plc_vals):
	plc_sum = sum(plc_vals)
	plc_res = "turbine_{}.png"
	if plc_sum == 13:
		rate = 'max'
	elif plc_sum == 12:
		rate = 'norm'
	elif plc_sum == 11:
		rate = 'low'
	elif plc_sum < 11 and plc_sum > 3:
		rate = 'on'
	else:
		rate = 'off'
		for i in (10,11):
			send_to_plc(i,0,PLCS.get('GENERATOR'))
			send_to_plc(i,0,PLCS.get('PYLON'))
	return plc_res.format(rate)

def get_generator_img(plc_vals):
	plc_sum = sum(plc_vals)
	plc_res = "generator_{}.png"
	if plc_sum > 8:
		rate = 'on'
	else:
		rate = 'off'
		for i in (10,11):
			send_to_plc(i,0,PLCS.get('PYLON'))
	return plc_res.format(rate)

def get_pylon_img(plc_vals):
	plc_sum = sum(plc_vals)
	plc_res = "pylon_{}.png"
	if plc_sum == 13:
		rate = 'max'
	elif plc_sum == 12:
		rate = 'norm'
	elif plc_sum == 11:
		rate = 'low'
	else:
		rate = 'off'
	return plc_res.format(rate)

def prod_on():
	x = get_plc_img()
	y = x.get('WATERPUMP')
	z = x.get('FUEL')
	if y.__contains__('on') and z != 'fuel_off.png':
		send_to_plc(10,1,PLCS.get('WATERPUMP'))
		send_to_plc(10,1,PLCS.get('BOILER'))
		send_to_plc(10,1,PLCS.get('TURBINE'))
		send_to_plc(10,1,PLCS.get('GENERATOR'))
		send_to_plc(10,1,PLCS.get('PYLON'))
	return True 

def plc_rate():
	x = get_plc_img()
	y = x.get('WATERPUMP')
	z = x.get('FUEL')
	if y.__contains__('on') and z == 'fuel_low.png':
		send_to_plc(11,1,PLCS.get('BOILER'))
		send_to_plc(11,1,PLCS.get('TURBINE'))
		send_to_plc(11,1,PLCS.get('GENERATOR'))
		send_to_plc(11,1,PLCS.get('PYLON'))
	elif y.__contains__('on') and z == 'fuel_norm.png':
		send_to_plc(11,2,PLCS.get('BOILER'))
		send_to_plc(11,2,PLCS.get('TURBINE'))
		send_to_plc(11,2,PLCS.get('GENERATOR'))
		send_to_plc(11,2,PLCS.get('PYLON'))
	elif y.__contains__('on') and z == 'fuel_max.png':
		send_to_plc(11,3,PLCS.get('BOILER'))
		send_to_plc(11,3,PLCS.get('TURBINE'))
		send_to_plc(11,3,PLCS.get('GENERATOR'))
		send_to_plc(11,3,PLCS.get('PYLON'))
	else:
		pass
	return True

def water_time():
	x = get_plc_img()
	y = x.get('WATERPUMP')
	z = x.get('FUEL')
	timeout_90 = time.time() + 90
	timeout_60 = time.time() + 60
	timeout_30 = time.time() + 30
	if y == 'waterpump_off.png' and z == 'fuel_low.png':
		while time.time() < timeout_90:
			pass
		else:
			time_off_90()	
	elif y == 'waterpump_off.png' and z == 'fuel_norm.png':
		while time.time() < timeout_60:
			pass
		else:
			time_off_60()
	elif y == 'waterpump_off.png' and z == 'fuel_max.png':
		while time.time() < timeout_30:
			pass
		else:
			time_off_30()
	else:
		pass
	return True
		

def time_off_90():
	for i in (10,11):
			send_to_plc(i,0,PLCS.get('WATERPUMP'))
			send_to_plc(i,0,PLCS.get('BOILER'))
			send_to_plc(i,0,PLCS.get('TURBINE'))
			send_to_plc(i,0,PLCS.get('GENERATOR'))
			send_to_plc(i,0,PLCS.get('PYLON'))

def time_off_60():
	for i in (10,11):
		send_to_plc(i,0,PLCS.get('WATERPUMP'))
		send_to_plc(i,0,PLCS.get('BOILER'))
		send_to_plc(i,0,PLCS.get('TURBINE'))
		send_to_plc(i,0,PLCS.get('GENERATOR'))
		send_to_plc(i,0,PLCS.get('PYLON'))

def time_off_30():
	for i in (10,11):
		send_to_plc(i,0,PLCS.get('WATERPUMP'))
		send_to_plc(i,0,PLCS.get('BOILER'))
		send_to_plc(i,0,PLCS.get('TURBINE'))
		send_to_plc(i,0,PLCS.get('GENERATOR'))
		send_to_plc(i,0,PLCS.get('PYLON'))
