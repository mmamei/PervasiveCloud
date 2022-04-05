from requests import get, post

base_url = 'http://34.140.248.158:80'


for i in range(2):
    r = post(f'{base_url}/sensors/s1',data={'val': i})

for i in range(2):
    r = post(f'{base_url}/sensors/s2',data={'val': i})

print('done')
