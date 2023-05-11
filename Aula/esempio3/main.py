from flask import Flask,request,render_template,redirect,url_for
import json
from google.cloud import firestore
from flask_login import LoginManager, current_user, login_user, logout_user, login_required, UserMixin
from secret import secret_key

class User(UserMixin):
    def __init__(self, username):
        super().__init__()
        self.id = username
        self.username = username
        self.par = {}

app = Flask(__name__)
app.config['SECRET_KEY'] = secret_key
local = True

login = LoginManager(app)
login.login_view = '/static/login.html'


@login.user_loader
def load_user(username):
    db = firestore.Client.from_service_account_json('credentials.json') if local else firestore.Client()
    user = db.collection('utenti').document(username).get()
    if user.exists:
        return User(username)
    return None

@app.route('/',methods=['GET','POST'])
@app.route('/main',methods=['GET','POST'])
@app.route('/sensors',methods=['GET'])
def main():
    db = firestore.Client.from_service_account_json('credentials.json') if local else firestore.Client()
    s = []
    for doc in db.collection('sensors').stream():
        s.append(doc.id)
    return json.dumps(s), 200


@app.route('/sensors/<s>',methods=['POST'])
def add_data(s):
    val = float(request.values['val'])
    db = firestore.Client.from_service_account_json('credentials.json') if local else firestore.Client()
    doc_ref = db.collection('sensors').document(s)
    entity = doc_ref.get()
    if entity.exists and 'values' in entity.to_dict():
        v = entity.to_dict()['values']
        v.append(val)
        doc_ref.update({'values':v})
    else:
        doc_ref.set({'values':[val]})
    return 'ok',200


@app.route('/sensors/<s>',methods=['GET'])
def get_data(s):
    db = firestore.Client.from_service_account_json('credentials.json') if local else firestore.Client()
    entity = db.collection('sensors').document(s).get()
    if entity.exists:
        return json.dumps(entity.to_dict()['values']),200
    else:
        return 'sensor not found',404

@app.route('/graph/<s>',methods=['GET'])
@login_required
def graph_data(s):
    db = firestore.Client.from_service_account_json('credentials.json') if local else firestore.Client()
    entity = db.collection('sensors').document(s).get()
    if entity.exists:
        d = []
        d.append(['Number',s])
        t = 0
        for x in entity.to_dict()['values']:
            d.append([t,x])
            t+=1
        return render_template('graph.html',sensor=s,data=json.dumps(d))
    else:
        return redirect(url_for('static', filename='sensor404.html'))

@app.route('/login', methods=['POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('/main'))
    username = request.values['u']
    password = request.values['p']

    db = firestore.Client.from_service_account_json('credentials.json') if local else firestore.Client()
    user = db.collection('utenti').document(username).get()
    if user.exists and user.to_dict()['password']==password:
        login_user(User(username))
        next_page = request.args.get('next')
        if not next_page:
            next_page = '/main'
        return redirect(next_page)
    return redirect('/static/login.html')


@app.route('/logout')
def logout():
    logout_user()
    return redirect('/')


@app.route('/adduser', methods=['GET','POST'])
@login_required
def adduser():
    if current_user.username == 'marco':
        if request.method == 'GET':
            return redirect('/static/adduser.html')
        else:
            username = request.values['u']
            password = request.values['p']
            db = firestore.Client.from_service_account_json('credentials.json') if local else firestore.Client()
            user = db.collection('utenti').document(username)
            user.set({'username':username,'password':password})
            return 'ok'
    else:
        return redirect('/')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)

