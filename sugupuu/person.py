class Person:
    name: str
    eid: int
    spouse_eid: int
    children: []

    def __init__(self):
        self.name = "John Smith"
        self.eid = 35411110289
        self.spouse_eid = 0

    def __init__(self, _name, _eid, _spouse_eid, _children):
        self.name = _name
        self.eid = _eid
        self.spouse_eid = _spouse_eid
        self.children = _children
