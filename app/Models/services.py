from app.extension import db
from datetime import datetime
class Services(db.Model):
    __tablename__ = 'services'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(255), nullable=False)
    icon_url = db.Column(db.String(255), nullable=False)
    price_rate = db.Column(db.String(150), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now)