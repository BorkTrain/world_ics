#!/usr/bin/env python
from reg_reader import *


def display_plc_img():
	stat = get_plc_stat()
	fuel_stat = stat.get('FUEL')
	water_stat = stat.get('WATERPUMP')
	boiler_stat = stat.get('BOILER')
	turbine_stat = stat.get('TURBINE')
	generator_stat = stat.get('GENERATOR')
	pylon_stat = stat.get('PYLON')
	img = {}
#	img = {'FUEL':'fuel_rate.png'}
	for plc_name in PLCS:
		stat = get_plc_stat()
		if plc_name is 'FUEL':
			img[plc_name] = display_fuel_img(fuel_stat)
		elif plc_name is 'WATERPUMP':
			img[plc_name] = display_waterpump_img(water_stat,fuel_stat)
		elif plc_name is 'BOILER':
			img[plc_name] = display_boiler_img(boiler_stat,fuel_stat,water_stat)
		elif plc_name is 'TURBINE':
			img[plc_name] = display_turbine_img(turbine_stat,boiler_stat,fuel_stat,water_stat)
		elif plc_name is 'GENERATOR':
			img[plc_name] = display_generator_img(generator_stat,turbine_stat)
		elif plc_name is 'PYLON':
			img[plc_name] = display_pylon_img(pylon_stat,generator_stat,turbine_stat,fuel_stat)
	return img 

def display_fuel_img(fuel_stat):
	self_stat = fuel_stat
	plc_img = "fuel_{}.png"
	if self_stat == 'off':
		state = 'off'
	elif self_stat == 'low':
		state = 'low'
	elif self_stat == 'norm':
		state = 'norm'
	elif self_stat == 'max':
		state = 'max'
	else:
		state = 'unknown'
	return plc_img.format(state)

def display_waterpump_img(water_stat,fuel_stat):
	self_stat = water_stat
	fuel_stat = fuel_stat
	plc_img = "waterpump_{}.png"
	if self_stat == 'off':
		state = 'off'
	elif self_stat == 'on' and fuel_stat != 'off':
		state = 'on_used'
	elif self_stat == 'on':
		state = 'on'
	else:
		state = 'unknown'
	return plc_img.format(state)

def display_boiler_img(boiler_stat,fuel_stat,water_stat):
	self_stat = boiler_stat
	fuel_stat = fuel_stat
	water_stat = water_stat
	plc_img = "boiler_{}.png"
	if fuel_stat == 'off' and self_stat == 'open' and water_stat == 'on':
		state = 'overflow'
	elif fuel_stat == 'off' and self_stat == 'closed' and water_stat == 'off':
		state = 'close_emp_NA'
	elif fuel_stat == 'off' and self_stat == 'open' and water_stat == 'off':
		state = 'open_emp_NA'
	elif fuel_stat == 'off' and self_stat == 'closed' and water_stat == 'on':
		state = 'closed_full'
#START FUEL LOW
	elif fuel_stat == 'low' and self_stat == 'open' and water_stat == 'on':
		state = 'low'
	elif fuel_stat == 'low' and self_stat == 'closed' and water_stat == 'off':
		state = 'close_emp_NA'
	elif fuel_stat == 'low' and self_stat == 'open' and water_stat == 'off':
		state = 'open_emp_NA'
	elif fuel_stat == 'low' and self_stat == 'closed' and water_stat == 'on':
		state = 'closed_full_low'
#START FUEL NORM
	elif fuel_stat == 'norm' and self_stat == 'open' and water_stat == 'on':
		state = 'norm'
	elif fuel_stat == 'norm' and self_stat == 'closed' and water_stat == 'off':
		state = 'close_emp_NA'
	elif fuel_stat == 'norm' and self_stat == 'open' and water_stat == 'off':
		state = 'open_emp_NA'
	elif fuel_stat == 'norm' and self_stat == 'closed' and water_stat == 'on':
		state = 'closed_full_norm'
#START FUEL MAX
	elif fuel_stat == 'max' and self_stat == 'open' and water_stat == 'on':
		state = 'max'
	elif fuel_stat == 'max' and self_stat == 'closed' and water_stat == 'off':
		state = 'close_emp_NA'
	elif fuel_stat == 'max' and self_stat == 'open' and water_stat == 'off':
		state = 'open_emp_NA'
	elif fuel_stat == 'max' and self_stat == 'closed' and water_stat == 'on':
		state = 'closed_full_max'
	else:
		state = 'unknown'
	return plc_img.format(state)

def display_turbine_img(turbine_stat,boiler_stat,fuel_stat,water_stat):
	self_stat = turbine_stat
	boiler_stat = boiler_stat
	water_stat = water_stat
	plc_img = 'turbine_{}.png'
	if self_stat == 'on' and boiler_stat == 'open' and fuel_stat == 'low' and water_stat == 'on':
		state = 'low'
	elif self_stat == 'on' and boiler_stat == 'open' and fuel_stat == 'norm' and water_stat == 'on':
		state = 'norm'
	elif self_stat == 'on' and boiler_stat == 'open' and fuel_stat == 'max' and water_stat == 'on':
		state = 'max'
	else:
		state = 'off'
	return plc_img.format(state)

def display_generator_img(generator_stat,turbine_stat):
	self_stat = generator_stat
	turbine_stat = turbine_stat
	plc_img = 'generator_{}.png'
	if self_stat == 'on' and turbine_stat == 'on':
		state = 'on'
	else:
		state = 'off'
	return plc_img.format(state)

def display_pylon_img(pylon_stat,generator_stat,turbine_stat,fuel_stat):
	self_stat = pylon_stat
	generator_stat = generator_stat
	turbine_stat = turbine_stat 
	fuel_stat = fuel_stat
	plc_img = 'pylon_{}.png'
	if self_stat == 'on' and generator_stat == 'on' and fuel_stat == 'low' and turbine_stat == 'on':
		state = 'low'
	elif self_stat == 'on' and generator_stat == 'on' and fuel_stat == 'norm' and turbine_stat == 'on':
		state = 'norm'
	elif self_stat == 'on' and generator_stat == 'on' and fuel_stat == 'max' and turbine_stat == 'on':
		state = 'max'
	else:
		state = 'off'
	return plc_img.format(state)
