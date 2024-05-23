from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

class Questions(db.Model):
    question_id = db.Column(db.Integer, primary_key=True)
    question_text = db.Column(db.String, unique=True)
    field_code = db.Column(db.String, unique=True, nullable=False)
