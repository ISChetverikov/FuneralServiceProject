import os

from flask import Flask
from flaskr.db import mysql
from flaskr.routes import *


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True, template_folder='templates')
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # MySQL configurations
    app.config['MYSQL_DATABASE_USER'] = 'Ilya'
    app.config['MYSQL_DATABASE_PASSWORD'] = '123456'
    app.config['MYSQL_DATABASE_DB'] = 'FuneralAgency'
    app.config['MYSQL_DATABASE_HOST'] = 'localhost'
    mysql.init_app(app)

    app.register_blueprint(routes)
    # a simple page that says hello
    @app.route('/')
    def hello():

        return 'Hello, World!'

    return app