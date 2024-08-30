import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
cred = credentials.Certificate("secretServiceCode.json")
firebase_admin.initialize_app(cred,{
    'databaseURL':'https://faceattendence-183ae-default-rtdb.firebaseio.com/'
})

ref=db.reference('Students')
data = {
    "21341a4521":
        {
            "name" : "GURAVANA ASHOK KUMAR",
            "section":"A",
            "Branch":"AI&DS",
            "Batch" : "2021-25",
            "total_attendence": 5,
            "year":4,
            "last_attendence_time":"2024-08-29 00:54:34"
        },
    "321654":
        {
            "name" : "Murtuja Hasan",
            "section":"C",
            "Branch":"robotics",
            "Batch" : "2022-26",
            "total_attendence": 6,
            "year":3,
            "last_attendence_time":"2024-08-23 00:54:34"
        },
    "852741":
        {
            "name" : "Monalisa",
            "section":"A",
            "Branch":"AI&ML",
            "Batch" : "2021-25",
            "total_attendence": 9,
            "year":4,
            "last_attendence_time":"2024-08-20 00:54:34"
        },
    "963852":
        {
            "name" : "elon musk",
            "section":"B",
            "Branch":"ECE",
            "Batch" : "2020-24",
            "total_attendence": 5,
            "year":3,
            "last_attendence_time":"2024-08-21 00:54:34"
        }
}

for key,value in data.items():
    ref.child(key).set(value)