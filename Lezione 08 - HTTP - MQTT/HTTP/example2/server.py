from flask import Flask,request
import json

app = Flask(__name__)

data = {}

@app.route('/sensors',methods=['GET'])
def main():
    return json.dumps(list(data.keys())), 200


@app.route('/sensors/<s>',methods=['POST'])
def add_data(s):
    val = request.values['val']
    if s in data:
        data[s].append(val)
    else:
        data[s] = [val]
    print(data)
    return 'ok',200

@app.route('/sensors/<s>',methods=['GET'])
def get_data(s):
    if s in data:
        return json.dumps(data[s]),200
    else:
        return 'sensor not found',404



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)

