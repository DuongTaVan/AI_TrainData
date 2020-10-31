import cv2
import numpy as np
import os
import sqlite3
from PIL import Image

face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')
recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read("./recoginzer/trainningData.yml")
#get profile by id from database

def getProfile(id):
    conn = sqlite3.connect("./data.db")
    query = "SELECT * FROM people WHERE id=" + str(id)
    cursor = conn.execute(query)
    profile = None
    for row in cursor:
        profile = row
    conn.close()
    return profile

def check_roll_call():
    conn = sqlite3.connect("./data.db")
    query = "SELECT * FROM people"
    cursor = conn.execute(query)

    check_appearance = {}
    for each in cursor:
        check_appearance[each] = 0
    return check_appearance

list_attendance = check_roll_call()

cap = cv2.VideoCapture(0)
fontface = cv2.FONT_HERSHEY_SIMPLEX

while(True):
    ret, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray)

    for(x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y),(x+w, y+h), (0,255,0), 2)
        roi_gray = gray[y:y+h, x: x+w]
        id, confidence = recognizer.predict(roi_gray)

        if confidence<40:
            profile = getProfile(id)
            if(profile != None):
                list_attendance[profile] = 1
                cv2.putText(frame,str(profile[1]), (x+10, y+h+30), fontface, 1, (0,255,0), 2)
        else:
            cv2.putText(frame, "unknow", (x+10, y+h+30), fontface, 1, (0,255,0), 2)

    print('='*25)
    for k,v in list_attendance.items():
        print(k[1],":",('roll-called' if v else 'missing'))

    cv2.imshow('image',frame)
    if(cv2.waitKey(1) == ord('q')):
        break

cap.release()
cv2.destroyAllWindows()