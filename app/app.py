#!/usr/bin/env python

from flask import Flask
from flask import abort
from flask import flash
from flask import g
from flask import jsonify
from flask import make_response
from flask import redirect
from flask import render_template
from flask import request
from flask import session
from reg_reader import *
from water_timer import *
from world import *
import time
import threading


app = Flask(__name__, static_url_path='')
app.secret_key = 'secret_key_'


@app.route('/')
def index_route():
	return render_template('index.html')

@app.route('/world')
def world_route():
	plc_stat = get_plc_stat()
	plc_img = display_plc_img()
#	plc_rate()
#	prod_on()
#	water_time() -- how do I not call after page reloads? 
	print(plc_img,plc_stat)
	return render_template('world.html',plc_img=plc_img)

if __name__ == '__main__':
    app.run(debug=True,host="0.0.0.0",port=9001)
