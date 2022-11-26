# File sugupuu_cli.py - sugupuu cli application
# Contributors: Karl-Mihkel Ott
# Last modified: 2022-11-24

from sugupuu.id import Id
from sugupuu.person import Person
import sugupuu.dataparse as dataparse
import sugupuu.treesearch as treesearch
import sys

# Bits for filtering 
FILTER_BIT_NAME = 0b0001
FILTER_BIT_EID = 0b0010
FILTER_BIT_SPOUSE_NAME = 0b0100
FILTER_BIT_SPOUSE_EID = 0b1000
FILTER_BIT_ALL = 0b1111

HELP_TEXT = "When using generic mode:\n"\
            "\t>help - show the help text\n"\
            "\t>select by eid|name|spouse_name|spouse_eid <val> - if succeeds, activates the selection mode\n"\
            "\t>list [filter name|eid|spouse_name|spouse_eid ...] - lists all people in current family tree\n"\
            "\t>exit|quit - exit the application\n"\
            "When using selection mode:\n"\
            "\t>help - show the help text\n"\
            "\t>children [level <N>] [filter eid|name|spouse_name|spouse_eid ...] - output children data\n"\
            "\t>spouse [filter eid|name]- output spouse data\n"\
            "\t>info [filter eid|name|spouse_name|spouse_eid ...]- output information about currently selected person\n"\
            "\t>add_child - prompt to add a new child for currently selected person\n"\
            "\t>exit|quit - exit to generic mode\n"

class State:
    is_generic: bool
    person: Person

    def __init__(self):
        self.is_generic = True


# Attempt to change into selection mode if possible
# If it isn't possible, output corresponding message
def change_to_selection_mode(person, state: State):
    if person == None:
        print("Could not find a person with given properties")
    else:
        state.is_generic = False
        state.person = person


# Output data about person according to specified filter bits
def filter_and_output_person_data(person: Person, tree: {}, filter_bits: int):
    print()
    if filter_bits & FILTER_BIT_NAME:
        print(f"Name: {person.name}")
    if filter_bits & FILTER_BIT_EID:
        print(f"Estonian ID: {person.eid.format_string()}")
    if filter_bits & FILTER_BIT_SPOUSE_NAME and person.spouse_eid.century != 0:
        print(f"Spouse name: {tree[person.spouse_eid.format_int()].name}")
    if filter_bits & FILTER_BIT_SPOUSE_EID and person.spouse_eid.century != 0:
        print(f"Spouse Estonian ID: {person.spouse_eid.format_string()}")


# Output data about person's children according to speficied filter bits
def filter_and_output_children_data(children: [], tree: {}, filter_bits: int):
    for child in children:
        print(f"\nGeneration: {child[1]}")
        if filter_bits & FILTER_BIT_NAME:
            print(f"Name: {child[0].name}")
        if filter_bits & FILTER_BIT_EID:
            print(f"Estonian ID: {child[0].eid.format_string()}")
        if filter_bits & FILTER_BIT_SPOUSE_NAME and child[0].spouse_eid.century != 0:
            print(f"Spouse name: {tree[child[0].spouse_eid.format_int()].name}")
        if filter_bits & FILTER_BIT_SPOUSE_EID and child[0].spouse_eid.century != 0:
            print(f"Spouse Estonian ID: {child[0].spouse_eid.format_string()}")


# Parse generic mode command
def parse_generic(cmd: str, tree: {}, state: State):
    if cmd == "help":
        print(HELP_TEXT, end='')
    elif cmd == "exit" or cmd == "quit":
        sys.exit(0)

    # Command can be select, list or unknown
    else:
        words = cmd.split(' ')
        if len(words) == 4 and words[0] == "select" and words[1] == "by":
            if words[2] == "eid":
                person = treesearch.search_by_int_eid(int(words[3]), tree)
                change_to_selection_mode(person, state)
            elif words[2] == "name":
                person = treesearch.search_by_name(words[3], tree)
                change_to_selection_mode(person, state)
            elif words[2] == "spouse_name":
                person = treesearch.search_by_spouse_name(words[3], tre)
                change_to_selection_mode(person, state)
            elif words[2] == "spouse_eid":
                person = treesearch.search_by_spouse_int_eid(int(words[3]), tree)
                change_to_selection_mode(person, state)
        elif len(words) >= 1 and words[0] == "list":
            filter_bits = 0
            if len(words) > 1 and words[1] == "filter":
                for i in range(2, len(words)):
                    if words[i] == "eid":
                        filter_bits = filter_bits | FILTER_BIT_EID
                    elif words[i] == "name":
                        filter_bits = filter_bits | FILTER_BIT_NAME
                    elif words[i] == "spouse_name":
                        filter_bits = filter_bits | FILTER_BIT_SPOUSE_NAME
                    elif words[i] == "spouse_eid":
                        filter_bits = filter_bits | FILTER_BIT_SPOUSE_EID
            else:
                filter_bits = FILTER_BIT_ALL
            
            for key in tree:
                filter_and_output_person_data(tree[key], tree, filter_bits)

        else:
            print(f"Unknown command: {cmd}")

