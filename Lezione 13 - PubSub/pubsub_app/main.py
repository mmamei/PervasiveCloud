
from flask import Flask,request
from google.cloud import pubsub_v1
from json import loads
from base64 import b64decode
from secret import project_id,topic_name

app = Flask(__name__)

@app.route('/',methods=['GET'])
def main():
    return 'ok'

@app.route('/pubsub/write',methods=['GET'])
def pubsub_write():
    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path(project_id, topic_name)
    r = publisher.publish(topic_path, b'message 1', key1='val1', key2='val2')
    return r.result()

@app.route('/pubsub/push',methods=['POST'])
def pubsub_push():
    print('ricevuto payload',flush=True)
    dict = loads(request.data.decode('utf-8'))
    print(dict,flush=True)
    msg = b64decode(dict['message']['data']).decode('utf-8')
    print(msg)
    return 'OK',200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)

