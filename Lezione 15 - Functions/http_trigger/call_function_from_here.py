from requests import post

r = post('https://europe-west1-mamei-test2-382313.cloudfunctions.net/hello_http',json={'name':'marco'})
print(r.status_code)
print(r.text)

