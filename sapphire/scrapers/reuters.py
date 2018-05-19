from bs4 import BeautifulSoup
import urllib.request

import datetime

import sapphire.utility


class RSSScraper:

    def __init__(self):
        pass

    # TODO: returns JSON
    # NOTE: make this "run" instead, and have scrape versus extract/parse separate functions?
    def scrape(self):

        #print(sapphire.utility.feed_scrape_raw_tmp_dir) # TODO: debug

        url = "http://feeds.reuters.com/Reuters/worldNews" # TODO: temp

        # scrape the RSS from the url
        request = urllib.request.Request(url)
        response = urllib.request.urlopen(request)
        page = response.read().decode('utf-8')

        scrape_time_dt = datetime.datetime.now()
        scrape_time = sapphire.utility.getTimestamp(scrape_time_dt)

        # store the scrape
        filename = sapphire.utility.getFileTimeStamp(scrape_time_dt) + "_reuters_testscrape.xml" # TODO: or reverse order?
        with open(sapphire.utility.feed_scrape_raw_tmp_dir + "/" + filename, 'w') as f:
            f.write(page)
        
        # parse the scrape
        soup = BeautifulSoup(page, "xml") # NOTE: using lxml-xml (is this available in apt repos for a pi?)

        items = soup.find_all('item')
        
        article_heads = []
        for item in items:
            timestamp = datetime.datetime.strptime(item.pubDate.text, "%a, %d %b %Y %H:%M:%S %z")

            # TODO: make this a class?
            article = { 
                    "title": item.title.text,
                    "description": item.description.text,
                    #"timestamp": timestamp.strftime("%Y-%m-%d %H:%M:%S"),
                    "timestamp": sapphire.utility.getTimestamp(timestamp),
                    "link": item.origLink.text,


                    "source": "reuters",
                    "source_type": "rss",
                    "source_sub": "WorldNews",
                    "source_explicit": url,
                    "scraped": scrape_time,

                    "other": { "category": item.category.text }
                    }

            article_heads.append(article)



