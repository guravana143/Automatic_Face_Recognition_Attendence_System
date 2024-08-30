from codecs import EncodedFile

import cv2
import cvzone
from datetime import datetime

import numpy as np
import os
import pickle
import face_recognition
from face_recognition import face_encodings

from Encodegenerator import encodeListknownwithIds, studentIds, encodelistKnown
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import storage

if not firebase_admin._apps:
    cred = credentials.Certificate("secretServiceCode.json")
    firebase_admin.initialize_app(cred,{
        'databaseURL':'https://faceattendence-183ae-default-rtdb.firebaseio.com/',
        'storageBucket':"faceattendence-183ae.appspot.com"
    })
bucket=storage.bucket()

cap = cv2.VideoCapture(0)
cap.set(3,640)
cap.set(4, 480)

#importing the modes

imgBackground=cv2.imread('resources/background.png')
folderModePath="resources/modes"
modePathList=os.listdir(folderModePath)
imgModeList=[]

for path in modePathList:
    imgModeList.append(cv2.imread(os.path.join(folderModePath,path)))

#print(len(imgModeList))

#load the encoded file
file = open("EncodeFile.p",'rb')
encodeListknownwithIds = pickle.load(file)
file.close()
encodeListknown, studentIds = encodeListknownwithIds


modeType=0
counter=0
id=-1
imgStudent=[]

while True:
    success, img = cap.read()

    imgS=cv2.resize(img,(0,0),None, 0.25,0.25)
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

    facecurrentFrame = face_recognition.face_locations(imgS)
    encodeCurrentFrame = face_encodings(imgS,facecurrentFrame)
    imgBackground[162:162+480,55:55+640] = img
    imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[modeType]
    if facecurrentFrame :

        for encoface , faceloc in zip(encodeCurrentFrame,facecurrentFrame):
            matches = face_recognition.compare_faces(encodeListknown,encoface)
            faceDis = face_recognition.face_distance(encodeListknown,encoface)
            matchIndex=np.argmin(faceDis)

            if matches[matchIndex]:
                y1, x2, y2, x1 =faceloc
                y1, x2, y2, x1 = y1*4, x2*4, y2*4, x1*4
                bbox = 55+x1, 162+y1, x2-x1, y2 - y1
                imgBackground= cvzone.cornerRect(imgBackground, bbox, rt=0)
                id=studentIds[matchIndex]

                if counter == 0:
                    cvzone.putTextRect(imgBackground,"Loading...",(275,400))
                    cv2.imshow("Face Attendence",imgBackground)
                    cv2.waitKey(1)
                    counter=1
                    modeType=1
        if counter!=0:
            if counter==1:
                #get the data from database
                studentInfo = db.reference(f'Students/{id}').get()

                #get the image from the database
                blob = bucket.get_blob(f'images/{id}.jpg')
                array=np.frombuffer(blob.download_as_string(),np.uint8)
                imgStudent=cv2.imdecode(array,cv2.COLOR_BGRA2BGR)

                #update data of attendence
                datetimeObject = datetime.strptime(studentInfo['last_attendence_time'], "%Y-%m-%d %H:%M:%S")
                secondsElapsed = (datetime.now()-datetimeObject).total_seconds()
                if secondsElapsed>30:
                    ref=db.reference(f'Students/{id}')
                    studentInfo['total_attendence']+=1
                    ref.child('total_attendence').set(studentInfo['total_attendence'])
                    ref.child('last_attendence_time').set(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

                else:
                    modeType=3
                    counter=0
                    imgBackground[44:44+633,808:808+414] = imgModeList[modeType]
            if modeType!=3:
                if 10<counter<20:
                    modeType = 2
                imgBackground[44:44+633,808:808+414]=imgModeList[modeType]

                if counter<=10:

                    cv2.putText(imgBackground, str(studentInfo['total_attendence']), (861, 125),
                                cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 1)
                    cv2.putText(imgBackground, str(studentInfo['Branch']), (1006, 550),
                                cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 255, 255), 1)
                    cv2.putText(imgBackground, str(id), (1006, 493),
                                cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 255, 255), 1)
                    cv2.putText(imgBackground, str(studentInfo['section']), (910, 625),
                                cv2.FONT_HERSHEY_COMPLEX, 0.6, (100, 100, 100), 1)
                    cv2.putText(imgBackground, str(studentInfo['year']), (1025, 625),
                                cv2.FONT_HERSHEY_COMPLEX, 0.6, (100, 100, 100), 1)
                    cv2.putText(imgBackground, str(studentInfo['Batch']), (1125, 625),
                                cv2.FONT_HERSHEY_COMPLEX, 0.6, (100, 100, 100), 1)

                    (w, h), _ = cv2.getTextSize(studentInfo['name'], cv2.FONT_HERSHEY_COMPLEX, 1, 1)
                    offset = (414 - w) // 2
                    cv2.putText(imgBackground, str(studentInfo['name']), (808 + offset, 445),
                                cv2.FONT_HERSHEY_COMPLEX, 1, (50, 50, 50), 1)

                    imgBackground[175:175 + 216, 909:909 + 216] = imgStudent

                counter +=1

                if counter>=20:
                    counter=0
                    modeType=0
                    studentInfo=[]
                    imgStudent=[]
                    imgBackground[44:44 + 633,808:808 + 414] = imgModeList[modeType]





    #cv2.imshow("webcam", img)
    cv2.imshow("Face Attendence", imgBackground)
    cv2.waitKey(1)
