
from flask import Flask,redirect,url_for, request
from flask_login import LoginManager, current_user, login_user, logout_user, login_required, UserMixin

class User(UserMixin):
    def __init__(self, username):
        super().__init__()
        self.id = username
        self.username = username

app = Flask(__name__)
login = LoginManager(app)
login.login_view = '/static/login.html'
app.config['SECRET_KEY'] = 'ciao'


@app.route('/')
def root():
    return redirect('/static/index.html')


@app.route('/main')
@login_required
def index():
    return 'Hi '+current_user.username


usersdb = {
    'marco':'mamei'
}

@login.user_loader
def load_user(username):
    if username in usersdb:
        return User(username)
    return None

@app.route('/login', methods=['POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('/main'))
    username = request.values['u']
    password = request.values['p']
    if username in usersdb:
        if password == usersdb[username]:
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

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)

