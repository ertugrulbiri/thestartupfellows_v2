import logging
import os

from flask import request, jsonify, render_template

from app import create_app
from config.config import Config

app = create_app(Config)
# CORS(app)


if __name__ == '__main__':
    app.config["CORS_ORIGINS"] = ["http://thestartupfellows.com"]
    app.run(host='0.0.0.0')


from werkzeug.exceptions import InternalServerError

@app.errorhandler(InternalServerError)
def handle_exception(e):
    e = e.original_exception

    # slack.send_slack_error_message(f"Hey Guys, I am tg exception hunter! I caught \n ",
    #                                f"'{type(e).__name__}: {e}'")
    return 'InternalServer Error', 500

@app.errorhandler(404)
def not_found(e):
    return 404
