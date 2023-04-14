from flask import Flask,request
app = Flask(__name__)

basePath = '/api'

@app.route(basePath+'/f1',methods=['GET','POST'])
def f1():
    return {'response':'marco'}


#
# Use these libraries to generate tokens automatically
# https://pyjwt.readthedocs.io/en/latest/
# see file test_jwt here
#

autTokens = [
    'secret1', 'secret2'
]

@app.route(basePath+'/f2',methods=['GET','POST'])
def f2():
    aut = request.headers.get('Authorization')
    if aut in autTokens:
        return {'response': 'ciao'}
    return {'message': 'token error'}, 401


@app.route(basePath+'/f3',methods=['GET','POST'])
def f3():
    aut = request.headers.get('Authorization')
    if aut in autTokens:
        if 'name' in request.values:
            return {'response': f"ciao {request.values['name']}"}
        else:
            return {'error': ['name parameter missing']},400
    return {'message': 'token error'}, 401


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)

