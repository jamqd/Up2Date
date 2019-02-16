# import requests
# import json

# def getDatabase():

#     response = requests.get("https://up2date-d815e.firebaseio.com/.json")
#     print(response.json())

# def writeToDataBase(json):
#     response = requests.put("https://up2date-d815e.firebaseio.com/hello.json", data='{"testing" : "{ "test":"bob"}"}')
#     print(str(response))

# def addUser(name):
#     json = {
#         "name": name
#     }
#     response = requests.post("https://up2date-d815e.firebaseio.com/users.json",data=str(json))
#     print(response)
#     print("added user " + str(name))


# def addQuery(UID, query, frequency=7):

#     print("added query: " + str(query) + "to " + str(UID))

# testJson = {
#   "Users" : {
#     "UID" : {
#       "query1" : {
#         "frequency" : 7,
#         "queryText" : "query text here",
#         "relevanceThreshold" : 50
#       },
#       "query2" : {
#         "frequency" : 30,
#         "queryText" : "query text 2 here",
#         "relevanceThreshold" : 60
#       }
#     },
#     "UID2" : {
#       "query1" : {
#         "frequency" : 9,
#         "queryText" : "query text here",
#         "relevanceThreshold" : 80
#       }
#     }
#   }
# }

# # writeToDataBase(testJson)
# addUser("bob")
# getDatabase()


import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

cred = credentials.Certificate('up2date-d815e-firebase-adminsdk-bvvmg-40710c7694.json')
default_app = firebase_admin.initialize_app(cred, options={
    'databaseURL': 'https://up2date-d815e.firebaseio.com/'
})


def addUser(name, email):
    usersRef = db.reference('users')

    userInfo = {
        "name" : name,
        "email" : email
    }

    uid = usersRef.push(userInfo)
    uid = uid.key
    print(uid)
    return uid


test_uid = addUser("niceu", "ceasar@gmail.com")

def addQuery(uid, queryText):
    userRef = db.reference('users/' + str(uid))
    queryInfo = {
        "queryText" : queryText,
        "frequency" : 7,
        "relevanceThreshold": 0
    }
    queryID = userRef.push(queryInfo)
    queryID = queryID.key
    return queryID

queryID = addQuery(test_uid, "trump is dumb")

def setQuery(uid, queryID, queryText):
    queryTextRef = db.reference('users/' + str(uid) + "/" + str(queryID) + "/" + "queryText")
    queryTextRef.set(queryText)

setQuery(test_uid, queryID, "this should be here")

def setFrequency(uid, queryID, frequency):
    frequencyRef = db.reference('users/' + str(uid) + "/" + str(queryID) + "/" + "frequency")
    frequencyRef.set(frequency)

setFrequency(test_uid,queryID,30)

def setRelevanceThreshold(uid, queryID, relevanceThreshold):
    relevanceThresholdRef = db.reference('users/' + str(uid) + "/" + str(queryID) + "/" + "relevanceThreshold")
    relevanceThresholdRef.set(relevanceThreshold)

setRelevanceThreshold(test_uid, queryID, 69)

def setEmail(uid, email):
    emailRef = db.reference('users/' + str(uid) + "/" + "email")
    emailRef.set(email)

setEmail(test_uid, "bobbyjindal@gmail.com")

def setName(uid, name):
    nameRef = db.reference('users/' + str(uid) + "/" + "name")
    nameRef.set(name)

setName(test_uid, "donald")





