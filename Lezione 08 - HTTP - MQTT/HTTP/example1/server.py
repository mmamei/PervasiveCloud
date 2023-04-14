import json

from flask import Flask,request,redirect
from requests import get

app = Flask(__name__)

data = [
    [1,2],[2,3],[4,5]
]

index = -1

@app.route('/',methods=['GET','POST'])
def main():
    global index
    index += 1
    return json.dumps(data[index])

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)
    print('ciao')

