from app.extension import db
from datetime import datetime
class DutySchedule(db.Model):
    __tablename__ = 'duty_schedules'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    shift_date = db.Column(db.String(20), nullable=False)
    start_time = db.Column(db.String(255), nullable=False)
    end_time = db.Column(db.String(50), nullable=False)
    shift_type = db.Column(db.String(150), nullable=False)
    guard_id = db.Column(db.Integer, db.ForeignKey('guards.id'), nullable=False)
    station_id = db.Column(db.String(150), nullable=False)