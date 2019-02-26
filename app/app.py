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
import time


app = Flask(__name__, static_url_path='')
app.secret_key = 'secret_key_'


@app.route('/')
def index_route():
	return render_template('index.html')

@app.route('/world')
def world_route():
	plc_imgs = get_plc_img()
	water_time()
	plc_rate()
	prod_on()
	print(plc_imgs)
	return render_template('world.html',plc_imgs=plc_imgs)

if __name__ == '__main__':
    app.run(debug=True,host="0.0.0.0",port=9001)
