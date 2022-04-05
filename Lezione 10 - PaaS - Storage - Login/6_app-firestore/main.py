
from flask import Flask
from google.cloud import firestore

app = Flask(__name__)

@app.route('/',methods=['GET'])
def main():
    return 'ok'

@app.route('/fire',methods=['GET'])
def fire():

    db = firestore.Client()
    result = ''
    for doc in db.collection('persone').stream():
     result += (f'{doc.id} --> {doc.to_dict()}<br>')
    return result


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)

