
from flask import Flask, request, render_template, redirect, url_for
from flask_login import LoginManager, current_user, login_user, logout_user, login_required, UserMixin
from google.cloud import firestore
from secret import secret, secret_key, usersdb
import json
from base64 import b64decode

class User(UserMixin):
    def __init__(self, username):
        super().__init__()
        self.id = username
        self.username = username
        self.par = {}

app = Flask(__name__)
app.config['SECRET_KEY'] = secret_key
login = LoginManager(app)
login.login_view = '/static/login.html'




@login.user_loader
def load_user(username):
    if username in usersdb:
        return User(username)
    return None




@app.route('/',methods=['GET'])
def main():
    return 'ok'

@app.route('/sensors/<sensor>',methods=['GET'])
def read_all(sensor):
    db = firestore.Client.from_service_account_json('credentials.json')
    #db = firestore.Client()
    data = []
    for doc in db.collection(sensor).stream():
        x = doc.to_dict()
        data.append([x['time'].split(' ')[0],float(x['value'])])
    return json.dumps(data)
    # [['2020-01-01',  40.5],....]


def soglia(s):
    db = firestore.Client.from_service_account_json('credentials.json')
    # db = firestore.Client()
    data = []
    for doc in db.collection('sensor1').stream():
        x = doc.to_dict()
        if float(x['value']) > s:
            data.append(x['time'].split(' ')[0])
    return json.dumps(data)


@app.route('/graph/<sensor>',methods=['GET'])
@login_required
def graph(sensor):
    data = json.loads(read_all(sensor))
    data.insert(0,['Time', 'Pm10'])
    return render_template('graph.html',data=data,soglia=json.loads(soglia(80)))


@app.route('/sensors/sensor1',methods=['POST'])
def save_data():
    s = request.values['secret']
    if s == secret:
        time = request.values['time']
        pm10 = request.values['pm10']
        db = firestore.Client.from_service_account_json('credentials.json')
        #db = firestore.Client()
        db.collection('sensor1').document(time).set({'time': time, 'value': pm10})
        return 'ok', 200
    else:
        return '', 401


@app.route('/login', methods=['POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('/'))
    username = request.values['u']
    password = request.values['p']
    if username in usersdb and password == usersdb[username]:
        login_user(User(username), remember=True)
        next_page = request.args.get('next')
        if not next_page:
            next_page = '/'
        return redirect(next_page)
    return redirect('/static/login.html')

@app.route('/logout')
def logout():
    logout_user()
    return redirect('/')


@app.route('/pubsub/receive',methods=['POST'])
def pubsub_push():
    dict = json.loads(request.data.decode('utf-8'))
    print(dict)
    msg = json.loads(dict['message']['attributes']['payload'])
    print(msg)
    # {'sensor': client_id, 'time': t, 'pm10': pm10})
    db = firestore.Client.from_service_account_json('credentials.json')
    db.collection(msg['sensor']).document(msg['time']).set({'time': msg['time'], 'value': msg['pm10']})
    return 'OK',200




if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)

