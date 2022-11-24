# File: generate_dataset.py - family tree generation script
# Contributors: Karl-Mihkel Ott
# Last modified: 2022-11-24

import random
import heapq
import names
from copy import deepcopy
from sugupuu.person import Person
from sugupuu.id import Id

# Use random.py library to generate semi-random Estonian ID number
def generate_random_eid(_centuryset):
    eid = Id()
    eid.century = random.sample(_centuryset, k=1)[0]
    y = 0
    if eid.century == 3 or eid.century == 1:
        eid.year = random.randrange(0, 100)
    else:
        eid.year = random.randrange(0, 22)

    eid.month = random.randrange(1, 13)
    eid.day = random.randrange(1, 29)
    eid.special = int(random.random() * 10**4)

    return eid


# Utility function to print EIDs in accending order using heapq
def print_eids(male_eids, female_eids):
    print("Male:")
    while(male_eids):
        print(heapq.heappop(male_eids).format_string())

    print("\nFemale:")
    while(female_eids):
        print(heapq.heappop(female_eids).format_string())


# Generate N male members and N female members
def generate_data_set(N):
    # each parent has max 3 children
    child_count = 2
    male_eids = []
    female_eids = []

    for i in range(N):
        eid = generate_random_eid([1, 3, 5])
        male_eids.append(eid)

        eid = generate_random_eid([2, 4, 6])
        female_eids.append(eid)


    people = []

    tree = []
    queue = []
    heapq.heappush(queue, heapq.heappop(male_eids))

    # construct the tree
    while queue:
        eid = heapq.heappop(queue)
        spouse_eid = Id()
        if male_eids or female_eids:
            if eid.century == 1 or eid.century == 3 or eid.century == 5:
                spouse_eid = deepcopy(heapq.heappop(female_eids))
            else:
                spouse_eid = deepcopy(heapq.heappop(male_eids))

        children = []
        while len(children) < child_count and (female_eids or male_eids):
            if len(male_eids) < len(female_eids):
                child = deepcopy(heapq.heappop(female_eids))
                children.append(child)
                heapq.heappush(queue, child)
            else:
                child = deepcopy(heapq.heappop(male_eids))
                children.append(child)
                heapq.heappush(queue, child)

        if eid.century in [1, 3, 5]:
            people.append(Person(
                names.get_first_name(gender='male'),
                eid,
                spouse_eid,
                children
            ))
        else:
            people.append(Person(
                names.get_first_name(gender='female'),
                eid,
                spouse_eid,
                children
            ))

        if spouse_eid.century != 0:
            people.append(Person(
                names.get_first_name(gender='female'),
                spouse_eid,
                eid,
                children
            ))

    return people


# Entry point
N = int(input())
people = generate_data_set(N)

for person in people:
    print(person.format_string())

