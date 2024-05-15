from requests import post
import json
from datetime import datetime

url = 'https://europe-west8-plcoud2024.cloudfunctions.net/hello_http'
#$.post(url,{'data':JSON.stringify(dati)},
r = post(url,data={'data':json.dumps({'time':str(datetime.now()),'value':[465,45]})})
print(r.status_code)
print(r.text)


