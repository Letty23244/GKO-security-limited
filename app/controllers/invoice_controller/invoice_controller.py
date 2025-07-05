from flask import Blueprint, jsonify, request
from app.Models.invoice import Invoice
from app.extension import db
from flask_jwt_extended import jwt_required
from app.status_code import  HTTP_200_OK , HTTP_400_BAD_REQUEST , HTTP_500_INTERNAL_SERVER_ERROR , HTTP_201_CREATED , HTTP_404_NOT_FOUND
    
invoice_bp = Blueprint('invoice', __name__, url_prefix='/api/v1/invoices')

@invoice_bp.route('/', methods=['GET'])
@jwt_required()
def get_invoices():
    try:
        invoices = Invoice.query.all()
        data = []
        for inv in invoices:
            data.append({
                'id': inv.id,
                'invoice_date': inv.invoice_date,
                'amount_paid': inv.amount_paid,
                'amount_due': inv.amount_due,
                'due_date': inv.due_date,
                'status': inv.status,
                'client_id': inv.client_id
            })
        return jsonify(data), HTTP_200_OK
    except Exception as e:
        return jsonify({'error': str(e)}), HTTP_500_INTERNAL_SERVER_ERROR

@invoice_bp.route('/', methods=['POST'])
@jwt_required()
def create_invoice():
    data = request.get_json()
    try:
        invoice = Invoice(
            invoice_date=data['invoice_date'],
            amount_paid=data['amount_paid'],
            amount_due=data['amount_due'],
            due_date=data['due_date'],
            status=data['status'],
            client_id=data['client_id']
        )
        db.session.add(invoice)
        db.session.commit()
        return jsonify({'message': 'Invoice created successfully'}), HTTP_201_CREATED
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), HTTP_500_INTERNAL_SERVER_ERROR

@invoice_bp.route('/<int:id>', methods=['PUT'])
@jwt_required()
def update_invoice(id):
    data = request.get_json()
    invoice = Invoice.query.get_or_404(id)
    try:
        invoice.invoice_date = data.get('invoice_date', invoice.invoice_date)
        invoice.amount_paid = data.get('amount_paid', invoice.amount_paid)
        invoice.amount_due = data.get('amount_due', invoice.amount_due)
        invoice.due_date = data.get('due_date', invoice.due_date)
        invoice.status = data.get('status', invoice.status)
        invoice.client_id = data.get('client_id', invoice.client_id)

        db.session.commit()
        return jsonify({'message': 'Invoice updated successfully'}), HTTP_200_OK
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), HTTP_500_INTERNAL_SERVER_ERROR

@invoice_bp.route('/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_invoice(id):
    invoice = Invoice.query.get_or_404(id)
    try:
        db.session.delete(invoice)
        db.session.commit()
        return jsonify({'message': 'Invoice deleted successfully'}), HTTP_200_OK
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), HTTP_500_INTERNAL_SERVER_ERROR
