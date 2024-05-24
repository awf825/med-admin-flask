# https://flask.palletsprojects.com/en/3.0.x/tutorial/install/
# brew services start mysql && mysql -u root
# flask --app app run --debug 
import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        # SECRET_KEY is used by Flask and extensions to keep data safe. 
        # It’s set to 'dev' to provide a convenient value during development, 
        # but it should be overridden with a random value when deploying.
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # overrides the default configuration with values taken from the config.py file 
        # in the instance folder if it exists. For example, when deploying, this can 
        # be used to set a real SECRET_KEY
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://root@localhost/med_diet_dbv3"
    
    db.init_app(app)

    with app.app_context():
        db.create_all()

    from . import auth, dashboard

    app.register_blueprint(auth.bp)
    app.register_blueprint(dashboard.bp)
    app.add_url_rule('/', endpoint='index')

    # a simple page that says hello
    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    return app