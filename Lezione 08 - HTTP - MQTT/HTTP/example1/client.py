from requests import get, post

base_url = 'http://localhost:80'


r = get(f'{base_url}/')
print(r.status_code)
r = r.json()
print(r)
print(r['response'])
