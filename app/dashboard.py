from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from app.auth import login_required
from app import db
from app.models import Questions
# from app.db import get_db

bp = Blueprint('blog', __name__)

@bp.route('/')
def index():
    questions = []
    stmt = db.select(Questions)
    results = db.session.execute(stmt)
    for question_obj in results.scalars():
        questions.append(question_obj)
        print('question_obj.field_code: ', question_obj.field_code)
        
    return render_template('dashboard/index.html', questions=questions)