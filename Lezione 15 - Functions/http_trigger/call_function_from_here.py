from requests import post

r = post('https://europe-west8-plcoud2024.cloudfunctions.net/hello_http',json={'name':'marco'})
print(r.status_code)
print(r.text)

