from sugupuu.person import Person
from sugupuu.id import Id
from copy import deepcopy

def int_to_eid(int_eid):
    eid = Id()
    eid.century = int(int_eid / 10**10)
    int_eid = int_eid % 10**10

    eid.year = int(int_eid / 10**8)
    int_eid = int_eid % 10**8

    eid.month = int(int_eid / 10**6)
    int_eid = int_eid % 10**6

    eid.day = int(int_eid / 10**4)
    int_eid = int_eid % 10**4

    eid.special = int_eid
    return eid

def read_eid(line_str, line_nr, pos, filename, throw=True):
    end_bit = False
    eid_pos = line_str.find('*', pos)
    if eid_pos == -1:
        end_bit = True
        eid_pos = line_str.find('#', pos)
        if eid_pos == -1 and throw:
            raise Exception(f"Malformed line {line} in file {filename}")
        elif eid_pos == -1 and not throw:
            return None
    
    eid = int_to_eid(int(line_str[pos:eid_pos]))
    return (eid, end_bit)


def read_from_file(filename):
    f = open(filename, 'r')
    lines = f.readlines()

    # People dictionary
    people = {}

    line_nr = 1
    for line in lines:
        line.encode('utf-8')
        # Read name position
        name_pos = line.find('*', 0)
        if name_pos == -1:
            raise Exception(f"Malformed line {line} in file {filename}")
        name = line[0:name_pos]

        # Read EID position
        end_bit = False
        eid = deepcopy(read_eid(line, line_nr, name_pos+1, filename, throw=True))

        # Optional values: read spouse and children EIDs
        if not eid[1]:
            # Read the spouse EID
            eid_pos = line.find('*', name_pos+1)+1
            spouse_eid = deepcopy(read_eid(line, line_nr, eid_pos, filename, throw=True))

            # Read children eids
            if not spouse_eid[1]:
                children = []
                end_bit = False
                while not end_bit:
                    eid_pos = line.find('*', eid_pos+1)+1
                    child = deepcopy(read_eid(line, line_nr, eid_pos, filename, throw=True))
                    children.append(child[0])
                    end_bit = child[1]

                people[eid[0]] = Person(name, eid[0], spouse_eid[0], children)
            else:
                people[eid[0]] = Person(name, eid[0], spouse_eid[0], [])

        else:
            people[eid[0]] = Person(name, eid[0], Id(), [])
            
        line_nr = line_nr + 1

    f.close()
    return people

