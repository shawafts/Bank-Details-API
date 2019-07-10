import os
from app.models import db, BankDetails, BankDetailsSchema
basedir = os.path.abspath(os.path.dirname(__file__))
filename = basedir + "/data/bank_branches.csv"


bank_detail_schema = BankDetailsSchema()

def populate_db():
    """
    db.session.connection().connection.set_isolation_level(0)
    db.session.execute('CREATE DATABASE BankDetails')
    db.session.connection().connection.set_isolation_level(1)
    """
    db.create_all()
    fetch_from_csv()

def fetch_from_csv():
    with open(filename) as f:
        content = f.readlines()
    content = [x.strip() for x in content]
    first_line = True
    if BankDetails.query.count() > 9900:
        print("Database is already populated")
        return
    print("Loading data to database...")
    count = 0
    for line in content:
        if first_line:
            first_line = False
            continue
        if count >= 9995:
            return
        line, address = extract_address(line)
        line = line.split(',')

        bank_data = {'ifsc': line[0], 'bank_id' : line[1], 'branch' : line[2], 'address' : address, 'city' : line[3], 'district' : line[4], 'state' : line[5], 'bank_name' : line[6]}
        data, errors = bank_detail_schema.load(bank_data)
        new_data = BankDetails(ifsc = data.ifsc, bank_id = data.bank_id, branch = data.branch, address = data.address, city = data.city, district = data.district, state = data.state, bank_name = data.bank_name)
        if db.session.query(BankDetails.ifsc).filter_by(ifsc=data.ifsc).scalar() is not None:
            continue
        try:
            db.session.add(new_data)
            db.session.commit()
            count += 1
        except Exception as e:
            #pass
            print ("Exception:", e)
        result = bank_detail_schema.dump(BankDetails).data
        #print("Result", result)
    
     
   
def extract_address(line):
        first_part = line.partition('"')[0]
        second_part =  line.partition('"')[2]
        address =  second_part.partition('"')[0]
        line  = first_part + second_part.partition('"')[2][1:]
        return line, address