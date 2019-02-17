from django.shortcuts import render
import requests
import datetime
import time
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
import time
import sys
import os
import json
from . import database
from . import authUser
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import auth

cred = credentials.Certificate('newsQuery/up2date-d815e-firebase-adminsdk-bvvmg-40710c7694.json')
default_app = firebase_admin.initialize_app(cred, options={
    'databaseURL': 'https://up2date-d815e.firebaseio.com/'
})

def query(search_term, from_date = 1262304000, article_count=100, count=100000, subscription_key="db529dd884ae4732a2bf1a453aa66bb1"): #use epoch time
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
        #print("info below:")
        #print(info)
        time.sleep(0.5)
    
    newsList = []
    newNews = queryNewsApi(search_term, '2019-02-10', '2019-02-17')
    for url in newNews:
        for article in search_results["value"]:
            #if dict_rank[article['provider'][0]['name']] > 10:
            print(article['url'])
            print(url)
                #print(dict_rank[article['provider'][0]['name']])
            if article['url'] == url:# and dict_rank[article['provider'][0]['name']] > 10:
                newsList.append(article['url'])
    print('news list below')
    print(newsList)
    return dict_rank
    #return dict_rank #returns (name, source name, url, datepublished)

def queryNewsApi (search_term, from_date, to_date): #date format yyyy-mm-dd one month back at most
    a = "https://newsapi.org/v2/everything?q={0}&from={1}&to={2}&sortBy=popularity&apiKey=3c906a21fbeb43c7819511120fd8a1c2".format(search_term, from_date, to_date)
    response = requests.get(a).json()
    
    info = [(article["url"]) for article in response["articles"]]
    print('newsapi info below')
    print(info)
    return info

@csrf_exempt
def search(request):
    searchterm = "not found"
    if request.method == "POST":
        print("POST received")
        data = json.loads(request.body)
        searchterm = data['query']
        uid = data['uid']
        info = query(searchterm)
        database.addQuery(uid, searchterm)
        max = 1
        total = 1
        for j, k in info.items():
            total += int(k)
            if int(k) > max:
                max = int(k)
            #print(str(j) + ': ' + str(k))
        freq_thres = (max / total) * 0.8
        database.setFrequency(uid, database.getQueryID(uid, searchterm), total)
        database.setRelevanceThreshold(uid, database.getQueryID(uid, searchterm), freq_thres)
    return HttpResponse(database.getQueries(uid))

@csrf_exempt
def pref_update(request):
    return render(request, 'preferences.html')

@csrf_exempt
def updated(request):
    return render(request, 'updated.html')

@csrf_exempt
def authenticate(request):
    print(request)
    print(json.loads(request.body))
    print(type(json.loads(request.body)))
    if request.method == "POST":
        print("auth POST received")
        data = json.loads(request.body)
        print(data)
        authUser.addAuthUser(data['name'], data['email'], data['password'])
        return HttpResponse('Account made!')
    return HttpResponse('false')


@csrf_exempt
def login(request):
    if request.method == "POST":
        data = json.loads(request.body)
        uid = authUser.signIn(data['email'], data['password'])
        return HttpResponse(uid)
    return HttpResponse('false')

@csrf_exempt
def getQ(request):
    if request.method == "POST":
        data = json.loads(request.body)
        uid = data['uid']
        value = str(database.getQueries(uid))
        return HttpResponse(value)
    return HttpResponse('false')

@csrf_exempt
def getQID(request):
    if request.method == "POST":
        data = json.loads(request.body)
        uid = data['uid']
        queryText = data['queryText']
        value = str(database.getQueryID(uid, queryText))
        return HttpResponse(value)
    return HttpResponse('false')

@csrf_exempt
def getF(request):
    if request.method == "POST":
        data = json.loads(request.body)
        uid = data['uid']
        text = data['query']
        freq = int(database.getFrequency(uid, database.getQueryID(uid, text)))
        return HttpResponse(freq)
    return HttpResponse('false')

@csrf_exempt
def setF(request):
    if request.method == "POST":
        data = json.loads(request.body)
        uid = data['uid']
        text = data['query']
        freq = data['frequency']
        database.setFrequency(uid, database.getQueryID(uid, text), freq)
        return HttpResponse('frequency set!')
    return HttpResponse('false')