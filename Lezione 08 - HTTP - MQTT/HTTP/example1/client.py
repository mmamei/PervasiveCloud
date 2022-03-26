from requests import get, post

base_url = 'http://localhost:80'


r = post(f'{base_url}/')
print(r.status_code)
r = r.json()
print(r)
print(r['response'])
