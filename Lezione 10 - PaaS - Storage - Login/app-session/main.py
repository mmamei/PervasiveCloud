
from flask import Flask,redirect, request, session


usersdb = {
    'marco':'mamei'
}


app = Flask(__name__)
app.config['SECRET_KEY'] = 'ciao'
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

