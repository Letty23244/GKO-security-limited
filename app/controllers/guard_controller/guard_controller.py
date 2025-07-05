from flask import Blueprint, jsonify, request
from app.Models.guard import Guard 
from app.extension import db
from flask_jwt_extended import jwt_required
from app.status_code import  HTTP_200_OK , HTTP_400_BAD_REQUEST , HTTP_500_INTERNAL_SERVER_ERROR , HTTP_201_CREATED , HTTP_404_NOT_FOUND
from datetime import datetime

guard = Blueprint('guard', __name__, url_prefix='/api/v1/guards')

@guard.route('/', methods=['GET'])
@jwt_required()
def get_guards():
    try:
        guards = Guard.query.all()
        data = []
        for guard in guards:
            data.append({
                'id': guard.id,
                'firstName': guard.firstName,
                'lastName': guard.lastName,
                'gender': guard.gender,
                'date_of_birth': guard.date_of_birth,
                'contacts': guard.contacts,
                'email': guard.email,
                'rank': guard.rank,
                'status': guard.status,
                'hire_date': guard.hire_date
            })
        return jsonify(data), HTTP_200_OK
    except Exception as e:
        return jsonify({'error': str(e)}), HTTP_500_INTERNAL_SERVER_ERROR

@guard.route('/', methods=['POST'])
@jwt_required()
def create_guard():
    data = request.get_json()
    try:
        guard = Guard(
            firstName=data['firstName'],
            lastName=data['lastName'],
            gender=data['gender'],
            date_of_birth=data['date_of_birth'],
            contacts=data['contacts'],
            email=data['email'],
            rank=data['rank'],
            status=data['status'],
            hire_date=data['hire_date']
        )
        db.session.add(guard)
        db.session.commit()
        return jsonify({'message': 'Guard created successfully'}), HTTP_201_CREATED
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), HTTP_500_INTERNAL_SERVER_ERROR

@guard.route('/<int:id>', methods=['PUT'])
@jwt_required()
def update_guard(id):
    data = request.get_json()
    guard = Guard.query.get_or_404(id)
    try:
        guard.firstName = data.get('firstName', guard.firstName)
        guard.lastName = data.get('lastName', guard.lastName)
        guard.gender = data.get('gender', guard.gender)
        guard.date_of_birth = data.get('date_of_birth', guard.date_of_birth)
        guard.contacts = data.get('contacts', guard.contacts)
        guard.email = data.get('email', guard.email)
        guard.rank = data.get('rank', guard.rank)
        guard.status = data.get('status', guard.status)
        guard.hire_date = data.get('hire_date', guard.hire_date)

        db.session.commit()
        return jsonify({'message': 'Guard updated successfully'}), HTTP_200_OK
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), HTTP_500_INTERNAL_SERVER_ERROR

@guard.route('/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_guard(id):
    guard = Guard.query.get_or_404(id)
    try:
        db.session.delete(guard)
        db.session.commit()
        return jsonify({'message': 'Guard deleted successfully'}), HTTP_200_OK
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), HTTP_500_INTERNAL_SERVER_ERROR
