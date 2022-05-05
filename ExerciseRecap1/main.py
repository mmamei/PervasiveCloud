
from flask import Flask, request, render_template
from google.cloud import firestore
from secret import secret
app = Flask(__name__)
import json

@app.route('/',methods=['GET'])
def main():
    return 'ok'

@app.route('/sensors/sensor1',methods=['GET'])
def read_all():
    db = firestore.Client.from_service_account_json('credentials.json')
    #db = firestore.Client()
    data = []
    for doc in db.collection('sensor1').stream():
        x = doc.to_dict()
        data.append([x['time'].split(' ')[0],float(x['value'])])
    return json.dumps(data)
    # [['2020-01-01',  40.5],....]


def soglia(s):
    db = firestore.Client.from_service_account_json('credentials.json')
    # db = firestore.Client()
    data = []
    for doc in db.collection('sensor1').stream():
        x = doc.to_dict()
        if float(x['value']) > s:
            data.append(x['time'].split(' ')[0])
    return json.dumps(data)


@app.route('/graph',methods=['GET'])
def graph():
    data = json.loads(read_all())
    data.insert(0,['Time', 'Pm10'])
    return render_template('graph.html',data=data,soglia=json.loads(soglia(80)))


@app.route('/sensors/sensor1',methods=['POST'])
def save_data():
    s = request.values['secret']
    if s == secret:
        time = request.values['time']
        pm10 = request.values['pm10']
        db = firestore.Client.from_service_account_json('credentials.json')
        #db = firestore.Client()
        db.collection('sensor1').document(time).set({'time': time, 'value': pm10})
        return 'ok', 200
    else:
        return '', 401


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)

