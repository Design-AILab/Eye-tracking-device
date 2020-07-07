from flask import Flask, render_template, url_for, flash, redirect, request, jsonify, session
from EyeTracking import app, db
import os
from EyeTracking.models import Tracked_Data
from flask_uploads import UploadSet, configure_uploads, IMAGES, ALL

# Storage for Images
photos = UploadSet('photos', IMAGES)
IMAGE_DIRECTORY = '/static/uploads'
app.config['UPLOADED_PHOTOS_DEST'] = "." + IMAGE_DIRECTORY
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
configure_uploads(app, photos)

# for the purpose of css
@app.context_processor
def override_url_for():
    return dict(url_for=dated_url_for)

def dated_url_for(endpoint, **values):
    if endpoint == 'static':
        filename = values.get('filename', None)
        if filename:
            file_path = os.path.join(app.root_path,
                                     endpoint, filename)
            values['q'] = int(os.stat(file_path).st_mtime)
    return url_for(endpoint, **values)

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
	data = coords
	session['data'] = data
	return redirect(url_for('show_coords'))
	#return render_template('results.html', length=len(data), data=data)


@app.route('/show_results')
def show_coords():
	data = session['data']
	# save data to database
	print("Goes here")
	coord_data = Tracked_Data(design="", tracked_coords=data)
	db.session.add(coord_data)
	db.session.commit()
	return render_template('results.html', length=len(data), data=data)
