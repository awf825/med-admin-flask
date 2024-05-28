# https://flask-sqlalchemy.palletsprojects.com/en/3.1.x/quickstart/#installation

from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

# from flask_sqlalchemy.orm import DeclarativeBase
# from flask_sqlalchemy.orm import relationship

# class Base(DeclarativeBase):
#     pass

class Users(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, unique=True, nullable=False)
    auth_method_id=db.Column(db.Integer)

class Questions(db.Model):
    question_id = db.Column(db.Integer, primary_key=True)
    question_text = db.Column(db.String, unique=True)
    field_code = db.Column(db.String, unique=True, nullable=False)
    category_id = db.Column(db.Integer, nullable=False)
    field_type_id = db.Column(db.Integer, nullable=False)
    form_id = db.Column(db.Integer, nullable=False)

class QuestionCategories(db.Model):
    question_category_id = db.Column(db.Integer, primary_key=True)
    category_name = db.Column(db.String, unique=True)
    category_display_name = db.Column(db.String, unique=True, nullable=False)
    display_hex_code = db.Column(db.String, unique=True)

class QuestionFieldTypes(db.Model):
    field_type_id = db.Column(db.Integer, primary_key=True)
    field_name = db.Column(db.String, unique=True)

class QuestionAnswerOptions(db.Model):
    option_id = db.Column(db.Integer, primary_key=True)
    field_type_id = db.Column(db.Integer)
    option_text = db.Column(db.String, unique=True)
    answer_value = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String, unique=False, nullable=True)

class Forms(db.Model):
    form_id = db.Column(db.Integer, primary_key=True)
    form_name = db.Column(db.String, unique=True, nullable=False)

class QuestionAnswerSubmissions(db.Model):
    submission_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    form_id = db.Column(db.Integer, nullable=False)
    score = db.Column(db.Integer)

class QuestionAnswers(db.Model):
    answer_id = db.Column(db.Integer, primary_key=True)
    question_id = db.Column(db.Integer, nullable=False)
    question_answer_submission_id = db.Column(db.Integer, nullable=False)
    answer_score = db.Column(db.Integer, nullable=False)
    
    # __tablename__ = 'question_answers'
    # __table_args__ = (
    #     db.PrimaryKeyConstraint('answer_id', 'answer_id'),
    # )


