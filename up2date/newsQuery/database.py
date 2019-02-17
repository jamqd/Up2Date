import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

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

def setQuery(uid, queryID, queryText):
    queryTextRef = db.reference('users/' + str(uid) + "/" + str(queryID) + "/" + "queryText")
    queryTextRef.set(queryText)

def setFrequency(uid, queryID, frequency):
    frequencyRef = db.reference('users/' + str(uid) + "/" + str(queryID) + "/" + "frequency")
    frequencyRef.set(frequency)

def setRelevanceThreshold(uid, queryID, relevanceThreshold):
    relevanceThresholdRef = db.reference('users/' + str(uid) + "/" + str(queryID) + "/" + "relevanceThreshold")
    relevanceThresholdRef.set(relevanceThreshold)

def getEmail(uid):
    emailRef = db.reference('users/' + str(uid) + '/' + 'email')
    return emailRef.get()

def setEmail(uid, email):
    emailRef = db.reference('users/' + str(uid) + "/" + "email")
    emailRef.set(email)

def setName(uid, name):
    nameRef = db.reference('users/' + str(uid) + "/" + "name")
    nameRef.set(name)

def getUID(email):
    usersRef = db.reference("users/")
    uidDict = usersRef.order_by_child('email').equal_to(email)
    print(list(uidDict.get().items())[0][0])
    return list(uidDict.get().items())[0][0]

def getQueryID(uid, queryText):
    userRef = db.reference("users/" + str(uid))
    qidDict = userRef.order_by_child('queryText').equal_to(queryText)
    print(list(qidDict.get())[0])
    return list(qidDict.get())[0]

def getFrequency(uid, queryID):
    queryRef = db.reference("users/" + str(uid )+ "/" + str(queryID))
    print(queryRef.get()["frequency"])
    return queryRef.get()["frequency"]
    
def getRelevanceThreshold(uid, queryID):
    queryRef = db.reference("users/" + str(uid )+ "/" + str(queryID))
    print(queryRef.get()["relevanceThreshold"])
    return queryRef.get()["relevanceThreshold"]

def getQueryText(uid, queryID):
    queryRef = db.reference("users/" + str(uid )+ "/" + str(queryID))
    print(queryRef.get()["queryText"])
    return queryRef.get()["queryText"]

def getQueryIDs(uid):
    userRef = db.reference("users/" + str(uid))
    qidDict = userRef.order_by_child('queryText')
    return list(qidDict.get())[2:]

def getQueries(uid):
    queryIDs = getQueryIDs(uid)
    queries = []
    for i in queryIDs:
        queries.append(getQueryText(uid, i))
    print(queries)
    return queries

def deleteQuery(uid, queryText):
    qid = getQueryID(uid, queryText)
    queryRef = db.reference("users/" + str(uid )+ "/" + str(qid))
    queryRef.delete()








# test_uid = addUser("niceu", "ceasar@gmail.com")
# queryID = addQuery(test_uid, "trump is dumb")
# setQuery(test_uid, queryID, "this should be here")
# setFrequency(test_uid,queryID,30)
# setRelevanceThreshold(test_uid, queryID, 69)
# setEmail(test_uid, "bobbyjindal@gmail.com")
# setName(test_uid, "donald")
# recoverd = getUID("bobbyjindal@gmail.com")
# testing = getQueryID(recoverd, "this should be here")
# getFrequency(test_uid, testing)
# getRelevanceThreshold(test_uid, testing)
# getQueryText(test_uid, testing)
# addQuery(recoverd, "fuck GCP")
# getQueryIDs(recoverd)
# getQueries(recoverd)


