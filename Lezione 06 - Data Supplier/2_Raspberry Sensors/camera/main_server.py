
from flask import Flask, render_template, request, redirect, url_for
import os
from datetime import datetime
import numpy as np
import cv2 as cv
import base64
import json


#import logging
#log = logging.getLogger('werkzeug')
#log.setLevel(logging.ERROR)

app = Flask(__name__)


@app.route('/',methods=['GET'])
def main():
    return redirect(url_for('static', filename='index.html'))


@app.route('/upload',methods=['POST'])
def upload():
    data = request.data.decode('utf-8')
    data_json = json.loads(data)
    image = data_json['image']
    image_dec = base64.b64decode(image)
    data_np = np.frombuffer(image_dec, dtype='uint8')
    img = cv.imdecode(data_np, 1)
    now = datetime.now()
    current_time = now.strftime("%H_%M_%S")
    cv.imwrite(f'img/test_{current_time}.png', img)
    return 'saved'


# download from https://raw.githubusercontent.com/opencv/opencv/master/data/haarcascades/haarcascade_frontalface_default.xml
face_cascade = cv.CascadeClassifier('haarcascade_frontalface_default.xml')
@app.route('/face',methods=['POST'])
def face():
    data = request.data.decode('utf-8')
    data_json = json.loads(data)
    image = data_json['image']
    image_dec = base64.b64decode(image)
    data_np = np.frombuffer(image_dec, dtype='uint8')
    img = cv.imdecode(data_np, 1)

    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.1, 4)
    for (x, y, w, h) in faces:
        cv.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
    print(f'N. people = {len(faces)}')

    now = datetime.now()
    current_time = now.strftime("%H_%M_%S")
    cv.imwrite(f'img/test_{current_time}.png', img)
    return 'saved'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)

