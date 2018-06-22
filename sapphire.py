#***************************************************************************
#
#  File: sapphire.py
#  Date created: 06/21/2018
#  Date edited: 06/21/2018
#
#  Author: Nathan Martindale
#  Copyright © 2018 Digital Warrior Labs
#
#  Description: Application for running sapphire backend engine
#
#***************************************************************************

import sys
import os
import pycolor

from sapphire.managers import article



VERSION = "0.1.0"
VERSION_DATE = "06/20/2018"
COPYRIGHT = "Copyright © 2018 Digital Warrior Labs"




def show_help():
    print("This is the help menu")
    
def repl():
    print(pycolor.BRIGHTBLUE + "Sapphire> " + pycolor.RESET, end='')
    command = input()
    
    if command == "exit":
        return -1

def repl_loop():
    result = 0
    while result != -1:
        result = repl()




# ----------------------------------------------------------------------
# MAIN PROGRAM FLOW
# ----------------------------------------------------------------------

    
# handle a confused user
if len(sys.argv[1:]) == 0 or sys.argv[1] == 'help' or sys.argv[1] == '-h':
    show_help()
    exit()

# print fanciness informational stuffs
print("\n=====================================================")
print(pycolor.BRIGHTBLUE + "SAPPHIRE ENGINE" + pycolor.RESET)
print("Version: " + pycolor.BRIGHTYELLOW + VERSION + pycolor.RESET)
print("Date: " + pycolor.BRIGHTYELLOW + VERSION_DATE + pycolor.RESET)
print(COPYRIGHT)
print("=====================================================\n")

# handle the first argument (the mode word)
mode = sys.argv[1]
print("Mode: " + str(mode) + "\n")

# get default config
config_filename = os.getenv("CONF_DIR") + "/sapphire_config.json"

# check for local config
files = [f for f in os.listdir('.') if os.path.isfile(f)]
for f in files:
    if f == "sapphire_config.json": config_filename = "./sapphire_config.json"

# handle command line arguments
for arg in sys.argv[2:]:
    if arg.startswith("--config"):
        config_filename = arg[arg.index('=')+1:]

# handle mode
if mode == "repl":
    repl_loop()
