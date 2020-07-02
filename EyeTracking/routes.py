from flask import Flask, render_template, url_for, flash, redirect, request, jsonify
from EyeTracking import app, db
import os

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/tracking')
def tracking():
	return render_template('tracking.html')


@app.route('/tracked_coordinates', methods=['POST'])
def tracked_coordinates():
	# print(request.json)
	coords = request.json['data']
	print(coords)
	data = coords
	#return redirect(url_for('show_coords', length=len(data), data=data))
	return render_template('results.html',  length=len(data), data=data)


# @app.route('/show_results/<length>/<data>')
# def show_coords(length, data):
# 	return render_template('results.html', length=int(length), data=data)
