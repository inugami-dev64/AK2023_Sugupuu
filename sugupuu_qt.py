# File sugupuu_cli.py - sugupuu cli application
# Contributors: Karl-Mihkel Ott
# Last modified: 2022-11-24

from re import sub
# from typing import Self
from sugupuu.id import Id
from sugupuu.person import Person
import sugupuu.dataparse as dataparse
import sugupuu.treesearch as treesearch
import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QLineEdit, QLabel, QComboBox, QTabWidget, QPushButton, QVBoxLayout, QHBoxLayout, QTableView, QCheckBox
from PyQt5.QtGui import QStandardItem, QStandardItemModel

# Bits for filtering 
FILTER_BIT_NAME = 0b0001
FILTER_BIT_EID = 0b0010
FILTER_BIT_SPOUSE_NAME = 0b0100
FILTER_BIT_SPOUSE_EID = 0b1000
FILTER_BIT_ALL = 0b1111

HELP_TEXT = "When using generic mode:\n"\
            "\t>help - show the help text\n"\
            "\t>select by eid|name|spouse_name|spouse_eid <val> - if succeeds, activates the selection mode\n"\
            "\t>list [filter name|eid|spouse_name|spouse_eid ...] - lists all people in current family tree\n"\
            "\t>exit|quit - exit the application\n"\
            "When using selection mode:\n"\
            "\t>help - show the help text\n"\
            "\t>children [recurse] [level <N>] [filter eid|name|spouse_name|spouse_eid ...] - output children data\n"\
            "\t>spouse [filter eid|name]- output spouse data\n"\
            "\t>info [filter eid|name|spouse_name|spouse_eid ...]- output information about currently selected person\n"\
            "\t>add_child - prompt to add a new child for currently selected person\n"\
            "\t>exit|quit - exit to generic mode\n"

class State:
    is_generic: bool
    person: Person

    def __init__(self):
        self.is_generic = True


# Attempt to change into selection mode if possible
# If it isn't possible, output corresponding message
def change_to_selection_mode(person, state: State):
    if person == None:
        print("Could not find a person with given properties")
    else:
        state.is_generic = False
        state.person = person


# Output data about person according to specified filter bits
def filter_and_output_person_data(person: Person, tree: {}, filter_bits: int):
    out=''
    
    if filter_bits & FILTER_BIT_NAME:
        
        out+=f"Name: {person.name}\n"
    if filter_bits & FILTER_BIT_EID:
        
        out+=f"Estonian ID: {person.eid.format_string()}\n"
    if filter_bits & FILTER_BIT_SPOUSE_NAME and person.spouse_eid.century != 0:
        
        out+=f"Spouse name: {tree[person.spouse_eid.format_int()].name}\n"
    if filter_bits & FILTER_BIT_SPOUSE_EID and person.spouse_eid.century != 0:
        
        out+=f"Spouse Estonian ID: {person.spouse_eid.format_string()}\n"
    return out


# Output data about person's children according to speficied filter bits
def filter_and_output_children_data(children: [], tree: {}, filter_bits: int):
    out=""
    for child in children:
        
        out+=f"\nGeneration: {child[1]}\n"
        if filter_bits & FILTER_BIT_NAME:
            
            out+=f"Name: {child[0].name}\n"
        if filter_bits & FILTER_BIT_EID:
            
            out+=f"Estonian ID: {child[0].eid.format_string()}\n"
        if filter_bits & FILTER_BIT_SPOUSE_NAME and child[0].spouse_eid.century != 0:
            
            out+=f"Spouse name: {tree[child[0].spouse_eid.format_int()].name}\n"
        if filter_bits & FILTER_BIT_SPOUSE_EID and child[0].spouse_eid.century != 0:
            
            out+=f"Spouse Estonian ID: {child[0].spouse_eid.format_string()}\n"
    return out


# Add a child to person  
def add_child(person: Person, tree: {}, name:str, childEid:int, str_spouse_eid:int ):
    # name = input("Enter child's name > ")
    eid = Id()
    eid.int_to_eid(childEid)
    spouse_eid = Id()
    # str_spouse_eid = input("Enter spouse's ID number > ")
    if str_spouse_eid != '':
        spouse_eid.int_to_eid(str_spouse_eid)

    person.children.append(eid)
    child = Person(
        name,
        eid,
        spouse_eid,
        []
    )
    tree[eid.format_int()] = child


