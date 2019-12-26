import os

from flask import Flask, session
from flask_session import Session
from sqlalchemy.orm import scoped_session, sessionmaker


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    app.config.from_mapping(
        SECRET_KEY='dev')

    # Configure session to use filesystem
    app.config["SESSION_PERMANENT"] = False
    app.config["SESSION_TYPE"] = "filesystem"
    Session(app)

    #import Auth blueprint for authentication logic and pages
    from . import auth
    app.register_blueprint(auth.bp)

    #import books pages blueprint and sets it as the default index
    #from . import blog
    #app.register_blueprint(blog.bp)
    #app.add_url_rule('/', endpoint='index')

    #import books pages blueprint and sets it as the default index
    from . import picolo
    app.register_blueprint(picolo.bp)
    app.add_url_rule('/', endpoint='index')

    return app

    
