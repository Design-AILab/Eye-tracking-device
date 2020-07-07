from flask import Flask, render_template, url_for, flash, redirect, request, jsonify, session
from EyeTracking import app, db
import os
from EyeTracking.models import Tracked_Data
from flask_uploads import UploadSet, configure_uploads, IMAGES, ALL
from werkzeug.utils import secure_filename
import pathlib


# Storage for Images
# upload limit
app.config['MAX_CONTENT_LENGTH'] = 32 * 1024 * 1024 # 16 megabytes

photos = UploadSet('photos', IMAGES)
IMAGE_DIRECTORY = '/static/uploads'
app.config['UPLOADED_PHOTOS_DEST'] = "EyeTracking"+IMAGE_DIRECTORY
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
configure_uploads(app, photos)

def allowed_file(filename):
        return '.' in filename and \
               filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

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


# Upload designs to a project
@app.route('/upload_designs/', methods=['POST'])
def upload_designs():
	file = request.files['file']
	if allowed_file(file.filename):
		filename = photos.save(file) # not just save the filename
		coord_data = Tracked_Data(design=IMAGE_DIRECTORY+"/"+filename, tracked_coords=None)
		db.session.add(coord_data)
		db.session.commit()
		#session['id'] = coord_data.id
		return redirect(url_for('tracking', data_id=coord_data.id))
	return render_template("home.html")


@app.route('/tracking/<data_id>')
def tracking(data_id):
	img_data = db.session.query(Tracked_Data).filter(Tracked_Data.id == data_id).first()
	if img_data:
		return render_template('tracking.html', img=img_data.design)
	return render_template('tracking.html', img=None)


@app.route('/tracked_coordinates', methods=['POST'])
def tracked_coordinates():
	# print(request.json)
	coords = request.json['data']
	image_positions = request.json['image position']
	data = coords
	session['data'] = data
	session['image position'] = image_positions
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
