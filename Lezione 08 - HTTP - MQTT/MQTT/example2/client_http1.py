from requests import get, post
import time

base_url = 'http://localhost:80'

sensor = 's3'

for i in range(1000):
    print(sensor,'invio....')
    r = post(f'{base_url}/sensors/{sensor}',data={'val': i})
    time.sleep(5)

print('done')
