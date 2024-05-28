from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, jsonify
)
from werkzeug.exceptions import abort

from app.auth import login_required
from app import db
from app.models import (
    Questions, QuestionAnswerOptions, 
    QuestionCategories, QuestionFieldTypes,
    Forms, QuestionAnswerSubmissions,
    QuestionAnswers
)
# from app.db import get_db

bp = Blueprint('dashboard', __name__)

@bp.route('/')
def index():
    questions = []
    stmt = db.select(Questions)
    results = db.session.execute(stmt)
    for question_obj in results.scalars():
        questions.append(question_obj)
        print('question_obj.field_code: ', question_obj.field_code)
        
    return render_template('dashboard/index.html', questions=questions)

@bp.route('/work', methods=('GET'))
def work():
    questions = []
    stmt = db.select(Questions)
    results = db.session.execute(stmt)
    for question_obj in results.scalars():
        questions.append(question_obj)
        print('question_obj.field_code: ', question_obj.field_code)
        
    return jsonify(questions)

@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        error = None

        if not request.form["question_text"]:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            q = Questions(
                question_text=request.form["question_text"],
                field_code=request.form["field_code"],
            )
            db.session.add(q)
            db.session.commit()
            db.commit()
            return redirect(url_for('dashboard.index'))

    return render_template('dashboard/create.html')

@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    q = get_question(id)
    categories = get_categories()
    field_types = get_field_types()
    forms = get_forms()

    if request.method == 'POST':
        error = None

        if not request.form["question_text"]:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            stmt = (
                db.update(Questions)
                .where(Questions.question_id == id)
                .values(
                    question_text=request.form["question_text"],
                    field_code=request.form["field_code"],
                    category_id=request.form["category_id"],
                    field_type_id=request.form["field_type_id"],
                    form_id=request.form["form_id"]
                )
            )
            db.session.execute(stmt)

            return redirect(url_for('dashboard.index'))

    return render_template(
        'dashboard/update.html', 
        question=q, categories=categories, field_types=field_types,
        forms=forms
    )

@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    get_question(id)
    stmt = delete(Questions).where(Questions.question_id == id)
    db.execute('DELETE FROM questions WHERE id = ?', (id,))
    db.session.execute(stmt)
    return redirect(url_for('dashboard.index'))

# select 
# count(qa.answer_score) as answer_number, 
# SUM(qa.answer_score) as score, 
# qc.category_display_name, 
# qc.question_category_id
# from question_answer_submissions qas 
# join question_answers qa ON qa.question_answer_submission_id = qas.submission_id 
# JOIN questions q ON q.question_id = qa.question_id 
# join question_categories qc on qc.question_category_id = q.category_id 
# where qc.question_category_id != 9 
# and 
# qas.user_id = :user_id 
# group by qc.question_category_id

def get_question(id, check_author=True):
    stmt = db.select(Questions).where(Questions.question_id == id)
    result = db.session.execute(stmt)
    q = None
    for q_obj in result.scalars():
        q = q_obj

    if q is None:
        abort(404, f"Question id {id} doesn't exist.")

    # if check_author and q['author_id'] != g.user['id']:
    #     abort(403)

    return q

def get_categories():
    stmt = db.select(QuestionCategories)
    categories = []
    results = db.session.execute(stmt)
    for cat_obj in results.scalars():
        categories.append(cat_obj)

    return categories

def get_field_types():
    stmt = db.select(QuestionFieldTypes)
    field_types = []
    results = db.session.execute(stmt)
    for ft_obj in results.scalars():
        field_types.append(ft_obj)

    return field_types

def get_forms():
    stmt = db.select(Forms)
    forms = []
    results = db.session.execute(stmt)
    for f_obj in results.scalars():
        forms.append(f_obj)

    return forms

