from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

bcrypt= Bcrypt()
db = SQLAlchemy()

def connect_db(app):
    """connect to the database"""
    
    db.app= app
    db.init_app(app)
    
class User(db.Model):
    """Site user"""
    
    __tablename__= 'users'
    
    username= db.Column(db.String(20), nullable= False, primary_key=True)
    password= db.Column(db.String(50), nullable=False)
    email= db.Column(db.String(50), unique=True, nullable= False)
    first_name= db.Column(db.String(30), nullable=False)
    last_name= db.Column(db.String(30), nullable=False)