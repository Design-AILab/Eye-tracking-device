from flask import Flask, render_template, url_for, flash, redirect, request, jsonify, session
from EyeTracking import app, db
import os
from EyeTracking.models import Tracked_Data
from flask_uploads import UploadSet, configure_uploads, IMAGES, ALL
from werkzeug.utils import secure_filename
import pathlib

import numpy as np
import matplotlib.pyplot as plt
import matplotlib
# check git issue https://github.com/matplotlib/matplotlib/issues/14304
matplotlib.use('agg')

# Storage for Images
# upload limit
app.config['MAX_CONTENT_LENGTH'] = 32 * 1024 * 1024 # 16 megabytes
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

photos = UploadSet('photos', IMAGES)
IMAGE_DIRECTORY = '/static/uploads'
app.config['UPLOADED_PHOTOS_DEST'] = "EyeTracking"+IMAGE_DIRECTORY
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
configure_uploads(app, photos)

def allowed_file(filename):
        return '.' in filename and \
               filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# plotting functions 
def in_frame(pos, data):
    '''
    This coordinate checks if a data point falls within a given boundary
    '''
    x, y = data[0], data[1]
    # check x direction
    if x > pos[1] or x < pos[3]:
        return False
    # check y direction
    if y < pos[0] or y > pos[2]:
        return False
    return True

def map_heatmap(data, pos, path):
    # only keep data within the image
    within_boundary = []
    for d in data:
        if in_frame(pos, d):
            within_boundary.append(d)
    x = []
    y = []
    for xx,yy in data:
        x.append(xx)
        y.append(yy)
    height_width_ratio = (pos[2] - pos[0])/(pos[1] - pos[3])
    bins = [np.arange(min(x), max(x), 20), np.arange(min(y), max(y), 20)]
    plt.figure(figsize=(9*height_width_ratio, 9))
    plt.hist2d(x,y, cmap='gray', bins=bins)
    plt.gca().invert_yaxis()
    plt.axis('off')
    plt.savefig(path)
    return path

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
		return render_template('tracking.html', img=img_data.design, id=data_id)
	return render_template('tracking.html', img=None, id=None)

@app.route('/tracked_coordinates', defaults={'data_id': None}, methods=['POST'])
@app.route('/tracked_coordinates/<data_id>', methods=['POST'])
def tracked_coordinates(data_id):
	# print(request.json)
	coords = request.json['data']
	image_positions = request.json['image position']
	data = coords
	# session['data'] = data
	# session['image position'] = image_positions
	if data_id:
		img_data = db.session.query(Tracked_Data).filter(Tracked_Data.id == data_id).first()
		img_data.tracked_coords = data
		img_data.image_pos = image_positions
		db.session.commit()
	return redirect(url_for('show_coords', data_id=data_id))
	#return render_template('results.html', length=len(data), data=data)

@app.route('/show_results', defaults={'data_id': None})
@app.route('/show_results/<data_id>')
def show_coords(data_id):
	#data = session['data']
	# save data to database
	# if data_id:
	# 	img_data = db.session.query(Tracked_Data).filter(Tracked_Data.id == data_id).first()
	# 	img_data.tracked_coords = data
	# 	db.session.commit()
	if data_id:
		img_data = db.session.query(Tracked_Data).filter(Tracked_Data.id == data_id).first()
		if img_data:
			data = img_data.tracked_coords
			positions = img_data.image_pos
			in_path = img_data.design
			#out_path = IMAGE_DIRECTORY + '/heatmap_' + data_id
			map_heatmap(data, positions, 'EyeTracking/static/uploads/heatmap_' + data_id)
			out_path = '/static/uploads/heatmap_' + data_id + '.png'
			return render_template('results.html', length=len(data), data=data, input=in_path, output=out_path)
	return render_template('results.html', length=None, data=None, input=None, output=None)
