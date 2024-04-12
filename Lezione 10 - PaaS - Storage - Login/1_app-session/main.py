
from flask import Flask,redirect, request, session
from secret import secret_key

usersdb = {
    'marco':'mamei',
    'matteo':'mamei'
}

app = Flask(__name__)

# In order to use session in flask you need to set the secret key in your application settings.
# secret key is a random key used to encrypt your cookies and save send them to the browser.
app.config['SECRET_KEY'] = secret_key

@app.route('/')
def root():
    if 'loggedin' not in session or session["loggedin"]==False:
        return redirect('/static/login.html')
    else:
        return 'Welcome '+session["nome"]


@app.route('/pag2')
def pag2():
    if 'loggedin' not in session or session["loggedin"]==False:
        return redirect('/static/login.html')
    else:
        return 'Welcome 2'+session["nome"]


@app.route('/login', methods=['POST'])
def login():
    username = request.values['u']
    password = request.values['p']
    if username in usersdb and usersdb[username] == password:
        session["loggedin"] = True
        session["nome"] = username
        return redirect('/')
    else:
        return redirect('/static/login.html')

@app.route('/logout')
def logout():
    session["loggedin"] = False
    return redirect('/')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)

