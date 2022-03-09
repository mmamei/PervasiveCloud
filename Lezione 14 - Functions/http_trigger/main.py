def hello_http(request):
    request_json = request.get_json(silent=True)
    if request_json and 'name' in request_json:
        name = request_json['name']
    else:
        name = 'world'
    return f'Hello {name}!'
