
from flask import Flask
from secret import user, password
import mysql.connector
from mysql.connector.constants import ClientFlag
app = Flask(__name__)

@app.route('/',methods=['GET'])
def main():
    return 'ok'

@app.route('/sql',methods=['GET'])
def sql():
    config = {
        'user': user,
        'password': password,
        'host': '34.79.175.127',
        'client_flags': [ClientFlag.SSL],
        'ssl_ca': 'secret/server-ca.pem',
        'ssl_cert': 'secret/client-cert.pem',
        'ssl_key': 'secret/client-key.pem',
        'database':'testdb'
    }
    cnxn = mysql.connector.connect(**config)
    cursor = cnxn.cursor()
    cursor.execute("select * from users")
    out = cursor.fetchall()
    result = ''
    for row in out:
        result+=str(row)+'<br>'
    return result


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8081, debug=True)