def only_numerics(seq):
    seq_type= type(seq)
    return seq_type().join(filter(seq_type.isdigit, seq))
    
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.state=State()
        self.tree = dataparse.read_from_file("test.txt")
        self.setWindowTitle("Sugupuu")
        self.person={}
        
        layout=QVBoxLayout()
        layout.setSpacing(16)
        layout.setContentsMargins(8,8,8,8)

        # Add search bar
        Line1=QHBoxLayout()
        Line1.setSpacing(16)
        self.SearchBy=QComboBox()
        self.SearchParam=QLineEdit()
        self.SearchBy.addItems(["eid", "name", "spouse_eid", "spouse_name"])
        for i in [QLabel("Search by"), self.SearchBy, self.SearchParam]:
            Line1.addWidget(i)
        widget1=QWidget()
        widget1.setLayout(Line1)
        layout.addWidget(widget1)

        # Add table view to display data
        self.table_view = QTableView()
        self.table_model = QStandardItemModel(self.table_view)
        self.table_view.setModel(self.table_model)
        self.table_view.horizontalHeader().setStretchLastSection(True)
        # filtering bits
        filterLayout=QHBoxLayout()
        self.filter_eid = QCheckBox("Estonian ID")
        self.filter_name = QCheckBox("Name")
        self.filter_spouse_eid = QCheckBox("Spouse Estonian ID")
        self.filter_spouse_name = QCheckBox("Spouse Name")
        self.filter_alive = QCheckBox("Alive")

        # Add output label for selected person's data
        self.output=QLabel()
        self.output.setStyleSheet("background-color: #efefeffe; border: 1px solid #ddd;")
        layout.addWidget(self.output)

        # Add Child 
        AddChildrenLayout=QHBoxLayout()
        layout.addWidget(QLabel("Add Child\nThe first parent is that who you have searched above"))
        self.childName=QLineEdit()
        self.childEID=QLineEdit()
        self.childSpouseEID=QLineEdit()
        self.addChildButton=QPushButton()
        self.addChildButton.setText("Add Child to tree")
        
        # set input mask Id only inputs 
        self.childSpouseEID.setInputMask("00000000000")
        self.childEID.setInputMask("00000000000")
        
        for i in [QLabel("name"), self.childName, QLabel("EID"), self.childEID, QLabel("Other parent EID"), self.childSpouseEID, self.addChildButton]:
            AddChildrenLayout.addWidget(i)
        AddChild=QWidget()
        AddChild.setLayout(AddChildrenLayout)
        layout.addWidget(AddChild)
        
        for i in [self.filter_eid, self.filter_name, self.filter_spouse_eid, self.filter_spouse_name]:
            i.setChecked(True)
            filterLayout.addWidget(i)
        # add the filter checks
        filterLayW=QWidget()
        filterLayW.setLayout(filterLayout)
        layout.addWidget(filterLayW)
        layout.addWidget(self.table_view)
        
        mainWidget=QWidget()
        mainWidget.setLayout(layout)
        self.setCentralWidget(mainWidget)
        
        # Connect search bar signal to searchby slot
        self.SearchParam.returnPressed.connect(self.searchby)

        self.addChildButton.clicked.connect(self.addperson)

        # Populate table view with data on startup
        self.update_table_view()

        self.filter_name.stateChanged.connect(self.update_table_view)
        self.filter_eid.stateChanged.connect(self.update_table_view)
        self.filter_spouse_name.stateChanged.connect(self.update_table_view)
        self.filter_spouse_eid.stateChanged.connect(self.update_table_view)
        self.filter_alive.stateChanged.connect(self.update_table_view)

    def update_table_view(self):
        self.table_model.clear()
        labels=[]
        for key in self.tree:
            person = self.tree[key]
            row = []
            if self.filter_eid.isChecked():
                row.append(QStandardItem(person.eid.format_string()))
            if self.filter_name.isChecked():
                row.append(QStandardItem(person.name))
            if self.filter_spouse_eid.isChecked():
                row.append(QStandardItem('-' if person.spouse_eid is None else person.spouse_eid.format_string()))
            if self.filter_spouse_name.isChecked():
                if person.spouse_eid.century != 0:
                    spouse_name = '-' if person.spouse_eid is None else self.tree[person.spouse_eid.format_int()].name
                    row.append(QStandardItem(spouse_name))
            if self.filter_alive.isChecked() and not person.is_alive():
                continue
            self.table_model.appendRow(row)
        if self.filter_eid.isChecked(): labels.append("Estonian ID") 
        if self.filter_name.isChecked(): labels.append("Name") 
        if self.filter_spouse_eid.isChecked(): labels.append("Spouse EID") 
        if self.filter_spouse_name.isChecked(): labels.append("Spouse name") 
        self.table_model.setHorizontalHeaderLabels(labels)

    def searchby(self):
        text=self.SearchParam.text()
        if self.SearchBy.currentText()=="eid" or self.SearchBy.currentText()=="spouse_eid": 
            text = sub("[^\d\.]", "", text)
        if text == "": return
        if self.SearchBy.currentText()=="eid":
            self.person=treesearch.search_by_int_eid(int(text), self.tree)
        elif self.SearchBy.currentText()=="name":
            self.person=treesearch.search_by_name(text, self.tree)
        elif self.SearchBy.currentText()=="spouse_eid":
            self.person=treesearch.search_by_spouse_int_eid(int(text), self.tree)
        elif self.SearchBy.currentText()=="spouse_name":
            self.person=treesearch.search_by_spouse_name(text, self.tree)
        if self.person is not None: 
            # self.output.setText(filter_and_output_person_data(person, self.tree, FILTER_BIT_ALL))
            children = treesearch.search_children(self.person, 1, self.tree)
            out=filter_and_output_person_data(self.person, self.tree, FILTER_BIT_ALL)
            out+=filter_and_output_children_data(children, self.tree, FILTER_BIT_ALL)
            self.output.setText(out)
            
    def addperson(self):
        name= self.childName.text()
        childEid=int(self.childEID.text())
        spouse_eid=int(self.childSpouseEID.text())
        add_child(self.person, self.tree, name, childEid, spouse_eid )
        

if __name__ == '__main__':
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()