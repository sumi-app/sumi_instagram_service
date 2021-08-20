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


def get_arg_from_request(request, arg_name: str):
    if arg_name in request.args.keys():
        return request.args[arg_name]

    return None


def str_is_none_or_empty(source: str) -> bool:
    if source == None:
        return True

    return len(source) < 1

@app.route('/applicants/get')
def showApplicants():
    habr_login = get_arg_from_request(request, 'test')
    print(habr_login)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=os.environ.get('PORT', 5000))
