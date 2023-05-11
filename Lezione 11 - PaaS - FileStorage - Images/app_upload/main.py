
from flask import Flask, request, redirect, url_for, send_file
import os
from werkzeug.utils import secure_filename
from google.cloud import storage
import datetime

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
        fname = secure_filename(file.filename)
        print(fname)
        #file.save(os.path.join('tmp/',fname))

        client = storage.Client.from_service_account_json('credentials.json')
        bucket = client.bucket('upload-mamei-11')
        source_file_name = fname
        destination_blob_name = source_file_name
        blob = bucket.blob(destination_blob_name)

        #blob.upload_from_filename(os.path.join('tmp/',fname))

        blob.upload_from_string(file.read(),content_type=file.content_type)

        return 'File {} uploaded to {}.'.format(source_file_name, destination_blob_name)


@app.route('/retrieve/<fname>',methods=['GET'])
def retrieve(fname):
    storage_client = storage.Client.from_service_account_json('credentials.json')
    bucket = storage_client.bucket('upload-mamei-11')
    blob = bucket.blob(fname)
    blob.download_to_filename(os.path.join('tmp/',fname))
    return send_file(os.path.join('tmp/',fname))


@app.route('/retrieve2/<fname>',methods=['GET'])
def retrieve2(fname):
    storage_client = storage.Client.from_service_account_json('credentials.json')
    bucket = storage_client.bucket('upload-mamei-11')
    blob = bucket.blob(fname)
    # https://cloud.google.com/storage/docs/access-control/signing-urls-with-helpers#code-samples
    serving_url = blob.generate_signed_url(
        version="v4",
        expiration=datetime.timedelta(minutes=15), # This URL is valid for 15 minutes
        method="GET") # Allow GET requests using this URL.
    return redirect(serving_url)

@app.route('/retrieve3',methods=['GET'])
def retrieve3():
    storage_client = storage.Client.from_service_account_json('credentials.json')
    bucket = storage_client.bucket('upload-mamei-11')
    fname = 'test.jpg'
    blob = bucket.blob(fname)
    blob.make_public()
    url = blob.public_url
    return redirect(url)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)

