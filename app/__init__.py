from flask import Flask
from .extension import db, migrate, jwt  
from app.controllers.auth_controller.auth_controller import auth
from app.controllers.admin_cntroller.admin_controller import admin
from app.controllers.client_controllers.client_controllers import client

#  Import models 
from app.Models.admin import Admin_user
from app.Models.client import Client
from app.Models.contact_message import Contact
from app.Models.duty_schedule import DutySchedule
from app.Models.guard import Guard
from app.Models.incident_report import Incident_report
from app.Models.invoice import Invoice
from app.Models.services import Services

def create_app():
    app = Flask(__name__)

    # Load config
    app.config.from_object('config.Config')

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)


    # register blue prints
    app.register_blueprint(auth)
    app.register_blueprint(admin)
    app.register_blueprint(client)

    # Default route
    @app.route('/')
    def index():
        return 'Hello, Security App!'

    return app
