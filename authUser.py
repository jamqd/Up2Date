import firebase_admin
from firebase_admin import auth
import database

def addAuthUser(name, email):
    uid = database.addUser(name, email, password)
    auth.create_user(uid=uid,display_name=name,email=email, password=password)

def getUserId(email):
    userRecord = auth.get_user_by_email(email)
    return userRecord.uid

