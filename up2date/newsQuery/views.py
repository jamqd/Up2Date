from django.shortcuts import render
import requests
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
import time
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import auth
import database

cred = credentials.Certificate('up2date-d815e-firebase-adminsdk-bvvmg-40710c7694.json')
default_app = firebase_admin.initialize_app(cred, options={
    'databaseURL': 'https://up2date-d815e.firebaseio.com/'
})

def addAuthUser(name, email):
    uid = database.addUser(name, email)
    auth.create_user(uid=uid,display_name=name,email=email)

def getUserId(email):
    userRecord = auth.get_user_by_email(email)
    return userRecord.uid

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

def query(search_term, from_date = 1262304000, article_count=100, subscription_key="db529dd884ae4732a2bf1a453aa66bb1"): #use epoch time
    search_url = "https://api.cognitive.microsoft.com/bing/v7.0/news/search"
    headers = {"Ocp-Apim-Subscription-Key" : subscription_key}
    dict_rank = {} #save this somewhere later to persist through calls

    for k in range(0, 10):
        params  = {"count": article_count, "q": search_term, "since": from_date, "sortBy": "Date", "textDecorations": True, "textFormat": "HTML", "offset": (k*100)}
        response = requests.get(search_url, headers=headers, params=params)
        response.raise_for_status()
        search_results = response.json()
    
        info = [(article["name"], article["provider"][0]["name"], article["url"], article["datePublished"]) for article in search_results["value"]]
        for i in info:
            if i[1] in dict_rank.keys():
                dict_rank[i[1]] += 1
            else :
                dict_rank[i[1]] = 1
        print("info below:")
        print(info)
        time.sleep(0.5)
    return dict_rank #returns (name, source name, url, datepublished)

# Create your views here.
@csrf_exempt
def search(request):
    userEmail = ""
    searchterm = "not found"
    if request.method == "POST":
        print("POST received")
        data = request.json()
        searchterm = data['query']
        userEmail = data['email']
        #searchterm = request.body.decode('utf-8')
        info = query(searchterm)
        addQuery(getUID(userEmail), searchterm)
        max = 1
        total = 1
        for j, k in info.items():
            total += int(k)
            if int(k) > max:
                max = int(k)
            print(str(j) + ': ' + str(k))
        freq_thres = (max / total) * 0.8
        setFrequency(getUID(userEmail), getQueryID(getUID(userEmail), searchterm), total)
        setRelevanceThreshold(getUID(userEmail), getQueryID(getUID(userEmail), searchterm), freq_thres)
    return HttpResponse(getQueries(getUID(userEmail)))

@csrf_exempt
def pref_update(request):
    return render(request, 'preferences.html')

@csrf_exempt
def updated(request):
    return render(request, 'updated.html')

@csrf_exempt 
def authenticate(request):
    if request.method == "POST":
        print("auth POST received")
        data = request.json()
        addAuthUser(data['name'], data['email'])
        return True
    return False