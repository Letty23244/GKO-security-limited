from app.extension import db
from datetime import datetime
class Incident_report(db.Model):
    __tablename__ = 'incident_reports'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    description = db.Column(db.String(255), nullable=False)
    incident_date = db.Column(db.String(20), nullable=False)
    severity = db.Column(db.String(255), nullable=False)
    status = db.Column(db.String(50), nullable=False)
    reported_by_guard_id = db.Column(db.Integer, db.ForeignKey('guards.id'), nullable=False)
    station_id = db.Column(db.String(150), nullable=False)
