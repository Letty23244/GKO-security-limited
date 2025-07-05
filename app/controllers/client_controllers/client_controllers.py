from flask import Blueprint, jsonify, request
from app.Models.client import Client
from app.extension import db
from flask_jwt_extended import jwt_required
from app.status_code import  HTTP_200_OK ,HTTP_500_INTERNAL_SERVER_ERROR ,HTTP_201_CREATED ,HTTP_404_NOT_FOUND

client = Blueprint('client', __name__, url_prefix='/api/v1/clients')


@client.route('/', methods=['GET'])
@jwt_required()
def get_all_clients():
    try:
        all_clients = Client.query.all()
        clients_data = []

        for client in all_clients:
            client_info = {
                'id': client.id,
                'firstName': client.firstName,
                'lastName': client.lastName,
                'company': client.company_name,
                'address': client.address,
                'contacts': client.contacts,
                'registered_on': client.registered_on
            }
            clients_data.append(client_info)

        return jsonify(clients_data), HTTP_200_OK

    except Exception as e:
        return jsonify({'error': str(e)}), HTTP_500_INTERNAL_SERVER_ERROR


@client.route('/<int:id>', methods=['GET'])
@jwt_required()
def get_single_client(id):
    try:
        client = Client.query.get_or_404(id)
        client_info = {
            'id': client.id,
            'firstName': client.firstName,
            'lastName': client.lastName,
            'company': client.company_name,
            'address': client.address,
            'contacts': client.contacts,
            'registered_on': client.registered_on
        }
        return jsonify(client_info), HTTP_200_OK

    except Exception as e:
        return jsonify({'error': str(e)}), HTTP_500_INTERNAL_SERVER_ERROR


@client.route('/', methods=['POST'])
@jwt_required()
def create_client():
    data = request.get_json()
    try:
        new_client = Client(
            firstName=data.get('firstName'),
            lastName=data.get('lastName'),
            company_name=data.get('company_name'),
            address=data.get('address'),
            contacts=data.get('contacts'),
            registered_on=data.get('registered_on')
        )
        db.session.add(new_client)
        db.session.commit()
        return jsonify({'message': 'Client created successfully'}), HTTP_201_CREATED

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), HTTP_500_INTERNAL_SERVER_ERROR
    


@client.route('/<int:id>', methods=['PUT'])
@jwt_required()
def update_client(id):
    data = request.get_json()
    
    try:

        data = request.get_json()
        client = client.query.get(id)

        if not client :
            return jsonify ({
                'error':"client not found"
            }),HTTP_404_NOT_FOUND
    
        client.firstName = data.get('firstName', client.firstName)
        client.lastName = data.get('lastName', client.lastName)
        client.company_name = data.get('company_name', client.company_name)
        client.address = data.get('address', client.address)
        client.contacts = data.get('contacts', client.contacts)

        db.session.commit()
        return jsonify({'message': 'Client updated successfully'}), HTTP_200_OK

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), HTTP_500_INTERNAL_SERVER_ERROR


    # Delete the client
@client.route('delete/<int:id>', methods=['DELETE'])
def deleteStudent(id):
    try:
        client = client.query.get(id)

        if not client :
            return jsonify ({
                'error':"Product not found"
            }),HTTP_404_NOT_FOUND
        else :
            # Delete associated clients
            db.session.delete(client)
            db.session.commit()

            return jsonify({
                'message': "client has been deleted successfully"
            }),HTTP_200_OK
        
    except Exception as e:
        return jsonify({
            'error': str(e)
        }),HTTP_500_INTERNAL_SERVER_ERROR