#pip install opencv-python
import cv2 as cv
import base64
import json
from datetime import  datetime

import requests
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
# define a video capture object
vid = cv.VideoCapture(0)
i = 0
last_sent = ''
while True:
    # Capture the video frame by frame
    ret, frame = vid.read()
    frame = cv.resize(frame, (640, 480))  # resize the frame
    # Display the resulting frame
    cv.imshow('frame', frame)

    #save locally
    cv.imwrite(f'tmp/frame{i}.jpg', frame)
    i += 1

    #send via post
    now = datetime.now()
    current_time = now.strftime("%H_%M_%S")
    if current_time != last_sent:
        print(f'send image @ {current_time}')
        _, encimg = cv.imencode(".png ", frame)
        img_byte = base64.b64encode(encimg).decode("utf-8")
        img_json = json.dumps({'image': img_byte}).encode('utf-8')
        response = requests.post('http://localhost:8080/face', data=img_json, verify=False)
        last_sent = current_time



    # the 'q' button is set as the quitting button
    if cv.waitKey(1) & 0xFF == ord('q'):
        break

# After the loop release the cap object
vid.release()
# Destroy all the windows
cv.destroyAllWindows()
