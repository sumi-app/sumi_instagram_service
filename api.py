import json

from eve import Eve
from flask import request
from flask_cors import CORS
import os
from dotenv import load_dotenv

from message_sender.msg_sender import send_message_to_account

app = Eve()

CORS(app)
app.config['JSON_AS_ASCII'] = False

load_dotenv()


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
    bot_msg = get_arg_from_request(request, 'bot_msg')
    send_message_to_account(ig_login, bot_msg)

    response = app.response_class(
        response=json.dumps(ig_login, ensure_ascii=False, indent=4),
        status=200,
        mimetype='application/json'
    )
    return response


# @app.route('/parse')
# def parse_users():
#     account = parse_accounts()
#
#     response = app.response_class(
#         response=json.dumps(account, ensure_ascii=False, indent=4),
#         status=200,
#         mimetype='application/json'
#     )
#     return response


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=os.environ.get('PORT', 5000))
