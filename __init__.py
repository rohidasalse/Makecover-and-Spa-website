
from flask import Flask,session
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from sqlalchemy_utils import database_exists, create_database
app=Flask(__name__,template_folder="Templates")
CORS(app)
app.secret_key='sdx2323@3343zbhcfew3rr3343@@###$2ffr45434'
# app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=30)

from config import Config
app.config.from_object(Config)
db=SQLAlchemy(app) 

from views import *

if not database_exists(app.config['SQLALCHEMY_DATABASE_URI']):
    create_database(app.config['SQLALCHEMY_DATABASE_URI'])

with app.app_context():
        db.create_all()



if __name__=='__main__':
    
    app.run(debug=True,host="0.0.0.0",port=2000)