import firebase_admin
from firebase_admin import auth
import database

def addAuthUser(name, email):
    uid = database.addUser(name, email)
    auth.create_user(uid=uid,display_name=name,email=email)

def getUserId(email):
    userRecord = auth.get_user_by_email(email)
    return userRecord.uid

print(getUserId("john.amq.dang@gmail.com"))