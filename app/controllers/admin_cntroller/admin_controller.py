from flask import Blueprint, request, jsonify
from app.Models.admin import Admin_user
from app.extension import db
from flask_jwt_extended import jwt_required
from app.status_code import HTTP_200_OK, HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND, HTTP_500_INTERNAL_SERVER_ERROR

admin = Blueprint('admin', __name__, url_prefix='/api/v1/admins')


# GET ALL ADMINS
@admin.route('/', methods=['GET'])
@jwt_required()
def get_all_admins():
    admins = Admin_user.query.all()
    results = [{
        "id": admin.id,
        "userName": admin.userName,
        "emailAddress": admin.emailAddress,
        "contacts": admin.contacts,
        "role": admin.role
    } for admin in admins]
    return jsonify(results), HTTP_200_OK


# GET SINGLE ADMIN
@admin.route('/<int:admin_id>', methods=['GET'])
@jwt_required()
def get_admin(admin_id):
    admin = Admin_user.query.get(admin_id)
    if not admin:
        return jsonify({'error': 'Admin not found'}), HTTP_404_NOT_FOUND

    return jsonify({
        "id": admin.id,
        "userName": admin.userName,
        "emailAddress": admin.emailAddress,
        "contacts": admin.contacts,
        "role": admin.role
    }), HTTP_200_OK


# UPDATE ADMIN
@admin.route('/<int:admin_id>', methods=['PUT'])
@jwt_required()
def update_admin(admin_id):
    admin = Admin_user.query.get(admin_id)
    if not admin:
        return jsonify({'error': 'Admin not found'}), HTTP_404_NOT_FOUND

    data = request.json or {}

    try:
        admin.userName = data.get('userName', admin.userName)
        admin.contacts = data.get('contacts', admin.contacts)
        admin.emailAddress = data.get('emailAddress', admin.emailAddress)
        admin.role = data.get('role', admin.role)

        db.session.commit()

        return jsonify({'message': 'Admin updated successfully'}), HTTP_200_OK
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), HTTP_500_INTERNAL_SERVER_ERROR


# DELETE ADMIN
@admin.route('/<int:admin_id>', methods=['DELETE'])
@jwt_required()
def delete_admin(admin_id):
    admin = Admin_user.query.get(admin_id)
    if not admin:
        return jsonify({'error': 'Admin not found'}), HTTP_404_NOT_FOUND

    try:
        db.session.delete(admin)
        db.session.commit()
        return jsonify({'message': 'Admin deleted successfully'}), HTTP_200_OK
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), HTTP_500_INTERNAL_SERVER_ERROR
