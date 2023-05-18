def save_video(event, context):
    import numpy as np
    import cv2 as cv
    import base64
    import json
    import time
    from google.cloud import storage

    client = storage.Client.from_service_account_json('credentials.json')
    bucket = client.get_bucket('video-mamei-test2')

    # print(f'messaggio ricevuto: {msg}')

    dict = json.loads(base64.b64decode(event['data']).decode('utf-8'))  # deserializzazione
    # print(dict, flush=True)
    x = base64.b64decode(dict['image'].encode('utf-8'))
    # converting into numpy array from buffer
    npimg = np.frombuffer(x, dtype=np.uint8)
    img = cv.imdecode(npimg, 1)
    name = str(int(time.time()))
    cv.imwrite('/tmp/test.jpg', img)

    # bucket = client.bucket('upload-mamei-1')
    source_file_name = '/tmp/test.jpg'
    destination_blob_name = f'{name}.jpg'
    blob = bucket.blob(destination_blob_name)
    blob.upload_from_filename(source_file_name)
    # blob.upload_from_string(img)
    print("File {} uploaded to {}.".format(source_file_name, destination_blob_name))









