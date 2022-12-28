
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred,{
    'databaseURL':"https://dutabangsaattendance-default-rtdb.asia-southeast1.firebasedatabase.app/"
})

ref = db.reference('Mahasiswa')

data = {
    "200103140":
        {
            "nama": "Adri Surya Kusuma",
            "jurusan": "TI",
            "angkatan": "2020",
            "total_attendance": 0,
            "status": "mhs",
            "tahun": 2,
            "last_attendance_time": "2022-12-24 18:30:00"
        },
    "200103141":
        {
            "nama": "Joko Widodo",
            "jurusan": "SI",
            "angkatan": "2019",
            "total_attendance": 0,
            "status": "presiden",
            "tahun": 3,
            "last_attendance_time": "2022-12-24 18:30:00"
        },
    "200103142":
        {
            "nama": "Elon Musk",
            "jurusan": "TK",
            "angkatan": "2021",
            "total_attendance": 0,
            "status": "dosen",
            "tahun": 1,
            "last_attendance_time": "2022-12-24 18:30:00"
        },
    "200103143":
        {
            "nama": "Erma Widiya N",
            "jurusan": "MI",
            "angkatan": "2021",
            "total_attendance": 0,
            "status": "mhs",
            "tahun": 1,
            "last_attendance_time": "2022-12-24 18:30:00"
        },
    "200103144":
        {
            "nama": "Mark Zuckerberg",
            "jurusan": "SI",
            "angkatan": "2021",
            "total_attendance": 0,
            "status": "dosen",
            "tahun": 1,
            "last_attendance_time": "2022-12-24 18:30:00"
        },
"200103145":
        {
            "nama": "Anya Geraldine",
            "jurusan": "Mipa",
            "angkatan": "2021",
            "total_attendance": 0,
            "status": "mhs",
            "tahun": 1,
            "last_attendance_time": "2022-12-24 18:30:00"
        },
"200103146":
        {
            "nama": "Joe Widya",
            "jurusan": "Hukum",
            "angkatan": "2021",
            "total_attendance": 0,
            "status": "mentor",
            "tahun": 1,
            "last_attendance_time": "2022-12-24 18:30:00"
        },
"200103147":
        {
            "nama": "Soekma A Sulistyo",
            "jurusan": "Hukum",
            "angkatan": "2021",
            "total_attendance": 0,
            "status": "mentor",
            "tahun": 1,
            "last_attendance_time": "2022-12-24 18:30:00"
        }
}

for key, value in data.items():
    ref.child(key).set(value)
