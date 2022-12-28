import os
import pickle
import cv2
import numpy as np
import cvzone
import face_recognition

import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import storage
from datetime import datetime

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred,{
    'databaseURL':"https://dutabangsaattendance-default-rtdb.asia-southeast1.firebasedatabase.app/",
    'storageBucket' : "dutabangsaattendance.appspot.com"
})

bucket = storage.bucket()

# videoCapture pada (1) karena  menggunakan device kamera dari luar pc (droidcam dari handphone)
cap = cv2.VideoCapture(1)
cap.set(3, 1280)
cap.set(4, 720)

imgBackground = cv2.imread('Resources/background.png')

# mengimport gambar dari modes kedalam list
folderModePath = 'Resources/Modes'
modePathList = os.listdir(folderModePath)
imgModeList = []
for path in modePathList:
    imgModeList.append(cv2.imread(os.path.join(folderModePath,path)))
# print(len(imgModeList))

# Load file encoding
print("Loading Encode File...")
file = open("EncodeFile.p", "rb")
encodeListKnownWithIds = pickle.load(file)
file.close()
encodeListKnown, mahasiswaIds = encodeListKnownWithIds
print("Encode File Loaded...")

# setting tipe interface mode
modeType = 0
counter = 0
id = -1
imgMahasiswa = []

while True:
    success, ori_img = cap.read()
    width = 640
    height = 480
    dim = (width, height)
    img = cv2.resize(ori_img,dim)

    imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

    faceCurFrame = face_recognition.face_locations(imgS)
    encodeCurFrame = face_recognition.face_encodings(imgS, faceCurFrame)

    imgBackground[162:162+480, 55:55+640] = img
    imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[modeType]

    if faceCurFrame:
        for encodeFace, faceLoc in zip(encodeCurFrame, faceCurFrame):
            matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
            faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)
            # print("matches", matches)
            # print("jarak", faceDis)

            matchIndex = np.argmin(faceDis)
            # print("Match index", matchIndex)

            if matches[matchIndex]:
                # print("wajah yang dikenal terdeteksi")
                # print (mahasiswaIds[matchIndex])
                y1, x2, y2, x1 = faceLoc
                # dikalikan 4 karena imgS meresize img 1/4
                y1, x2, y2, x1 =  y1*4, x2*4, y2*4, x1*4
                bbox = 55+x1, 162+y1, x2-x1, y2 - y1
                imgBackground = cvzone.cornerRect(imgBackground, bbox, rt=0)

                #cek counter
                id = mahasiswaIds[matchIndex]
                if counter == 0:
                    cvzone.putTextRect(imgBackground, "Loading", (275, 400))
                    cv2.imshow('tampilan face attendance', imgBackground)
                    cv2.waitKey(1)
                    counter = 1
                    modeType = 1

        if counter != 0:

            if counter ==1:
                #Get Data
                mahasiswaInfo = db.reference(f'Mahasiswa/{id}').get()
                print(mahasiswaInfo)
                #Get image dari storage
                blob = bucket.get_blob(f'Images/{id}.png')
                array = np.frombuffer(blob.download_as_string(), np.uint8)
                imgMahasiswa = cv2.imdecode(array, cv2.COLOR_BGRA2BGR)
                # Update data of attendance
                datetimeObject = datetime.strptime(mahasiswaInfo['last_attendance_time'],
                                                   "%Y-%m-%d %H:%M:%S")
                secondsElapsed = (datetime.now() - datetimeObject).total_seconds()
                print(secondsElapsed)
                # batasi untuk 30 detik
                if secondsElapsed >30:
                    ref = db.reference(f'Mahasiswa/{id}')
                    mahasiswaInfo['total_attendance'] += 1
                    ref.child('total_attendance').set(mahasiswaInfo['total_attendance'])
                    ref.child('last_attendance_time').set(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                else:
                    modeType = 3
                    counter = 0
                    imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[modeType]

            if modeType != 3:

                if 10 < counter < 20:
                    modeType = 2

                imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[modeType]

                if counter <=10:
                    cv2.putText(imgBackground, str(mahasiswaInfo['total_attendance']), (861, 125),
                                cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 1)
                    cv2.putText(imgBackground, str(mahasiswaInfo['jurusan']), (1006, 550),
                                cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 255, 255), 1)
                    cv2.putText(imgBackground, str(id), (1006, 493),
                                cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 255, 255), 1)
                    cv2.putText(imgBackground, str(mahasiswaInfo['status']), (910, 625),
                                cv2.FONT_HERSHEY_COMPLEX, 0.6, (100, 100, 100), 1)
                    cv2.putText(imgBackground, str(mahasiswaInfo['tahun']), (1025, 625),
                                cv2.FONT_HERSHEY_COMPLEX, 0.6, (100, 100, 100), 1)
                    cv2.putText(imgBackground, str(mahasiswaInfo['angkatan']), (1125, 625),
                                cv2.FONT_HERSHEY_COMPLEX, 0.6, (100, 100, 100), 1)

                    (w, h), _ = cv2.getTextSize(mahasiswaInfo['nama'], cv2.FONT_HERSHEY_COMPLEX, 1, 1)
                    offset = (414 - w) // 2
                    cv2.putText(imgBackground, str(mahasiswaInfo['nama']), (808 + offset, 445),
                                cv2.FONT_HERSHEY_COMPLEX, 1, (50, 50, 50), 1)

                    imgBackground[175:175+216, 909:909+216] = imgMahasiswa

                counter +=1

                if counter >= 20:
                    counter = 0
                    modeType = 0
                    mahasiswaInfo = []
                    imgMahasiswa = []
                    imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[modeType]

    else:
        modeType = 0
        counter = 0

    # cv2.imshow('webcam', img)
    cv2.imshow('tampilan face attendance', imgBackground)
    cv2.waitKey(1)