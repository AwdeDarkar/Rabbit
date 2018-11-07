"""
init
====================================================================================================

Initialize the app for use in Flask.

----------------------------------------------------------------------------------------------------

**Created**
    11.05.18
**Updated**
    11.06.18 by Darkar
**Author**
    Darkar
**Copyright**
    This code is Free and Open Source for any purpose; it is provided as-is without warranty.
"""

import os

from flask import Flask
from flask import g
from flask import request

from .database import manage_db
from .predict.api_functions import process_api_call

def create_app(test_config=None):
    """ Create the Flask app """
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY="dev",
        DATABASE=os.path.join(app.instance_path, "rabbit.sqlite"),
        )

    if test_config is None:
        #Load the instance config, if exists, when not testing
        app.config.from_pyfile("config.py", silent=True)
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    manage_db.init_app(app)

    @app.route("/")
    def index(): #pylint: disable=unused-variable
        """ Return a static greeting page """
        with open("./rabbit/site/index.html", "r") as f:
            html = f.read()
        return html

    @app.route("/api", methods=["POST"])
    def web_api(): #pylint: disable=unused-variable
        """ Accept POST requests here """
        conn = manage_db.get_db()
        response = process_api_call(conn, request) #pylint: disable=undefined-variable
        if response: return response
        return "{ 'error' : 'true' }"

    return app
