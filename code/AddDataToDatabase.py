import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

cred = credentials.Certificate("C:/Users/Dell/PycharmProjects/serviceAccountKey.json")
firebase_admin.initialize_app(cred, {
    "databaseURL": "https://face-attendance-a3bd4-default-rtdb.firebaseio.com/"
})


ref = db.reference("Students")

data = {
    "321654": {
        "Name": "Murtaza Hassan",
        "major": "Robotics",
        "starting_year": 2017,
        "total_attendance": 0,
        "standing": "G",
        "year": 4,
        "last_attendance_time": "2024-04-05 00:54:34"
    },
    "852741": {
        "Name": "Emily Blunt",
        "major": "Economics",
        "starting_year": 2020,
        "total_attendance": 0,
        "standing": "B",
        "year": 4,
        "last_attendance_time": "2024-04-05 00:54:34"
    },
    "963852": {
        "Name": "Elon Musk",
        "major": "Physics",
        "starting_year": 2020,
        "total_attendance": 0,
        "standing": "G",
        "year": 4,
        "last_attendance_time": "2024-04-05 00:54:34"
    },
    "17302112005": {
        "Name": "Sahil Kumar",
        "major": "ENC",
        "starting_year": 2021,
        "total_attendance": 0,
        "standing": "G",
        "year": 3,
        "last_attendance_time": "2024-04-05 00:54:34"
    },
    "17302112004": {
        "Name": "Priyanshu Dutta",
        "major": "ENC",
        "starting_year": 2021,
        "total_attendance": 0,
        "standing": "G",
        "year": 3,
        "last_attendance_time": "2024-04-05 00:54:34"
    },
    "17302112006": {
        "Name": "Dinker",
        "major": "ENC",
        "starting_year": 2021,
        "total_attendance": 0,
        "standing": "G",
        "year": 3,
        "last_attendance_time": "2024-04-05 00:54:34"
    },
    "17302112007": {
        "Name": "Shivam Thakur",
        "major": "ENC",
        "starting_year": 2021,
        "total_attendance": 0,
        "standing": "G",
        "year": 3,
        "last_attendance_time": "2024-04-05 00:54:34"
    },
    "17302112008": {
        "Name": "Gurwinder Singh",
        "major": "ENC",
        "starting_year": 2021,
        "total_attendance": 0,
        "standing": "G",
        "year": 3,
        "last_attendance_time": "2024-04-05 00:54:34"
    },
    "17302112009": {
        "Name": "Aman Singh",
        "major": "ENC",
        "starting_year": 2021,
        "total_attendance": 0,
        "standing": "G",
        "year": 3,
        "last_attendance_time": "2024-04-05 00:54:34"
    },
    "173021120010": {
        "Name": "Rahul",
        "major": "ENC",
        "starting_year": 2021,
        "total_attendance": 0,
        "standing": "G",
        "year": 3,
        "last_attendance_time": "2024-04-05 00:54:34"
    },
}

for key, value in data.items():
    ref.child(key).set(value)

