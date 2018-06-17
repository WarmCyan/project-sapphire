import sapphire.utility

#from sapphire.managers.metadata import MetadataManager
#from sapphire.scrapers import reuters_v1
from sapphire.utility.logging import registerLogger, ConsoleLogger
from sapphire.managers import database, content

print("--------------------------------------------------")
print("\tTEST 3 - content scraping")
print("--------------------------------------------------")
sapphire.utility.readConfig("config.json")


cl = ConsoleLogger({"[ALL]":{"color":"white"}, "DEBUG":{"color":"yellow"}, "WARNING":{"color":"brightyellow"}, "ERROR":{"color":"red"}}, {"RSS Manager":{"color":"brightcyan"}, "Metadata Manager":{"color":"green"}, "Content Manager":{"color":"blue"}}, True, True)
registerLogger(cl)

#url = "https://www.reuters.com/article/us-australia-security-elections/australia-forms-task-force-to-guard-elections-from-cyber-attacks-idUSKCN1J506D?feedType=RSS&feedName=technologyNews&utm_source=feedburner&utm_medium=feed&utm_campaign=Feed%3A+reuters%2FtechnologyNews+%28Reuters+Technology+News%29"

#scraper = reuters_v1.ContentScraper()
#scraper.run(url, "DISISTEST")


cm = content.ContentManager()
db = database.DatabaseManager()

article = db.getFirstLackingArticle()
cm.scrape(article)



print("==================================================")
