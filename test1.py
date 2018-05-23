import sapphire.utility

from sapphire.scrapers import reuters
from sapphire.utility.logging import registerLogger, ConsoleLogger

print("--------------------------------------------------")
sapphire.utility.readConfig("config.json")


cl = ConsoleLogger({"[ALL]":{}, "DEBUG":{"color":"yellow", "prepend":"DEBUG :: "}})
registerLogger(cl)


scraper = reuters.RSSScraper()
scraper.run()
print("==================================================")
