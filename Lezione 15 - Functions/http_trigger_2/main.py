def index(request):
    from flask import render_template
    user = {'username': 'Marco'}
    list = [1, 2, 3, 4, 5]
    return render_template('index.html', title='Home', user=user, list=list)
