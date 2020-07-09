from EyeTracking import app, db
DEBUG = True
if __name__ == "__main__":
	context  = ('cert/server.crt', 'cert/server.key')
	if DEBUG:
		db.drop_all()
	db.create_all()
	app.run('0.0.0.0', port=8100, debug=DEBUG, ssl_context=context)