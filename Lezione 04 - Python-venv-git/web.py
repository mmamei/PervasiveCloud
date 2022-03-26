
from flask import Flask, redirect, url_for

app = Flask(__name__)

@app.route('/',methods=['GET'])
def main():
    return 'ciao'

@app.route('/home')
def home():
    return redirect(url_for('static', filename='home.html'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)

