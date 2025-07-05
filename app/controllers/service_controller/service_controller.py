from flask import Blueprint, jsonify, request
from app.Models.services import Services
from app.extension import db
from flask_jwt_extended import jwt_required
from app.status_code import  HTTP_200_OK , HTTP_400_BAD_REQUEST , HTTP_500_INTERNAL_SERVER_ERROR , HTTP_201_CREATED , HTTP_404_NOT_FOUND

services_bp = Blueprint('services', __name__, url_prefix='/api/v1/services')

@services_bp.route('/', methods=['GET'])
@jwt_required()
def get_services():
    try:
        services = Services.query.all()
        data = []
        for svc in services:
            data.append({
                'id': svc.id,
                'title': svc.title,
                'description': svc.description,
                'icon_url': svc.icon_url,
                'price_rate': svc.price_rate,
                'created_at': svc.created_at
            })
        return jsonify(data), HTTP_200_OK
    except Exception as e:
        return jsonify({'error': str(e)}), HTTP_500_INTERNAL_SERVER_ERROR

@services_bp.route('/', methods=['POST'])
@jwt_required()
def create_service():
    data = request.get_json()
    try:
        service = Services(
            title=data['title'],
            description=data['description'],
            icon_url=data['icon_url'],
            price_rate=data['price_rate']
        )
        db.session.add(service)
        db.session.commit()
        return jsonify({'message': 'Service created successfully'}), HTTP_201_CREATED
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), HTTP_500_INTERNAL_SERVER_ERROR

@services_bp.route('/<int:id>', methods=['PUT'])
@jwt_required()
def update_service(id):
    data = request.get_json()
    service = Services.query.get_or_404(id)
    try:
        service.title = data.get('title', service.title)
        service.description = data.get('description', service.description)
        service.icon_url = data.get('icon_url', service.icon_url)
        service.price_rate = data.get('price_rate', service.price_rate)

        db.session.commit()
        return jsonify({'message': 'Service updated successfully'}), HTTP_200_OK
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), HTTP_500_INTERNAL_SERVER_ERROR

@services_bp.route('/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_service(id):
    service = Services.query.get_or_404(id)
    try:
        db.session.delete(service)
        db.session.commit()
        return jsonify({'message': 'Service deleted successfully'}), HTTP_200_OK
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), HTTP_500_INTERNAL_SERVER_ERROR
