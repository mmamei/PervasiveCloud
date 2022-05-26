def graph(request):
    from flask import render_template
    from google.cloud import firestore
    import json

    def read_all(sensor):
        db = firestore.Client()
        data = []
        for doc in db.collection(sensor).stream():
            x = doc.to_dict()
            data.append([x['time'].split(' ')[0], float(x['value'])])
        return json.dumps(data)

    sensor = request.values['sensor']
    data = json.loads(read_all(sensor))
    data.insert(0, ['Time', 'Pm10'])
    return render_template('graph.html', data=data)
