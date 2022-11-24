class Id:
    century: int
    year: int
    month: int
    day: int
    special: int

    def __init__(self):
        self.century = 0
        self.year = 0
        self.month = 0
        self.day = 1
        self.special = 0

    def __lt__(self, other):
        if self.century != other.century:
            return self.century < other.century;
        elif self.year != other.year:
            return self.year < other.year
        elif self.month != other.month:
            return self.month < other.month
        else:
            return self.day < other.day

    def format_string(self):
        return f"{self.century}{self.year:02}{self.month:02}{self.day:02}{self.special:04}"
