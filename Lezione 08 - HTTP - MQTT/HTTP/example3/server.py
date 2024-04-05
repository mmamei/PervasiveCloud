from flask import Flask,request,redirect,url_for
import json

app = Flask(__name__)

db = {}

@app.route('/graph', methods=['GET'])
def graph():
    return redirect(url_for('static', filename='graph.html'))



@app.route('/sensors',methods=['GET'])
def sensors():
    return json.dumps(list(db.keys())), 200


@app.route('/sensors/<s>',methods=['POST'])
def add_data(s):
    data = request.values['data']
    val = float(request.values['val'])
    if s in db:
        db[s].append((data,val))
    else:
        db[s] = [(data,val)]
    return 'ok',200

@app.route('/sensors/<s>',methods=['GET'])
def get_data(s):
    if s in db:
        # return json.dumps(db[s])
        r = []
        for i in range(len(db[s])):
            r.append([i,db[s][i][1]])
        return json.dumps(r),200
    else:
        return 'sensor not found',404


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)

