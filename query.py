import requests
import datetime
import time

def queryNewsApi (search_term, from_date, to_date): #date format yyyy-mm-dd one month back at most
    a = "https://newsapi.org/v2/everything?q={0}&from={1}&to={2}&sortBy=popularity&apiKey=3c906a21fbeb43c7819511120fd8a1c2".format(search_term, from_date, to_date)
    response = requests.get(a).json()
    return response

# merge with views.py later
#return (avg num articles of past four weeks, num of articles this week)
def getRatio (search_term):
    sum = getControl(search_term, 5)
    first = getControl(search_term, 0)
    avg = (sum-first)/4
    return (avg, first)

def getControl(search_term, weeksback):
    back = time.mktime(datetime.datetime.now().timetuple()) - weeksback*604800
    offset = 0
    res = query(search_term, offset)
    oldestdate = getTime(res[99][3])
    print(back)
    print(res[99][3])
    while(back < oldestdate):
        offset += 100
        res = query(search_term, offset)
        oldestdate = getTime(res[99][3])
    index = 0
    for i in range(100):
        if (getTime(res[i][3]) <= oldestdate):
            index = i
    return offset + i

def getTime(date):
    str = date[8:10] + date[5:7] + date[:4]
    dt = datetime.datetime.strptime(str, "%d%m%Y").date()
    unix = time.mktime(dt.timetuple())
    return unix


def query(search_term, offset, from_date = 1262304000, article_count=100, subscription_key="db529dd884ae4732a2bf1a453aa66bb1"): #use epoch time
    search_url = "https://api.cognitive.microsoft.com/bing/v7.0/news/search"
    headers = {"Ocp-Apim-Subscription-Key" : subscription_key}
    #dict_rank = {} #save this somewhere later to persist through calls

    #for k in range(0, count/article_count):
    params  = {"count": article_count, "q": search_term, "since": from_date, "sortBy": "Date", "textDecorations": True, "textFormat": "HTML", "offset": offset}
    response = requests.get(search_url, headers=headers, params=params)
    response.raise_for_status()
    search_results = response.json()

    info = [(article["name"], article["provider"][0]["name"], article["url"], article["datePublished"]) for article in search_results["value"]]
    time.sleep(0.5)
    return info
#print(query("trump", 0, time.mktime(datetime.datetime.now().timetuple()) - 604800))
print(getRatio("trump"))
