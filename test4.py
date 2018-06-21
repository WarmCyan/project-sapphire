#import sapphire.utility

#from sapphire.utility.logging import registerLogger, ConsoleLogger
from sapphire.managers import article

print("--------------------------------------------------")
print("\tTEST 4 - article manager")
print("--------------------------------------------------")

am = article.ArticleManager("config.json")
am.scrapeFeeds()
am.consumeQueue()
am.scrapeNextArticle()

print("==================================================")
