import requests
url = 'http://192.168.0.101:8080/upload'
files = {'file': open('test.jpg','rb')}
values = {'key1':'value1','key2':'value2'}

r = requests.post(url, files=files, data=values)
print(r.status_code)
print(r.text)
