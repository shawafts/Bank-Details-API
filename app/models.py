from app import db, ma

class BankDetails(db.Model):
    __tablename__ = 'BankDetails'
    #__table_args__ = {"schema": "shawaf"}
    #id = db.Column('id', db.BigInteger, primary_key=True)
    ifsc = db.Column('ifsc', db.VARCHAR(length = 30), primary_key=True)
    bank_id = db.Column('bank_id', db.BigInteger)
    branch = db.Column('branch', db.TEXT)
    address = db.Column('address', db.TEXT) 
    city = db.Column('city', db.TEXT)
    district = db.Column('district', db.TEXT)
    state = db.Column('state', db.TEXT)
    bank_name = db.Column('bank_name', db.TEXT)
    
class BankDetailsSchema(ma.ModelSchema):
#class BankDetailsSchema(ma.Schema):
    class Meta:
        model = BankDetails







