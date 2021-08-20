import json

from eve import Eve
from flask import request
from selenium.webdriver.chrome.webdriver import WebDriver
from flask import jsonify
from flask_cors import CORS
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import os

app = Eve()

CORS(app)
app.config['JSON_AS_ASCII'] = False


@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers',
                         'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods',
                         'GET,PUT,POST,DELETE,OPTIONS')
    return response


def get_arg_from_request(req, arg_name: str):
    if arg_name in req.args.keys():
        return req.args[arg_name]

    return None


@app.route('/write')
def write_to_user():
    ig_login = get_arg_from_request(request, 'login')
    response = app.response_class(
        response=json.dumps(ig_login, ensure_ascii=False, indent=4),
        status=200,
        mimetype='application/json'
    )
    return response


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=os.environ.get('PORT', 5000))
