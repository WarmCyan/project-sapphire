import sapphire.utility

from sapphire.scrapers import reuters

print("hi")
sapphire.utility.readConfig("config.json")
print(sapphire.utility.feed_scrape_raw_tmp_dir)


scraper = reuters.RSSScraper()
scraper.scrape()
print("Done")