# Add a child to person  
def add_child(person: Person, tree: {}):
    name = input("Enter child's name > ")
    eid = Id()
    eid.int_to_eid(int(input("Enter child's ID number > ")))
    spouse_eid = Id()
    spouse_eid.int_to_eid(int(input("Enter spouse's ID number > ")))

    tree[eid.format_int()] = Person(
        name,
        eid,
        spouse_eid,
        []
    )

                

# Parse selection mode command
def parse_selection(cmd: str, tree: {}, state: State):
    if cmd == "help":
        print(HELP_TEXT, end='')
    elif cmd == "add_child":
        add_child(state.person, tree)
    elif cmd == "exit" or cmd == "quit":
        state.is_generic = True
    else:
        words = cmd.split(' ')

        # Output children data
        if words[0] == "children":
            level = 1
            filter_bits = 0
            capture_filter = False

            i = 1
            while(i < len(words)):
                if not capture_filter:
                    if words[i] == "level" and i != len(words) - 1:
                        level = int(words[i+1])
                        i = i + 1
                    elif words[i] == "filter":
                        capture_filter = True
                    else:
                        print(f"Unknown command: {cmd}")
                        break
                else:
                    if words[i] == "eid":
                        filter_bits = filter_bits | FILTER_BIT_EID
                    elif words[i] == "name":
                        filter_bits = filter_bits | FILTER_BIT_NAME
                    elif words[i] == "spouse_name":
                        filter_bits = filter_bits | FILTER_BIT_SPOUSE_NAME
                    elif words[i] == "spouse_eid":
                        filter_bits = filter_bits | FILTER_BIT_SPOUSE_EID
                    else:
                        print(f"Unknown command: {cmd}")
                        return
                i = i + 1

            # if filter bits are zero - then no explicit filtering will be done
            if filter_bits == 0:
                filter_bits = FILTER_BIT_ALL

            children = treesearch.search_children(state.person, level, tree)
            filter_and_output_children_data(children, tree, filter_bits)
        elif words[0] == "spouse":
            # No spouse present
            if state.person.spouse_eid.century == 0:
                return

            # Check for output filters
            filter_bits = 0
            if len(words) > 1 and words[1] == "filter":
                for i in range(2, len(words)):
                    if words[i] == "eid":
                        filter_bits = filter_bits | FILTER_BIT_EID
                    elif words[i] == "name":
                        filter_bits = filter_bits | FILTER_BIT_NAME
                    else:
                        print(f"Unknown command: {cmd}")
                        return
            else:
                filter_bits = FILTER_BIT_EID | FILTER_BIT_NAME

            filter_and_output_person_data(tree[state.person.spouse_eid.format_int()], tree, filter_bits)

        else:
            print(f"Unknown command: {cmd}")


# Main loop function
def loop(tree):
    state = State()

    # Main program loop
    print("Type `help` to get information about the usage of the program")
    while True:
        if state.is_generic:
            cmd = input("(sugupuu)> ")
            parse_generic(cmd, tree, state)
        else:
            cmd = input(f"(sugupuu)[{state.person.name}]> ")
            parse_selection(cmd, tree, state)


# Check if any arguments were passed into the program
tree = {}
if len(sys.argv) <= 1:
    name = input("Enter the file name: ")
    tree = dataparse.read_from_file(name)
else:
    tree = dataparse.read_from_file(sys.argv[1])

loop(tree)
