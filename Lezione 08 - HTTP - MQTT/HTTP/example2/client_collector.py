from requests import get, post

base_url = 'http://34.140.248.158:80'


r = get(f'{base_url}/sensors')
sensors = r.json()
print(sensors)
for s in sensors:
    r = get(f'{base_url}/sensors/{s}')
    print(s,r.json())