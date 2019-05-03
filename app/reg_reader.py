#!/usr/bin/env python
import time

PLCS = {'FUEL':'10.10.1.120','WATERPUMP':'10.10.1.121','BOILER':'10.10.1.122','TURBINE':'10.10.1.123','GENERATOR':'10.10.1.124','PYLON':'10.10.1.125'}

def send_to_plc(reg_loc,reg_value,ip):
	from pymodbus.client.sync import ModbusTcpClient as ModbusClient
	modbusClient = ModbusClient(ip, port=502)
	modbusClient.write_register(reg_loc,reg_value)
	return True

def read_from_plc(reg_start,reg_stop,ip):
	from pymodbus.client.sync import ModbusTcpClient as ModbusClient
	modbusClient = ModbusClient(ip, port=502)
	res = modbusClient.read_holding_registers(reg_start,reg_stop).registers
	return res

def get_plc_stat():
	res = {}
	# res = {'FUEL':'off'|'low'|'norm'|'max','WATERPUMP':'off'|'on'}
	for plc_name in PLCS:
		plc_ip = PLCS.get(plc_name)
		plc_vals = read_from_plc(1,16,plc_ip)
		if plc_name is 'FUEL':
			res[plc_name] = get_fuel_stat(plc_vals)
		elif plc_name is 'WATERPUMP':
			res[plc_name] = get_water_stat(plc_vals)
		elif plc_name is 'BOILER':
			res[plc_name] = get_boiler_stat(plc_vals)
		elif plc_name is 'TURBINE':
			res[plc_name] = get_turbine_stat(plc_vals)
		elif plc_name is 'GENERATOR':
			res[plc_name] = get_generator_stat(plc_vals)
		elif plc_name is 'PYLON':
			res[plc_name] = get_pylon_stat(plc_vals)
	return res

def get_fuel_stat(plc_vals):
	plc_sum = sum(plc_vals)
	if plc_sum == 64:
		rate = 'max'
	elif plc_sum == 32:
		rate = 'norm'
	elif plc_sum == 16:
		rate = 'low'
	else:
		rate = 'off'
	return rate

def get_water_stat(plc_vals):
	plc_sum = sum(plc_vals)
	if plc_sum == 16:
		rate = 'on'
	else:
		rate = 'off'
	return rate

def get_boiler_stat(plc_vals):
	plc_sum = sum(plc_vals)
	if plc_sum == 16:
		rate = 'open'
	else:
		rate = 'closed'
	return rate

def get_turbine_stat(plc_vals):
	plc_sum = sum(plc_vals)
	if plc_sum == 16:
		rate = 'on'
	else:
		rate = 'off'
	return rate

def get_generator_stat(plc_vals):
	plc_sum = sum(plc_vals)
	if plc_sum == 16:
		rate = 'on'
	else:
		rate = 'off'
	return rate

def get_pylon_stat(plc_vals):
	plc_sum = sum(plc_vals)
	if plc_sum == 16:
		rate = 'on'
	else:
		rate = 'off'
	return rate
