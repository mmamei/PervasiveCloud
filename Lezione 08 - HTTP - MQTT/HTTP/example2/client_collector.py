from requests import get, post

base_url = 'http://localhost:80'


r = get(f'{base_url}/sensors')
sensors = r.json()
print(sensors)
for s in sensors:
    r = get(f'{base_url}/sensors/{s}')
    print(s,r.json())