from flask import Blueprint, jsonify, request
from app.Models.contact_message import Contact
from app.extension import db
from flask_jwt_extended import jwt_required
from app.status_code import *
from datetime import datetime

contact_message = Blueprint('contact', __name__, url_prefix='/api/v1/contacts')

# Get all contact messages
@contact_message.route('/', methods=['GET'])
@jwt_required()
def get_contacts():
    try:
        contacts = Contact.query.all()
        data = []
        for contact in contacts:
            data.append({
                'id': contact.id,
                'name': contact.name,
                'email': contact.email,
                'subject': contact.subject,
                'message': contact.message,
                'received_on': contact.received_on,
                'status': contact.status
            })
        return jsonify(data), HTTP_200_OK
    except Exception as e:
        return jsonify({'error': str(e)}), HTTP_500_INTERNAL_SERVER_ERROR

# Create a new contact message
@contact_message.route('/', methods=['POST'])
def create_contact():
    data = request.get_json()
    name = data.get('name')
    email = data.get('email')
    subject = data.get('subject')
    message = data.get('message')

    if not name or not email or not subject or not message:
        return jsonify({'error': 'All fields are required'}), HTTP_400_BAD_REQUEST

    try:
        contact = Contact(
            name=name,
            email=email,
            subject=subject,
            message=message,
            received_on=datetime.utcnow()
        )
        db.session.add(contact)
        db.session.commit()

        return jsonify({'message': 'Contact message submitted successfully'}), HTTP_201_CREATED
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), HTTP_500_INTERNAL_SERVER_ERROR

# Update contact message status

# 
@contact_message.route('/edit/<int:id>', methods =['PUT'])
def updatecontact_message(id):

    try:

        data = request.get_json()
        contact_message = contact_message.query.get(id)

        if not contact_message :
            return jsonify ({
                'error':"contact_message not found"
            }),HTTP_404_NOT_FOUND
        
        contact_message.name = data.get('name', contact_message.name)
        contact_message.email = data.get('last_name',contact_message.email)
        contact_message.subject = data.get('email',contact_message.subject)
        contact_message.message = data.get('contact',contact_message.message)
        contact_message.recieved_on = data.get('last_name',contact_message.recieved_on)
        contact_message.status = data.get('email',contact_message.status)

        db.session.commit()

        return jsonify({
            'message': f"The contact_message id of {id} is updated successfully",
            'student':{
                'id': contact_message.id,
                'name':contact_message.name,
                'email': contact_message.email,
                'message': contact_message.message,
                'recieved_on': contact_message.recieved_on
            }
        }), HTTP_200_OK
    
    except Exception as e:
        return jsonify ({
            'error': str(e)
        }),HTTP_500_INTERNAL_SERVER_ERROR


# Delete a contact message
@contact_message.route('/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_contact(id):
    contact = Contact.query.get_or_404(id)

    try:
        db.session.delete(contact)
        db.session.commit()
        return jsonify({'message': 'Contact message deleted'}), HTTP_200_OK
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), HTTP_500_INTERNAL_SERVER_ERROR