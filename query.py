import requests

url = "https://api.similarweb.com/v1/website/cnn.com/total-traffic-and-engagement/visits?api_key=863cfc940aa344a6831457b963e794c9&start_date=2016-01&end_date=2016-03&main_domain_only=false&granularity=monthly"


response = requests.get(url)
print(response.text)


# .format(
#     site='cnn.com',
#     api_key=MY_API_KEY,
#     start_date="2017-09",
#     end_date="2017-10",
#     granularity="monthly"
