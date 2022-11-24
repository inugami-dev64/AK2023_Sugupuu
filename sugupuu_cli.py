from sugupuu.id import Id
from sugupuu.person import Person
import sugupuu.dataparse as dataparse

name = input("Enter the file name: ")
print(dataparse.read_from_file(name))

