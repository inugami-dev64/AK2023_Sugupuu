import random
import names
from sugupuu/person import Person
from sugupuu/id import Id


# The generic structure of 11 number Estonian ID code is following:
#   1: 1 - for 19th century male, 2 - for 19th century female, 3 - for 20th century male, 4 - for 20th century female, 5 - for 21th centrury male, 6 - for 21th centrury female
#   2-3: year of birth
#   4-5: month of birth
#   6-7: day of birth
#   8-11: special identification code (probably derived from hospital of birth IIRC)
def generate_random_male_eid(olderthan=Id()):
    eid = Id()
    eid.century = random.sample([1, 3, 5], k=1)
    y = 0
    if eid.century == 3 or eid.century == 1:
        eid.year = random.randrange(0, 100)
    else:
        eid.year = random.randrange(0, 22)

    eid.month = random.randrange(0, 13)
    eid.day = random.randrange(0, 31)
    eid.special = int(random.random() * 10**4)


def generate_data_set(N):
    for i in range(N)

N = int(input())
names.get_full_name()
