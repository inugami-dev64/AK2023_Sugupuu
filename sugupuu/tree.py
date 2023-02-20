# File: tree.py - family tree operations file
# Contributors: Karl-Mihkel Ott

from sugupuu.id import Id
from sugupuu.person import Person
import sugupuu.data as data


def binary_KMP(pat: str, txt: str):
    lps = [0]*len(pat)
    l = 0
    for i in range(1, len(pat)):
        if pat[i] == pat[l]:
            l += 1
            lps[i] = l
        else:
            if l != 0:
                l = lps[l-1]
                i -= 1
            else:
                lps[i] = 0

    i = 0
    j = 0
    while (len(txt) - i) >= (len(pat) - j):
        if pat[j] == txt[i]:
            i += 1
            j += 1

        if j == len(pat):
            return True

        elif i < len(txt) and pat[j] != txt[i]:
            if j != 0:
                j = lps[j-1]
            else:
                i += 1

    return False


def search_by_int_eid(int_eid: int, tree: {}):
    for key in tree:
        if binary_KMP(str(int_eid), str(tree[key].eid.format_int())):
            return tree[key]

    return None



def search_by_name(name: str, tree: {}):
    for eid in tree:
        if binary_KMP(name.lower(), tree[eid].name.lower()):
            return tree[eid]

    return None



def search_by_spouse_name(spouse_name: str, tree: {}):
    for eid in tree:
        if tree[eid].spouse_eid.century != 0 and binary_KMP(spouse_name.lower(), tree[tree[eid].spouse_eid.format_int()].name.lower()):
            return tree[eid]
        elif tree[eid].name == spouse_name:
            return tree[tree[eid].spouse_eid.format_int()]

    return None



def search_by_spouse_int_eid(spouse_eid: int, tree: {}):
    eid = Id()
    eid.int_to_eid(spouse_eid)

    for key in tree:
        if binary_KMP(str(eid.format_int()), str(tree[key].spouse_eid.format_int())):
            return tree[key]

    return None


# Search all children for given person
def search_children(person: Person, level: int, tree: {}, recursive=True):
    if level == 0:
        return []
    
    children = []
    queue = []

    # Push first generation children
    for child in person.children:
        if recursive:
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




# Add a child to person  
def add_child(parent1: Person, parent2: Person, tree: {}, name: str, child_eid: int, int_spouse_eid: int, filename: str):
    eid = Id()
    eid.int_to_eid(child_eid)
    spouse_eid = Id()
    spouse_eid.int_to_eid(int_spouse_eid)

    parent1.children.append(eid)
    parent2.children.append(eid)
    child = Person(
        name,
        eid,
        spouse_eid,
        []
    )
    tree[eid.format_int()] = child
    data.save(tree, filename)

