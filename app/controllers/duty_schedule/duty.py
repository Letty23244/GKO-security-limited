from flask import Blueprint, jsonify, request
from app.Models.duty_schedule import DutySchedule
from app.extension import db
from flask_jwt_extended import jwt_required
from app.status_code import  HTTP_200_OK , HTTP_400_BAD_REQUEST , HTTP_500_INTERNAL_SERVER_ERROR , HTTP_201_CREATED , HTTP_404_NOT_FOUND
from datetime import datetime

duty_schedules = Blueprint('duty_schedule', __name__, url_prefix='/api/v1/duty_schedules')



# Get all duty schedules
@duty_schedules.route('/', methods=['GET'])
@jwt_required()
def get_all_duties():
    try:
        duties = DutySchedule.query.all()
        result = []
        for duty in duties:
            result.append({
                'id': duty.id,
                'shift_date': duty.shift_date,
                'start_time': duty.start_time,
                'end_time': duty.end_time,
                'shift_type': duty.shift_type,
                'guard_id': duty.guard_id,
                'station_id': duty.station_id
            })
        return jsonify(result), HTTP_200_OK
    except Exception as e:
        return jsonify({'error': str(e)}), HTTP_500_INTERNAL_SERVER_ERROR

# Create new duty schedule
@duty_schedules.route('/', methods=['POST'])
@jwt_required()
def create_duty():
    data = request.get_json()
    shift_date = data.get('shift_date')
    start_time = data.get('start_time')
    end_time = data.get('end_time')
    shift_type = data.get('shift_type')
    guard_id = data.get('guard_id')
    station_id = data.get('station_id')

    if not all([shift_date, start_time, end_time, shift_type, guard_id, station_id]):
        return jsonify({'error': 'All fields are required'}), HTTP_400_BAD_REQUEST

    try:
        duty = DutySchedule(
            shift_date=shift_date,
            start_time=start_time,
            end_time=end_time,
            shift_type=shift_type,
            guard_id=guard_id,
            station_id=station_id
        )
        db.session.add(duty)
        db.session.commit()
        return jsonify({'message': 'Duty schedule created'}), HTTP_201_CREATED
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), HTTP_500_INTERNAL_SERVER_ERROR

# Update duty schedule
@duty_schedules.route('/<int:id>', methods=['PUT'])
@jwt_required()
def update_duty(id):
    duty = DutySchedule.query.get_or_404(id)
    data = request.get_json()

    duty.shift_date = data.get('shift_date', duty.shift_date)
    duty.start_time = data.get('start_time', duty.start_time)
    duty.end_time = data.get('end_time', duty.end_time)
    duty.shift_type = data.get('shift_type', duty.shift_type)
    duty.guard_id = data.get('guard_id', duty.guard_id)
    duty.station_id = data.get('station_id', duty.station_id)

    try:
        db.session.commit()
        return jsonify({'message': 'Duty schedule updated'}), HTTP_200_OK
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), HTTP_500_INTERNAL_SERVER_ERROR

# Delete duty schedule
@duty_schedules.route('/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_duty(id):
    duty = DutySchedule.query.get_or_404(id)
    try:
        db.session.delete(duty)
        db.session.commit()
        return jsonify({'message': 'Duty schedule deleted'}), HTTP_200_OK
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), HTTP_500_INTERNAL_SERVER_ERROR

