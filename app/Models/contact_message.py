from app.extension import db
from datetime import datetime
class Contact(db.Model):
    __tablename__ = 'contacts'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    name = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(20), nullable=False)
    subject = db.Column(db.String(255), nullable=False)
    message = db.Column(db.String(50), nullable=False)
    received_on = db.Column(db.String(150), nullable=False)
    status = db.Column(db.DateTime, default=datetime.now)
