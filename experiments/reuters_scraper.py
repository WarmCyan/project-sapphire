from bs4 import BeautifulSoup
import urllib.request


# scraping part
url = "http://feeds.reuters.com/Reuters/worldNews"

request = urllib.request.Request(url)
response = urllib.request.urlopen(request)

page = response.read().decode('utf-8')

#print(page)


# cleaning/extraction part

soup = BeautifulSoup(page, "xml") # NOTE: this is using lxml-xml
