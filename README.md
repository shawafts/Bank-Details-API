# Bank-Details-API
This application provides APIs to retrieve bank details from the database. This app is heroku deployable.

## API Details

#### 1. Fetch by branch IFSC Code
  This API fetches bank details from database based on the IFSC Code provided
  - URL: http://127.0.0.1:5000/v1/bankdetails/ifsc
  - Content-Type: JSON                          (Mandatory)
  - Data: {'ifsc': '<IFSC CODE>'}               (Mandatory)
  - Authorization Header: JWT Token             (Mandatory)
  
Example:
```sh
curl -H "Content-Type: application/json" \
-H "Authorization: OAuth eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOjYsImlhdCI6MTU2MjY3NjkxNSwiZXhwIjoxNTYyNzYzMzE1fQ.aByVmR-AiBEe5_3cCs3r4j6DfOD0S3ddOtUD641Xfzk" \
-X GET --data '{"ifsc" : "ABHy0065001"}' \
http://127.0.0.1:5000/v1/bankdetails/ifsc
```
Output:
```sh
{
    "Bank Details": {
        "address": "ABHYUDAYA BANK BLDG., B.NO.71, NEHRU NAGAR, KURLA (E), MUMBAI-400024",
        "branch": "RTGS-HO",
        "city": "MUMBAI",
        "state": "MAHARASHTRA",
        "bank_id": 60,
        "bank_name": "ABHYUDAYA COOPERATIVE BANK LIMITED",
        "ifsc": "ABHY0065001",
        "district": "GREATER MUMBAI"
    }
}

```
#### 2. Fetch by bank name and city
This API fetches bank details from database based on the given bank name and city
  - URL: http://127.0.0.1:5000/v1/bankdetails/name_city
  - Content-Type: JSON                    (Mandatory)
  - Data: 
        {'city': '<city>'}                      (Mandatory)
        {'bank_name': '<bank name>'}            (Mandatory)
        {'limit': '<limit>'}                    (Optional)
        {'offset': '<offset>'}                  (Optional)
  - Authorization Header: JWT Token             (Mandatory)

Example:
```sh
curl -H "Content-Type: application/json" \
-H "Authorization: OAuth eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOjYsImlhdCI6MTU2MjY3NjkxNSwiZXhwIjoxNTYyNzYzMzE1fQ.aByVmR-AiBEe5_3cCs3r4j6DfOD0S3ddOtUD641Xfzk"   \
-X GET --data '{"bank_name" : "abhyudaya cooperative bank limited", "city": "mumbai", "limit" : "1", "offset" : "2"}' \
http://127.0.0.1:5000/v1/bankdetails/name_city
```

Output:
```sh
{
    "Bank Details": [
        {
            "address": "KMSPM'S SCHOOL, WADIA ESTATE, BAIL BAZAR-KURLA(W), MUMBAI-400070",
            "branch": "BAIL BAZAR",
            "city": "MUMBAI",
            "state": "MAHARASHTRA",
            "bank_id": 60,
            "bank_name": "ABHYUDAYA COOPERATIVE BANK LIMITED",
            "ifsc": "ABHY0065003",
            "district": "GREATER MUMBAI"
        }
    ]
}
```

#### 3. Create New Token
This API creates new JWT token.
  - URL: http://127.0.0.1:5000/v1/bankdetails/name_city
  - Content-Type: JSON                    (Mandatory)
  - Data: 
        {'name': '<city>'}                (Mandatory)
        {'key': '<bank name>'}            (Mandatory)

Example:
```sh
curl -H "Content-Type: application/json" \
--data '{"name" : "shawaf" , "key": "dasdas324das"}' \
http://127.0.0.1:5000/v1/auth/register
```
