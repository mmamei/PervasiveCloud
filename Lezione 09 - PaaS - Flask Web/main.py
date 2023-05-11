
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

@app.route('/',methods=['GET'])
def main():
    #return 'ciao marco'
    user = {'username': 'Marco'}
    list = [1,2,3,4,5]
    return render_template('index.html', title='Home', user=user, list=list)

# http form
@app.route('/form')
def root():
    return redirect(url_for('static', filename='login.html'))


# parameters in the url
@app.route('/urlpar/<par>',methods=['GET'])
def urlpar(par):
    user = {'username': par}
    list = [1, 2, 3, 4, 5]
    return render_template('index.html', title='Home', user=user, list=list)

# http get parameters
@app.route('/reqpar',methods=['GET','POST'])
def getpar():
    print(request.values)
    user = {'username': request.values['name']}
    return render_template('index.html', title='Home', user=user, list=[])


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)

