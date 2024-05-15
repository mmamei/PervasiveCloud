def hello_http(request):
    from flask import render_template
    user = {'username': 'Marco'}

    if 'username' in request.values:
        user['username'] = request.values['username']

    list = [1, 2, 3, 4, 5]
    return render_template('index.html', title='Home', user=user, list=list)
