#import sapphire.utility

#from sapphire.utility.logging import registerLogger, ConsoleLogger
from sapphire.managers import article

print("--------------------------------------------------")
print("\tTEST 4 - article manager (self configuring)")
print("--------------------------------------------------")

am = article.ArticleManager("config.json")

print("==================================================")
