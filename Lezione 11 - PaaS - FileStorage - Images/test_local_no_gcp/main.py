
from flask import Flask, request, redirect, url_for
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)

@app.route('/',methods=['GET'])
def main():
    return 'ok'


@app.route('/upload',methods=['GET','POST'])
def upload():
    if request.method == 'GET':
        return redirect(url_for('static', filename='form.html'))
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            return redirect(request.url)
        fname = secure_filename(file.filename) # opzionale
        print(fname)
        file.save(os.path.join('files',fname))
        return 'saved '+fname


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)

