from shared import user_routine_dict
from flask import Flask, jsonify, request

app = Flask(__name__)


@app.route('/api/login', methods=['GET'])
def get_login_data():
    username = request.args.get('username')
    password = request.args.get('password')
    data = {'exist':False,
            'match':False}
    if username not in user_routine_dict:
        return jsonify(data)
    else:
        if password == user_routine_dict[username]['password']:
            data = {'exist':True,
                    'match':True}
        else:
            data = {'exist':True,
                    'match':False}
    return jsonify(data)


@app.route('/api/signup', methods=['POST'])
def get_sigup_data():
    username = request.args.get('username')
    password = request.args.get('password')
    data = {'exist':False}
    if username not in user_routine_dict:
        user_routine_dict[username] = {}
        user_routine_dict[username]['password'] = password
        user_routine_dict[username]['routine'] = {}
        return jsonify(data)
    else:
        data = {'exist':True}
    return jsonify(data)

@app.route('/api/gallery', methods=['GET'])
def get_gallery_data():
    global user_routine_dict
    username = str(request.args.get('username'))
    
    routine_num = len(user_routine_dict[username]['routine'].keys())
    routine = user_routine_dict[username]['routine']

    data = {'routine_num':routine_num,'routine':routine}
    return jsonify(data)


@app.route('/api/add_routine', methods=['POST'])
def add_routine_data():
    global user_routine_dict
    username = request.json['username']
    routine_num = 'routine'+str(request.json['routine_num'])
    routine_info = request.json['routine_info']
    user_routine_dict[username]['routine'][routine_num] = routine_info
    return 'success'
