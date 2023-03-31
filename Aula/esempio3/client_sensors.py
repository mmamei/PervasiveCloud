from requests import get, post
import time

#base_url = 'http://localhost:80'
base_url = 'https://mamei-test2-382313.appspot.com'

sensor = 's8'

for i in range(1000):
    print(sensor,'invio....')
    r = post(f'{base_url}/sensors/{sensor}',data={'val': i})
    time.sleep(1)

print('done')
