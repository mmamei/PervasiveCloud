from flask import Flask,request,render_template,redirect,url_for
import json
from google.cloud import firestore

app = Flask(__name__)

@app.route('/sensors',methods=['GET'])
def main():
    #db = firestore.Client.from_service_account_json('credentials.json')
    db = firestore.Client()
    s = []
    for doc in db.collection('sensors').stream():
        s.append(doc.id)
    return json.dumps(s), 200


@app.route('/sensors/<s>',methods=['POST'])
def add_data(s):
    val = float(request.values['val'])
    #db = firestore.Client.from_service_account_json('credentials.json')
    db = firestore.Client()
    doc_ref= db.collection('sensors').document(s)
    entity = doc_ref.get()
    if entity.exists and 'values' in entity.to_dict():
        v = entity.to_dict()['values']
        v.append(val)
        doc_ref.update({'values':v})
    else:
        doc_ref.set({'values':[val]})
    return 'ok',200


@app.route('/sensors/<s>',methods=['GET'])
def get_data(s):
    #db = firestore.Client.from_service_account_json('credentials.json')
    db = firestore.Client()
    entity = db.collection('sensors').document(s).get()
    if entity.exists:
        return json.dumps(entity.to_dict()['values']),200
    else:
        return 'sensor not found',404

@app.route('/graph/<s>',methods=['GET'])
def graph_data(s):
    db = firestore.Client.from_service_account_json('credentials.json')
    # db = firestore.Client()
    entity = db.collection('sensors').document(s).get()
    if entity.exists:
        d = []
        d.append(['Number',s])
        t = 0
        for x in entity.to_dict()['values']:
            d.append([t,x])
            t+=1
        return render_template('graph.html',sensor=s,data=json.dumps(d))
    else:
        return redirect(url_for('static', filename='sensor404.html'))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)

