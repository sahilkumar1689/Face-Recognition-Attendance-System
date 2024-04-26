# Import the open cv library
import os
import pickle
import cv2
import face_recognition
import numpy as np
import dlib
import cvzone
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import storage
from datetime import datetime
import time

cred = credentials.Certificate("C:/Users/Dell/PycharmProjects/Facerecogination/code/serviceAccountKey.json")
firebase_admin.initialize_app(cred, {
    "databaseURL": "https://face-attendance-a3bd4-default-rtdb.firebaseio.com/",
    "storageBucket": "face-attendance-a3bd4.appspot.com"
})
bucket = storage.bucket()



#  Use to capture the webcam using VideoCapture() function if you want to use your built in camera them gave "0" as a parameter else give "1 or 2."
cap = cv2.VideoCapture(0)


# Set the dimensions of the webcam
cap.set(3, 640)
cap.set(4, 480)

imgBackground = cv2.imread("C:/Users/Dell/PycharmProjects/Facerecogination/Resources/background.png")



# Import the modes images into the list:
folderModePath = 'C:/Users/Dell/PycharmProjects/Facerecogination/Resources/Modes'
modePathList = os.listdir(folderModePath)
imgModeList = []
for path in modePathList:
    imgModeList.append(cv2.imread(os.path.join(folderModePath, path)))
# print(len(imgModeList))



# Load the encoding files:
file = open('Facerecogination\code\ExtractEncodings.p', 'rb')
encodeListKnownwithIds = pickle.load(file)
file.close()
encodeListKnown, studentIds = encodeListKnownwithIds
# print(studentIds)


modeType = 0
counter = 0
ids = -1
imgStudent = []

while True:
    success, img = cap.read()

    imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

    faceCurrFrame = face_recognition.face_locations(imgS)
    encodeCurrFrame = face_recognition.face_encodings(imgS, faceCurrFrame)

    imgBackground[162:162 + 480, 55:55 + 640] = img
    imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[modeType]

    if faceCurrFrame:
        for encodeFace, faceLoc in zip(encodeCurrFrame, faceCurrFrame):
            matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
            faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)
            # print("matches", matches)
            # print("FaceDis", faceDis)

            matchIndex = np.argmin(faceDis)
            # print("Match Index:", matchIndex)

            if matches[matchIndex]:
                # print("KnownFace Detected")
                # print(studentIds[matchIndex])
                y1, x2, y2, x1 = faceLoc
                y1, x2, y2, x1 = y1*4, x2*4, y2*4, x1*4
                bbox = 55 + x1, 162 + y1, x2 - x1, y2-y1
                imgBackground = cvzone.cornerRect(imgBackground, bbox, rt=0)

                ids = studentIds[matchIndex]

                if counter == 0:
                    cvzone.putTextRect(imgBackground, "Loading...", (275, 200))
                    cv2.imshow("Face Attendance", imgBackground)
                    cv2.waitKey(1)
                    counter = 1
                    modeType = 1

                if counter != 0:
                    if counter == 1:
                        # Get the Student Data:q
                        studentInfo = db.reference(f'Students/{ids}').get()
                        print(studentInfo)

                        # Get the Student Image:
                        folderPath = 'C:/Users/Dell/PycharmProjects/Facerecogination/Images'
                        blob = bucket.get_blob(f'{folderPath}/{ids}.png')
                        array = np.frombuffer(blob.download_as_string(), np.uint8)
                        imgStudent = cv2.imdecode(array, cv2.COLOR_BGR2RGB)

                        # Update Attendance:
                        dateTimeObject = datetime.strptime(studentInfo['last_attendance_time'],
                                                     "%Y-%m-%d %H:%M:%S")
                        secondsElapsed = (datetime.now() - dateTimeObject).total_seconds()
                        # print(secondsElapsed)

                        if secondsElapsed>60:
                            ref = db.reference(f'Students/{ids}')
                            studentInfo['total_attendance'] += 1
                            ref.child('total_attendance').set(studentInfo['total_attendance'])
                            ref.child('last_attendance_time').set(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                        else:
                            modeType = 3
                            counter = 0
                            imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[modeType]

                    if modeType != 3:

                        if 10<counter<20:
                            modeType = 2

                        imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[modeType]

                        if counter <= 10:
                            cv2.putText(imgBackground, str(studentInfo['total_attendance']), (861, 125),
                                        cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 1)
                            cv2.putText(imgBackground, str(studentInfo['major']), (1010, 550),
                                        cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 255, 255), 1)
                            cv2.putText(imgBackground, str(ids), (1006, 493),
                                        cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 255, 255), 1)
                            cv2.putText(imgBackground, str(studentInfo['standing']), (910, 625),
                                        cv2.FONT_HERSHEY_COMPLEX, 0.6, (100, 100, 100), 1)
                            cv2.putText(imgBackground, str(studentInfo['year']), (1025, 625),
                                        cv2.FONT_HERSHEY_COMPLEX, 0.6, (100, 100, 100), 1)
                            cv2.putText(imgBackground, str(studentInfo['starting_year']), (1125, 625),
                                        cv2.FONT_HERSHEY_COMPLEX, 0.6, (100, 100, 100), 1)

                            (w, h), _ = cv2.getTextSize(studentInfo['Name'], cv2.FONT_HERSHEY_COMPLEX, 1, 1)
                            offset = (414 - w)//2
                            cv2.putText(imgBackground, str(studentInfo['Name']), (800+offset, 445),
                                        cv2.FONT_HERSHEY_COMPLEX, 1, (50, 50, 50), 1)

                            imgBackground[175:175 + 216, 909:909 + 216] = imgStudent

                            time.sleep(1)

                        counter += 1

                        if counter>=20:
                            counter = 0
                            modeType = 0
                            studentInfo = []
                            imgStudent = []
                            imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[modeType]

    else:
        modeType = 0
        counter = 0


    # cv2.imshow("Webcam", img)

    cv2.imshow("Face Attendance", imgBackground)
    cv2.waitKey(1)
