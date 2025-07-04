from app.extension import db
from datetime import datetime
class Invoice(db.Model):
    __tablename__ = 'invoices'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    invoice_date = db.Column(db.String(255), nullable=False)
    amount_paid = db.Column(db.String(50), nullable=False)
    amount_due = db.Column(db.String(150), nullable=False)
    due_date = db.Column(db.String(20), nullable=False)
    status = db.Column(db.String(20), nullable=False)
    client_id = db.Column(db.Integer, db.ForeignKey('clients.id'), nullable=False)
