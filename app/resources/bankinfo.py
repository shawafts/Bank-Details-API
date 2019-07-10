from flask import request
from flask_restful import Resource
from sqlalchemy import func, and_
from app.models import db, BankDetails, BankDetailsSchema
from app.resources.helper import response, token_required
bank_details_schema = BankDetailsSchema(many=True)
bank_detail_schema = BankDetailsSchema()

class InfoByIfscCode(Resource):
    """
    Resource class for fetching bank data by IfscCode
    """
    @token_required
    def get(self, user):
        if request.content_type != 'application/json':
            return response('failed', 'Content-type must be json', 400)
        get_data = request.get_json()
        ifsc_code = get_data.get('ifsc')
        
        if ifsc_code is not None:
            bank_details = BankDetails.query.filter(func.lower(BankDetails.ifsc)==func.lower(ifsc_code)).first()
            if not bank_details:
                return response('failed', 'no matching results', 200)
            bank_details = bank_detail_schema.dump(bank_details).data        
            return {"Bank Details": bank_details}, 200
        return response('failed', 'no ifsc code provided', 400)


class InfoByNameAndCity(Resource):
    """
    Resource class for fetching bank details by bank name and city
    """
    @token_required
    def get(self, user):
        if request.content_type != 'application/json':
            return response('failed', 'Content-type must be json', 400)
        get_data = request.get_json()
        bank_name = get_data.get('bank_name')
        city = get_data.get('city')
        limit = get_data.get('limit')
        offset = get_data.get('offset')
        if bank_name is not None and city is not None: 
            count = BankDetails.query.filter(and_(func.lower(BankDetails.bank_name)==func.lower(bank_name), func.lower(BankDetails.city) == func.lower(city))).count()
            if limit is None and offset is None:
                bank_details = BankDetails.query.filter(and_(func.lower(BankDetails.bank_name)==func.lower(bank_name), func.lower(BankDetails.city) == func.lower(city))).all()
            else:
                if offset is None:
                    offset = 0
                else: 
                    offset = int(offset)
                    if offset >= count:
                        return response('failed', 'offset is greater than or equal to available entries', 200)
                if limit is None:
                    limit = count - offset
                else:
                    limit = int(limit)
                    if limit is 0:
                        return response('failed', 'limit should be greater than 0', 200)
            
                bank_details = BankDetails.query.filter(and_(func.lower(BankDetails.bank_name)==func.lower(bank_name), func.lower(BankDetails.city) == func.lower(city))).offset(offset).limit(limit).all()
            
            if len(bank_details) < 1:
                return response('failed', 'No matching results', 200)

            bank_details = bank_details_schema.dump(bank_details).data

            return {"Bank Details": bank_details}, 200
        return response('failed', 'invalid bank_name or city or both', 400)
