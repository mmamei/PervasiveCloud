from requests import get, post

#base_url = 'http://localost:8080'
base_url = 'https://testlez12.appspot.com'
#base_url = 'https://api-dot-mamei-api.appspot.com'

#r = post(f'{host}/api/f1')
#print(r.status_code)
#print(r.json())

#headers = {'Authorization':'secret1'}
#r = post(f'{host}/api/f2',headers=headers)
#print(r.status_code)
#print(r.text)

headers = {'Authorization':'secret1'}
r = post(f'{base_url}/api/f3', headers=headers, data={'name': 'marco'})
print(r.status_code)
print(r.text)

