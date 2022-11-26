# File: treesearch.py - family tree member search algorithms
# Contributors: Karl-Mihkel Ott
# Last modified: 2022-11-24

from sugupuu.id import Id
from sugupuu.person import Person
import sugupuu.dataparse as dataparse

# mostly O(1), sometimes O(N)
def search_by_int_eid(int_eid: int, tree: {}):
    if not int_eid in tree:
        print(f"Invalid EID: {str(int_eid)}")
        return None

    return tree[int_eid]

# O(N)
def search_by_name(name: str, tree: {}):
    for eid in tree:
        if tree[eid].name == name:
            return tree[eid]

    return None


# O(N)
def search_by_spouse_name(spouse_name: str, tree: {}):
    for eid in tree:
        if tree[eid].spouse_eid.century != 0 and tree[tree[eid].spouse_eid.format_int()].name == spouse_name:
            return tree[eid]
        elif tree[eid].name == spouse_name:
            return tree[tree[eid].spouse_eid.format_int()]

    return None


# O(N)
def search_by_spouse_eid(spouse_eid: int, tree: {}):
    eid = Id()
    eid.int_to_eid(spouse_eid)

    for key in tree:
        if tree[key].spouse_eid == eid:
            return tree[key]
        elif key == eid:
            return tree[eid]

    return None


# Search all children for given person
def search_children(person: Person, level: int, tree: {}):
    if level == 0:
        return []
    
    children = []
    queue = []

    # Push first generation children
    for child in person.children:
        children.append((tree[child.format_int()], 1))
        queue.append((child, 1))

    while queue:
        qchild = queue.pop(0)
        if qchild[1] == level:
            break

        for child in tree[qchild[0].format_int()].children:
            children.append((tree[child.format_int()], qchild[1]+1))
            queue.append((child, qchild[1]+1))

    return children
