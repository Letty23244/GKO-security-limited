from app.extension import db
from datetime import datetime
class Client(db.Model):
    __tablename__ = 'clients'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    firstName = db.Column(db.String(20), nullable=False)
    lastName = db.Column(db.String(20), nullable=False)
    company_name = db.Column(db.String(255), nullable=False)
    address = db.Column(db.String(50), nullable=False)
    contacts = db.Column(db.String(150), nullable=False)
    registered_on = db.Column(db.DateTime, default=datetime.now)

    invoices = db.relationship('Invoice', backref='client', lazy=True)