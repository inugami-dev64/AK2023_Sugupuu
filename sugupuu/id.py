# File: id.py - Estonian Id class source file
# Contributors: Karl-Mihkel Ott
# Last modified: 2022-11-24


# The generic structure of 11 number Estonian ID code is following:
#   1: 1 - for 19th century male, 2 - for 19th century female, 3 - for 20th century male, 4 - for 20th century female, 5 - for 21th centrury male, 6 - for 21th centrury female
#   2-3: year of birth
#   4-5: month of birth
#   6-7: day of birth
#   8-11: special identification code (probably derived from hospital of birth IIRC)
class Id:
    century: int
    year: int
    month: int
    day: int
    special: int

    # constructor
    def __init__(self, century=0, year=0, month=1, day=1, special=0):
        self.century = century
        self.year = year
        self.month = month
        self.day = day
        self.special = special
    
    # operator< overload for C++ people
    def __lt__(self, other):
        if self.century != other.century:
            return self.century < other.century;
        elif self.year != other.year:
            return self.year < other.year
        elif self.month != other.month:
            return self.month < other.month
        else:
            return self.day < other.day

    # format EID into string value
    def format_string(self):
        return f"{self.century}{self.year:02}{self.month:02}{self.day:02}{self.special:04}"

    # format EID into int value
    def format_int(self):
        return self.century * 10**11 + self.year * 10**9 + self.month * 10**7 + self.day * 10**5 + self.special
