# https://towardsdatascience.com/sql-on-the-cloud-with-python-c08a30807661
# https://www.w3schools.com/python/python_mysql_select.asp

import mysql.connector
from mysql.connector.constants import ClientFlag
from secret import user,password
config = {
    'user': user,
    'password': password,
    'host': '34.79.175.127',
    'client_flags': [ClientFlag.SSL],
    'ssl_ca': 'secret/server-ca.pem',
    'ssl_cert': 'secret/client-cert.pem',
    'ssl_key': 'secret/client-key.pem'
}


# now we establish our connection
cnxn = mysql.connector.connect(**config) ## unpack config dict in parameters

#cursor = cnxn.cursor()  # initialize connection cursor
#cursor.execute('CREATE DATABASE testdb')  # create a new 'testdb' database
#cnxn.close()  # close connection because we will be reconnecting to testdb

config['database'] = 'testdb'  # add new database to config dict
cnxn = mysql.connector.connect(**config)
cursor = cnxn.cursor()

#cursor.execute("create table users (name VARCHAR(255),surname VARCHAR(255))")
#cnxn.commit()  # this commits changes to the database

#cursor.execute("insert into users (name, surname) VALUES ('marco','mamei')")
#cnxn.commit()  # and commit changes

cursor.execute("select * from users")
out = cursor.fetchall()
print([i[0] for i in cursor.description])
for row in out:
    print(row[0])

