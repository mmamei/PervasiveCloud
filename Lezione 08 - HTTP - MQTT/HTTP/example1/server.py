from flask import Flask,request,redirect
from requests import get

app = Flask(__name__)


@app.route('/',methods=['GET','POST'])
def main():
    return {'response': 'ciao'}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)
    print('ciao')

