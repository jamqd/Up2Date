import firebase_admin
from firebase_admin import auth
from . import database

def addAuthUser(name, email, password):
    uid = database.addUser(name, email)
    auth.create_user(uid=uid,display_name=name,email=email, password=password)

def getUserId(email):
    userRecord = auth.get_user_by_email(email)
    print(userRecord.user_metadata)
    return userRecord.uid