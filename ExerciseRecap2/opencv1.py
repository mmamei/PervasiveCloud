#pip install opencv-python
import cv2 as cv
import base64
import json
import time

import requests
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)



from google.cloud import pubsub_v1
from secret import project_id,topic_name
from google.auth import jwt
import  json

service_account_info = json.load(open("credentials.json"))
audience = "https://pubsub.googleapis.com/google.pubsub.v1.Publisher"
credentials = jwt.Credentials.from_service_account_info(
    service_account_info, audience=audience
)
publisher = pubsub_v1.PublisherClient(credentials=credentials)
topic_path = publisher.topic_path(project_id, topic_name)

try:
    topic = publisher.create_topic(request={"name": topic_path})
    print(f"Created topic: {topic.name}")
except Exception as e:
    print(e)


# define a video capture object
vid = cv.VideoCapture(0)
i = 0
last_sent = 0
while True:
    # Capture the video frame by frame
    ret, frame = vid.read()
    frame = cv.resize(frame, (640, 480))  # resize the frame
    # Display the resulting frame
    cv.imshow('frame', frame)

    #save locally
    # cv.imwrite(f'tmp/frame{i}.jpg', frame)
    # i += 1

    #send via post
    current_time = int(time.time())


    if current_time - last_sent > 5:
        print(f'send image @ {(current_time)}')
        _, encimg = cv.imencode(".png ", frame)
        img_byte = base64.b64encode(encimg).decode("utf-8")
        img_json = json.dumps({'image': img_byte}).encode('utf-8')
        print(img_json[0:100])

        r = publisher.publish(topic_path, img_json)
        last_sent = current_time

    # the 'q' button is set as the quitting button
    if cv.waitKey(1) & 0xFF == ord('q'):
        break

# After the loop release the cap object
vid.release()
# Destroy all the windows
cv.destroyAllWindows()
