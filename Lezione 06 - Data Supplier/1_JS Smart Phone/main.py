
from flask import Flask, render_template, request, redirect, url_for
import os
from datetime import datetime


# requires pyopenssl

app = Flask(__name__)

@app.route('/',methods=['GET'])
def main():
    return redirect(url_for('static', filename='index.html'))

@app.route('/upload_data',methods=['POST'])
def upload_data():
    i = request.form.get("i")
    j = request.form.get("j")
    k = request.form.get("k")
    print(i,j,k)

    return 'saved'

@app.route('/upload',methods=['POST'])
def upload():
    # check if the post request has the file part

    file = request.files['file']

    now = datetime.now()
    current_time = now.strftime("%H_%M_%S")

    file.save(os.path.join(f'tmp/test_{current_time}.png'))
    return 'saved'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True, ssl_context='adhoc')

