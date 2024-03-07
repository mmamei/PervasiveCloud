
from flask import Flask, render_template, request, redirect, url_for
from flask import send_from_directory,redirect
app = Flask(__name__)

@app.route('/',methods=['GET'])
def main():
    return redirect(url_for('static', filename='index.html'))

@app.route('/templates/<path:path>')
def send_templates(path):
    return send_from_directory('templates', path)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)

