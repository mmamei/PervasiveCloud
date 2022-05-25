from requests import post

r = post('https://europe-west1-jssensors.cloudfunctions.net/hello_http',json={'name':'marco'})
print(r.status_code)
print(r.text)

