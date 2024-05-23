# https://flask-sqlalchemy.palletsprojects.com/en/3.1.x/quickstart/#installation

from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

class Users(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, unique=True, nullable=False)
    auth_method_id=db.Column(db.Integer)

class Questions(db.Model):
    question_id = db.Column(db.Integer, primary_key=True)
    question_text = db.Column(db.String, unique=True)
    field_code = db.Column(db.String, unique=True, nullable=False)
