import sapphire.utility

#from sapphire.scrapers import reuters_v1 as reuters
from sapphire.managers.rss import RSSManager
from sapphire.utility.logging import registerLogger, ConsoleLogger

print("--------------------------------------------------")
sapphire.utility.readConfig("config.json")


cl = ConsoleLogger({"[ALL]":{"color":"white"}, "DEBUG":{"color":"yellow"}}, {}, True, True)
registerLogger(cl)


#scraper = reuters.RSSScraper()
#scraper.run("worldnews")
print("==================================================")
