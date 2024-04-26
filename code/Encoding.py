import cv2
import face_recognition
import pickle
import os
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import storage


cred = credentials.Certificate("C:/Users/Dell/PycharmProjects/Facerecogination/code/serviceAccountKey.json")
firebase_admin.initialize_app(cred, {
    "databaseURL": "https://face-attendance-a3bd4-default-rtdb.firebaseio.com/",
    "storageBucket": "face-attendance-a3bd4.appspot.com"
})

# Import the student images into the list:
folderPath = 'C:/Users/Dell/PycharmProjects/Facerecogination/Images'
PathList = os.listdir(folderPath)
print(PathList)
imgList = []
studentIds=[]

for path in PathList:
    imgList.append(cv2.imread(os.path.join(folderPath, path)))
    studentIds.append(os.path.splitext(path)[0])

    fileName = f'{folderPath}/{path}'
    bucket = storage.bucket()
    blob = bucket.blob(fileName)
    blob.upload_from_filename(fileName)


print(studentIds)
print(len(imgList))



def findEncodings(imageList):
    encodeList=[]
    for img in imageList:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)

    return encodeList


encodeListKnown = findEncodings(imgList)
encodeListKnownwithIds = [encodeListKnown, studentIds]
# print(encodeListKnownwithIds)
# print(encodeListKnown)


file = open("ExtractEncodings.p", 'wb')
pickle.dump(encodeListKnownwithIds, file)
file.close()
