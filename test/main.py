####################################################################################
################################# LIBRERIE E SETUP #################################
####################################################################################
import math

from requests import post
from secret import secret
import cv2 as cv
import datetime
import time
import os

#url del server di gcp
base_url = 'https://ccp-claudiocomp.ew.r.appspot.com'

# Load the cascade
face_cascade = cv.CascadeClassifier('haarcascade_frontalface_default.xml')

# To capture video from webcam.
cap = cv.VideoCapture(0)
cap.set(2, 760)
last_check = 0
last_photo = 0
nameimages = [] #lista immagini create
# To use a video file as input
#cap = cv.VideoCapture('filename.mp4')

####################################################################################
############################ FUNZIONAMENTO DEL SENSORE #############################
####################################################################################

while True:
    # Read and make up the frame
    _, img = cap.read()
    text = "Width: " + str(cap.get(3)) + " Height: " + str(cap.get(4))
    datet = str(datetime.datetime.now())
    frame = cv.putText(img, datet, (10, 50), cv.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2, cv.LINE_AA)
    # Convert to grayscale
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

    # Detect the faces
    faces = face_cascade.detectMultiScale(gray, 1.1, 4)
    # Draw the rectangle around each face
    for (x, y, w, h) in faces:
        cv.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)

    # Show Display
    cv.imshow('img', img)

####################################################################################
######################### CREAZIONE E INVIO FILE OUTPUT ############################
####################################################################################

    # Controlla il tempo ogni 5 seconds
    t = int(time.time())
    if t%5 == 0 and t != last_check:
        last_check = t
        #print(t)

        #IL NOME DEL SENSORE DEVE ESSERE CAMBIATO AD OGNI DUPLICAZIONE DEL CODICE DI INPUT
        #ANCHE IL LINK DI INVIO FILE ALLA RIGA 71
        value = "Sensor 4 * {} * {} *".format(len(faces), datet)
        all = datet[0:-7]                              #GIORNO E DATA
        prenum = datet.replace(":", "_")[0:-7]         #GIORNO E DATA IN FORMATO SALVABILE
        num = prenum.replace(" ", "_")
        date = datet.split(" ")[0]                     #DATA
        hms = all.split(" ")[1]                        #ORA
        day = int(datet.split(" ")[0].split("-")[2])   #giorno
        month = int(datet.split(" ")[0].split("-")[1]) #mese
        hour = int(datet.split(" ")[1].split(":")[0])  #ora
        min = int(datet.split(" ")[1].split(":")[1])   #min
        sec = math.floor(float(datet.split(" ")[1].split(":")[2]))        #sec
        print(value,all,num,date,day,month,hour,min,sec)

        #invia i dati 3 volte al minuto
        if sec>=16 and sec<=23 or sec>=36 and sec<=43 or sec>=54 and sec<=58:
            nameimage = "frame_sensor4_{}.jpg".format(num)
            cv.imwrite(nameimage, img)
            files = {'file': open(nameimage, 'rb')}
            r = post(f'{base_url}/sensors/sensor4'
                                                      , data={'all': num, 'day': day, 'month': month,
                                                      'hour': hour, 'min': min, 'sec': sec, 'hms': hms,
                                                      'value': len(faces), 'secret': secret}, files=files)
            print('Done: {}'.format(value))
            nameimages.append(nameimage)      #lista nomi immagini create per poi eliminarle

####################################################################################
############################## SPEGNIMENTO DEL SENSORE #############################
####################################################################################

    # Stop if 'escape' key is pressed
    k = cv.waitKey(30) & 0xff
    if k == 27:
        for name in nameimages:
            os.remove(name) #non elimina l'ultimo frame, da eliminare manualmente
        break

# Release the VideoCapture object
cap.release()