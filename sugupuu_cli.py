# File sugupuu_cli.py - sugupuu cli application
# Contributors: Karl-Mihkel Ott
# Last modified: 2022-11-24

from sugupuu.id import Id
from sugupuu.person import Person
import sugupuu.dataparse as dataparse
import sys

HELP_TEXT = "When using generic mode:\n"\
            "\t>help - show the help text\n"\
            "\t>select by eid|name|spouse_name|spouse_eid - if succeeds, activates the selection mode\n"\
            "\t>list [filter name|eid|spouse_name|spouse_eid ...] - lists all people in current family tree\n"\
            "\t>exit|quit - exit the application\n"\
            "When using selection mode:\n"\
            "\t>help - show the help text\n"\
            "\t>children [filter eid|name|spouse_name|spouse_eid ...] [recursive] [level <N>] - output children data\n"\
            "\t>spouse [filter eid|name]- output spouse data\n"\
            "\t>info [filter name|eid|spouse_name|spouse_eid ...]- output information about currently selected person\n"\
            "\t>exit|quit - exit to generic mode\n"

# Check if any arguments were passed into the program
tree = {}
if len(sys.argv) == 1:
    name = input("Enter the file name: ")
    tree = dataparse.read_from_file(name)
else:
    tree = dataparse.read_from_file(sys)

# Main program loop
print("Type `help` to get information about the usage of the program")

while True:
    ipt = input("(sugupuu)> ")

    if ipt == "help":
        print(HELP_TEXT, end='')
    elif ipt == "exit" or ipt == "quit":
        break
    else:
        print(f"Unknown command '{ipt}'")

