
from flask import Flask,redirect,url_for, request
from flask_login import LoginManager, current_user, login_user, logout_user, login_required, UserMixin
from secret import secret_key


# For more advanced features: email confirmation, password reset, roles, etc.
# use Flask-Security https://pythonhosted.org/Flask-Security/quickstart.html


# From: https://stackoverflow.com/questions/63231163/what-is-the-usermixin-in-flask
# Flask-login requires a User model with the following properties:
# -- has an is_authenticated() method that returns True if the user has provided valid credentials
# -- has an is_active() method that returns True if the user’s account is active
# -- has an is_anonymous() method that returns True if the current user is an anonymous user
# --has a get_id() method which, given a User instance, returns the unique ID for that object
# UserMixin class provides the implementation of this properties.
# Its the reason you can call for example is_authenticated to check
# if login credentials provide is correct or not instead of having to write a
# method to do that yourself.

class User(UserMixin):
    def __init__(self, username):
        super().__init__()
        self.id = username
        self.username = username

app = Flask(__name__)
app.config['SECRET_KEY'] = secret_key

# The login manager contains the code that lets your application and Flask-Login work together,
# such as how to load a user from an ID, where to send users when they need to log in, and the like.
login = LoginManager(app)
login.login_view = '/static/login.html'


usersdb = {
    'marco':'mamei'
}

@login.user_loader
def load_user(username):
    if username in usersdb:
        return User(username)
    return None


@app.route('/')
def root():
    return redirect('/static/index.html')

@app.route('/main')
@login_required
def index():
    return 'Hi '+current_user.username

@app.route('/main2')
@login_required
def index2():
    return 'Hi2 '+current_user.username

@app.route('/login', methods=['POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('/main'))
    username = request.values['u']
    password = request.values['p']
    next_page = request.values['next']
    if username in usersdb and password == usersdb[username]:
        login_user(User(username))
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

