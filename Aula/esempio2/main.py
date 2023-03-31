from flask import Flask,request,render_template,redirect,url_for
import json

app = Flask(__name__)

data = {}

@app.route('/sensors',methods=['GET'])
def main():
    return json.dumps(list(data.keys())), 200


@app.route('/sensors/<s>',methods=['POST'])
def add_data(s):
    val = float(request.values['val'])
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

@app.route('/graph/<s>',methods=['GET'])
def graph_data(s):
    if s in data:
        d = []
        d.append(['Number',s])
        t = 0
        for x in data[s]:
            d.append([t,x])
            t+=1
        return render_template('graph.html',sensor=s,data=json.dumps(d))
    else:
        return redirect(url_for('static', filename='sensor404.html'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)

