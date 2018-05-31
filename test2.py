import sapphire.utility

from sapphire.managers.metadata import MetadataManager
from sapphire.utility.logging import registerLogger, ConsoleLogger

print("--------------------------------------------------")
print("\tTEST 2 - metadata storing")
print("--------------------------------------------------")
sapphire.utility.readConfig("config.json")


cl = ConsoleLogger({"[ALL]":{"color":"white"}, "DEBUG":{"color":"yellow"}, "WARNING":{"color":"brightyellow"}, "ERROR":{"color":"red"}}, {"RSS Manager":{"color":"brightcyan"}, "Metadata Manager":{"color":"green"}}, True, True)
registerLogger(cl)

meta_man = MetadataManager()
meta_man.consumeQueue()


print("==================================================")
