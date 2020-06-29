from flask import render_template, url_for, flash, redirect, request
from EyeTracking import app, db
import os

@app.route('/')
def hello_world():
    return 'Hello, World!'