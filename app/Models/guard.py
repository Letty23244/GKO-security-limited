from app.extension import db
from datetime import datetime
class Guard(db.Model):
    __tablename__ = 'guards'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    firstName = db.Column(db.String(20), nullable=False)
    lastName = db.Column(db.String(20), nullable=False)
    gender = db.Column(db.String(255), nullable=False)
    date_of_birth = db.Column(db.String(50), nullable=False)
    contacts = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    rank = db.Column(db.String(150), nullable=False)
    status = db.Column(db.String(150), nullable=False)
    hire_date = db.Column(db.String(150), nullable=False)

    duty_schedules = db.relationship('DutySchedule', backref='guard', lazy=True)
    incident_reports = db.relationship('Incident_report', backref='reporting_guard', lazy=True)