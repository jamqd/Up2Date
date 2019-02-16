import requests

def query (search_term, from_date, to_date):
    a = "https://newsapi.org/v2/everything?q={0}&from={1}&to={2}&sortBy=popularity&apiKey=3c906a21fbeb43c7819511120fd8a1c2".format(search_term, from_date, to_date)
    response = requests.get(a).json()
    print(response)

query("bitcoin", "2019-01-26", "2019-02-15") #date format yyyy-mm-dd one month back at most
