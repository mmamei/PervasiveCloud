from flask import Flask,request,redirect
from requests import get

app = Flask(__name__)


@app.route('/base',methods=['GET','POST'])
def base():
    return 'ok'

@app.route('/',methods=['GET','POST'])
def main():
    r = get(f'{request.url}api/f1')
    return f'<h1>Ciao {r.json()["response"]}</h1>'

@app.route('/test',methods=['GET','POST'])
def main2():
    return redirect('/api/f1')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8081, debug=True)

