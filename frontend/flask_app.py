from shared import user_dict
from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route('/api')
def index():
    return 'This is the Flask app home page.'

@app.route('/api/login', methods=['GET'])
def get_data():
    global user_dict
    username = request.args.get('username')
    password = request.args.get('password')
    data = {'exist':False,
            'match':False}
    if username not in user_dict:
        return jsonify(data)
    else:
        if password == user_dict[username]:
            data = {'exist':True,
                    'match':True}
        else:
            data = {'exist':True,
                    'match':False}
    return jsonify(data)
