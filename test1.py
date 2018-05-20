import sapphire.utility

from sapphire.scrapers import reuters
from sapphire.utility.logging import registerLogger, ConsoleLogger

print("--------------------------------------------------")
sapphire.utility.readConfig("config.json")


cl = ConsoleLogger({"[ALL]":{}})
registerLogger(cl)


scraper = reuters.RSSScraper()
scraper.run()
print("==================================================")
