from EyeTracking import db
from datetime import datetime

class Tracked_Data(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	design = db.Column(db.String, nullable=True)
	tracked_coords = db.Column(db.PickleType, nullable=True)
	def __repr__(self):
		return f"Tracked_data('{self.id}', '{self.design}')"



