from app.extension import db
from datetime import datetime

class Order(db.Model):
    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key=True)
    customer_name = db.Column(db.String(100))
    total_price = db.Column(db.Float)
    order_date = db.Column(db.DateTime, default=datetime.utcnow)
