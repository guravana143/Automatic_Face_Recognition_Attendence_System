import cv2
import face_recognition
import pickle
import os
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import storage
cred = credentials.Certificate("secretServiceCode.json")
firebase_admin.initialize_app(cred,{
    'databaseURL':'https://faceattendence-183ae-default-rtdb.firebaseio.com/',
    'storageBucket':"faceattendence-183ae.appspot.com"
})

folderPath='images'
pathList=os.listdir(folderPath)
imgList=[]
studentIds=[]

for path in pathList:
    imgList.append(cv2.imread(os.path.join(folderPath,path)))
    studentIds.append(os.path.splitext(path)[0])

    filename=f'{folderPath}/{path}'
    bucket = storage.bucket()
    blob = bucket.blob(filename)
    blob.upload_from_filename(filename)


def findEncodiongs(imageList):
    encodeList=[]
    for img in imageList:
        img=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        encode= face_recognition.face_encodings(img)[0]
        encodeList.append(encode)

    return encodeList

encodelistKnown=findEncodiongs(imgList)
encodeListknownwithIds=[encodelistKnown,studentIds]
file = open("EncodeFile.p",'wb')
pickle.dump(encodeListknownwithIds,file)
file.close()

