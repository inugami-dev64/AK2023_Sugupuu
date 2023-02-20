from sugupuu.person import Person

FILTER_BIT_NAME = 0b0001
FILTER_BIT_EID = 0b0010
FILTER_BIT_SPOUSE_NAME = 0b0100
FILTER_BIT_SPOUSE_EID = 0b1000
FILTER_BIT_ALL = 0b1111


# Output data about person according to specified filter bits
def filter_and_output_person_data(person: Person, tree: {}, filter_bits: int):
    out = ''
    if filter_bits & FILTER_BIT_NAME:
        out += f"Name: {person.name}\n"
    if filter_bits & FILTER_BIT_EID:
        out += f"Estonian ID: {person.eid.format_string()}\n"
    if filter_bits & FILTER_BIT_SPOUSE_NAME and person.spouse_eid.century != 0:
        out += f"Spouse name: {tree[person.spouse_eid.format_int()].name}\n"
    if filter_bits & FILTER_BIT_SPOUSE_EID and person.spouse_eid.century != 0:
        out += f"Spouse Estonian ID: {person.spouse_eid.format_string()}\n"

    return out


# Output data about person's children according to speficied filter bits
def filter_and_output_children_data(children: [], tree: {}, filter_bits: int):
    out = ''
    for child in children:
        out += f"\nGeneration: {child[1]}\n"
        if filter_bits & FILTER_BIT_NAME:
            out += f"Name: {child[0].name}\n"
        if filter_bits & FILTER_BIT_EID:
            out += f"Estonian ID: {child[0].eid.format_string()}\n"
        if filter_bits & FILTER_BIT_SPOUSE_NAME and child[0].spouse_eid.century != 0:
            out += f"Spouse name: {tree[child[0].spouse_eid.format_int()].name}\n"
        if filter_bits & FILTER_BIT_SPOUSE_EID and child[0].spouse_eid.century != 0:
            out += f"Spouse Estonian ID: {child[0].spouse_eid.format_string()}\n"

    return out
