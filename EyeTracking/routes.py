from flask import render_template, url_for, flash, redirect, request
from EyeTracking import app, db
import os

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/tracking')
def tracking():
	return render_template('tracking.html')
