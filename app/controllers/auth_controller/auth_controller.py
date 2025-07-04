from flask import Blueprint, request, jsonify
from app.status_code import (
    HTTP_400_BAD_REQUEST,
    HTTP_409_CONFLICT,
    HTTP_500_INTERNAL_SERVER_ERROR,
    HTTP_201_CREATED,
    HTTP_401_UNAUTHORIZED,
    HTTP_200_OK
)
import validators
from app.Models.admin import Admin_user
from app.extension import db, bcrypt
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    get_jwt_identity,
    jwt_required
)

# User blueprint
auth = Blueprint('auth', __name__, url_prefix='/api/v1/auth')

# User registration
@auth.route('/register', methods=['POST'])
def register_auth():
    data = request.json or {}

    userName = data.get('userName')
    emailAddress = data.get('emailAddress')
    contacts = data.get('contacts')
    role = data.get('role')
    password = data.get('password')
    lastLogin = data.get('lastLogin')  # Optional: consider setting server-side if not provided

    # Validate required fields
    if not all([userName, emailAddress, contacts, password]):
        return jsonify({"error": "userName, emailAddress, contacts, and password are required"}), HTTP_400_BAD_REQUEST

    if not role:
        return jsonify({"error": "Enter your user role"}), HTTP_400_BAD_REQUEST

    if len(password) < 8:
        return jsonify({"error": "Password must be at least 8 characters"}), HTTP_400_BAD_REQUEST

    if not validators.email(emailAddress):
        return jsonify({"error": "Email is not valid"}), HTTP_400_BAD_REQUEST

    # Check if email or contacts already exist
    if Admin_user.query.filter_by(emailAddress=emailAddress).first():
        return jsonify({"error": "Email address already in use"}), HTTP_409_CONFLICT

    if Admin_user.query.filter_by(contacts=contacts).first():
        return jsonify({"error": "Contact is already in use"}), HTTP_409_CONFLICT

    try:
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

        # Set lastLogin to current time if not provided
        from datetime import datetime
        if not lastLogin:
            lastLogin = datetime.now()

        new_user = Admin_user(
            userName=userName,
            contacts=contacts,
            emailAddress=emailAddress,
            role=role,
            lastLogin=lastLogin,
            password=hashed_password
        )

        db.session.add(new_user)
        db.session.commit()

        # Use author_info to get user display info (make sure author_info returns string)
        author = f"{new_user.userName} ({new_user.emailAddress})"

        return jsonify({
            'message': f"{author} has been successfully created as a user",
            'Admin_user': {
                "userName": new_user.userName,
                "contacts": new_user.contacts,
                "emailAddress": new_user.emailAddress,
                "role": new_user.role
                # Avoid returning password hash for security reasons
            }
        }), HTTP_201_CREATED

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), HTTP_500_INTERNAL_SERVER_ERROR


# User login
@auth.post('/login')
def login():
    data = request.json or {}
    emailAddress = data.get('emailAddress')
    password = data.get('password')

    if not emailAddress or not password:
        return jsonify({'message': "emailAddress and password are required"}), HTTP_400_BAD_REQUEST

    try:
        user = Admin_user.query.filter_by(emailAddress=emailAddress).first()

        if user and bcrypt.check_password_hash(user.password, password):
            access_token = create_access_token(identity=user.id)
            refresh_token = create_refresh_token(identity=user.id)

            author_info = f"{user.userName} ({user.emailAddress})"

            return jsonify({
                "author": {
                    'id': user.id,
                    'username': author_info,
                    'emailAddress': user.emailAddress,
                    'access_token': access_token,
                    'refresh_token': refresh_token
                }
            }), HTTP_200_OK

        else:
            return jsonify({"message": "Invalid emailAddress or password"}), HTTP_401_UNAUTHORIZED

    except Exception as e:
        return jsonify({'error': str(e)}), HTTP_500_INTERNAL_SERVER_ERROR


# Token refresh route
@auth.route("/token/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh():
    identity = get_jwt_identity()
    access_token = create_access_token(identity=identity)  # identity can be int or string as stored
    return jsonify({'access_token': access_token})
