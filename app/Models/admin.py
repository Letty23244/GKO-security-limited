from app.extension import db
from datetime import datetime
class Admin_user(db.Model):
    __tablename__ = 'admin_users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    userName = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    emailAddress = db.Column(db.String(50), nullable=False)
    contacts = db.Column(db.String(150), nullable=False)
    role = db.Column(db.String(150), nullable=False)
    lastLogin = db.Column(db.DateTime, default=datetime.now)

    def __init__(self, userName, emailAddress, password, role, lastLogin, contacts):
        self.userName = userName
        self.emailAddress = emailAddress
        self.password = password
        self.contacts = contacts
        self.role = role
        self.lastLogin = lastLogin
