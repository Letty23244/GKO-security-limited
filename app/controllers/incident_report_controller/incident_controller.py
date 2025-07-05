from flask import Blueprint, jsonify, request
from app.Models.incident_report import Incident_report 
from app.extension import db
from flask_jwt_extended import jwt_required
from app.status_code import  HTTP_200_OK , HTTP_400_BAD_REQUEST , HTTP_500_INTERNAL_SERVER_ERROR , HTTP_201_CREATED , HTTP_404_NOT_FOUND
from datetime import datetime

incident_bp = Blueprint('incident', __name__, url_prefix='/api/v1/incidents')

@incident_bp.route('/', methods=['GET'])
@jwt_required()
def get_incidents():
    try:
        incidents = Incident_report.query.all()
        data = []
        for inc in incidents:
            data.append({
                'id': inc.id,
                'description': inc.description,
                'incident_date': inc.incident_date,
                'severity': inc.severity,
                'status': inc.status,
                'reported_by_guard_id': inc.reported_by_guard_id,
                'station_id': inc.station_id
            })
        return jsonify(data), HTTP_200_OK
    except Exception as e:
        return jsonify({'error': str(e)}), HTTP_500_INTERNAL_SERVER_ERROR

@incident_bp.route('/', methods=['POST'])
@jwt_required()
def create_incident():
    data = request.get_json()
    try:
        incident = Incident_report(
            description=data['description'],
            incident_date=data['incident_date'],
            severity=data['severity'],
            status=data['status'],
            reported_by_guard_id=data['reported_by_guard_id'],
            station_id=data['station_id']
        )
        db.session.add(incident)
        db.session.commit()
        return jsonify({'message': 'Incident report created successfully'}), HTTP_201_CREATED
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), HTTP_500_INTERNAL_SERVER_ERROR

@incident_bp.route('/<int:id>', methods=['PUT'])
@jwt_required()
def update_incident(id):
    data = request.get_json()
    incident = Incident_report.query.get_or_404(id)
    try:
        incident.description = data.get('description', incident.description)
        incident.incident_date = data.get('incident_date', incident.incident_date)
        incident.severity = data.get('severity', incident.severity)
        incident.status = data.get('status', incident.status)
        incident.reported_by_guard_id = data.get('reported_by_guard_id', incident.reported_by_guard_id)
        incident.station_id = data.get('station_id', incident.station_id)

        db.session.commit()
        return jsonify({'message': 'Incident report updated successfully'}), HTTP_200_OK
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), HTTP_500_INTERNAL_SERVER_ERROR

@incident_bp.route('/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_incident(id):
    incident = Incident_report.query.get_or_404(id)
    try:
        db.session.delete(incident)
        db.session.commit()
        return jsonify({'message': 'Incident report deleted successfully'}), HTTP_200_OK
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), HTTP_500_INTERNAL_SERVER_ERROR
