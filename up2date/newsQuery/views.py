from django.shortcuts import render
import requests
dict = {} #save this somewhere later to persist through calls

def query(search_term, from_date=1262304000, article_count=10, subscription_key="db529dd884ae4732a2bf1a453aa66bb1"): #use epoch time
    search_url = "https://api.cognitive.microsoft.com/bing/v7.0/news/search"
    headers = {"Ocp-Apim-Subscription-Key" : subscription_key}
    params  = {"count": article_count, "q": search_term, "since": from_date, "sortBy": "Date", "textDecorations": True, "textFormat": "HTML"}
    response = requests.get(search_url, headers=headers, params=params)
    response.raise_for_status()
    search_results = response.json()
    info = [(article["name"], article["provider"][0]["name"], article["url"], article["datePublished"]) for article in search_results["value"]]
    for i in info:
        if i[1] in dict.keys():
            dict[i[1]] += 1
        else :
            dict[i[1]] = 1

    print(info)
    return info #returns (name, source name, url, datepublished)
    
# Create your views here.
def search(request):
    searchterm = ""
    if request.method == "POST":
        print("POST recieved")
        searchterm = request.body.decode('utf-8')
    info = query(searchterm)
    return info