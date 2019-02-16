import requests

def query(search_term, from_date=1262304000, article_count=10, subscription_key="db529dd884ae4732a2bf1a453aa66bb1"): #use epoch time
    search_url = "https://api.cognitive.microsoft.com/bing/v7.0/news/search"
    headers = {"Ocp-Apim-Subscription-Key" : subscription_key}
    params  = {"count": article_count, "q": search_term, "since": from_date, "sortBy": "Date", "textDecorations": True, "textFormat": "HTML"}
    response = requests.get(search_url, headers=headers, params=params)
    response.raise_for_status()
    search_results = response.json()
    dates = [(article["name"], article["url"], article["datePublished"]) for article in search_results["value"]]
    for i in dates:
        print(i) #prints (name, url, datepublished), return/print search results to get entire research result in JSON format
