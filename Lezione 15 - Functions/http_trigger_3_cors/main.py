def hello_http(request):
    from google.cloud import firestore
    import json
    if request.method == 'OPTIONS':
        print('------ options')
        # Allows GET requests from any origin with the Content-Type
        # header and caches preflight response for an 3600s
        headers = {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'GET,POST',
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Max-Age': '3600',
            'Access-Control-Allow-Credentials': 'true'
        }
        return ('', 204, headers)

    request_json = json.loads(request.values['data'])
    #request_json = request.data.decode('utf-8')
    print('>>>>>>>>>>>>>>>>>>>>>>>')
    print(request_json)
    # Set CORS headers for the main request
    headers = {
        'Access-Control-Allow-Origin': '*'
    }
    # request_json = {'time':'20-5-2022 14:39:31','value':[45,45]}
    db = firestore.Client()
    db.collection('sensor').document(request_json['time']).set(request_json)
    return ('ok', 200, headers)
