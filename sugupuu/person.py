from sugupuu.id import Id

class Person:
    name: str
    eid: Id
    spouse_eid: Id
    children: []

    def __init__(self):
        self.name = "John Smith"

    def __init__(self, _name, _eid, _spouse_eid, _children):
        self.name = _name
        self.eid = _eid
        self.spouse_eid = _spouse_eid
        self.children = _children

    def format_string(self):
        fstr = f"{self.name}*{self.eid.format_string()}"
        if self.spouse_eid.century != 0:
            fstr = fstr + f"*{self.spouse_eid.format_string()}"
        
        for child in self.children:
            fstr = fstr + f"*{child.format_string()}"

        fstr = fstr + '#'

        return fstr



