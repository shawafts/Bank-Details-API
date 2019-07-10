from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask import Blueprint
from flask_restful import Api
import os


# Initialize application
app = Flask(__name__, static_folder=None)

#config_filename = "config"
app_settings = os.getenv(
    'APP_SETTINGS',
    'app.config.DevelopmentConfig'
)
#Loading configurations
app.config.from_object(app_settings)


# Initialize Flask Sql Alchemy and Marshmallow
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy(app)

from flask_marshmallow import Marshmallow
ma = Marshmallow(app)


# Import the application views
from app import views

api_bp = Blueprint('api', __name__)
api = Api(api_bp)


#Adding Routes to api
from app.resources.auth import  NewToken #RegisterUser, LoginUser, LogOutUser,
api.add_resource(NewToken, '/auth/register')

from app.resources.bankinfo import InfoByIfscCode,InfoByNameAndCity
api.add_resource(InfoByIfscCode, '/bankdetails/ifsc')
api.add_resource(InfoByNameAndCity, '/bankdetails/name_city')

#Registering API Blueprint
app.register_blueprint(api_bp, url_prefix='/v1')



