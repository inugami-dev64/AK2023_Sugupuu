# File sugupuu_cli.py - sugupuu cli application
# Contributors: Karl-Mihkel Ott
# Last modified: 2022-11-24

from re import sub

# Internal module imports
from sugupuu.id import Id
from sugupuu.person import Person
import sugupuu.data as data
import sugupuu.tree as tree
import sugupuu.textformat as fmt
import sys

# PyQt5 imports
from PyQt5 import uic
from PyQt5.QtWidgets import (
    QApplication, 
    QMainWindow, 
    QWidget, 
    QLineEdit, 
    QLabel, 
    QComboBox, 
    QTabWidget, 
    QPushButton, 
    QVBoxLayout, 
    QHBoxLayout, 
    QTableView, 
    QFileDialog,
    QCheckBox)

from PyQt5.QtGui import QStandardItem, QStandardItemModel

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.filename = self.pick_file()
        if self.filename == "":
            sys.exit(0)

        self.tree = data.read_from_file(self.filename)
        self.setWindowTitle("AsiKarikas 2023 Sugupuu")
        self.person={}

        layout=QVBoxLayout()
        layout.setSpacing(16)
        layout.setContentsMargins(8,8,8,8)

        # Add search bar
        Line1=QHBoxLayout()
        Line1.setSpacing(16)
        self.SearchBy=QComboBox()
        self.SearchParam=QLineEdit()
        self.SearchBy.addItems(["EID", "Name", "Spouse EID", "Spouse Name"])
        for i in [QLabel("Search by"), self.SearchBy, self.SearchParam]:
            Line1.addWidget(i)
        widget1=QWidget()
        widget1.setLayout(Line1)
        layout.addWidget(widget1)

        # Add table view to display data
        self.table_view = QTableView()
        self.table_model = QStandardItemModel(self.table_view)
        self.table_model.itemChanged.connect(self.entry_changed)
        self.table_view.setModel(self.table_model)
        self.table_view.horizontalHeader().setStretchLastSection(True)
        # filtering bits
        filterLayout=QHBoxLayout()
        self.filter_eid = QCheckBox("Estonian ID")
        self.filter_name = QCheckBox("Name")
        self.filter_spouse_eid = QCheckBox("Spouse Estonian ID")
        self.filter_spouse_name = QCheckBox("Spouse Name")

        # Add output label for selected person's data
        self.output=QLabel()
        self.output.setStyleSheet("background-color: #efefeffe; border: 1px solid #ddd;")
        layout.addWidget(self.output)

        # Add Child 
        AddChildrenLayout=QHBoxLayout()
        layout.addWidget(QLabel("Add a Child\nThe first parent is that who you have searched above.\nThe second parent is first's spouse."))
        self.childName=QLineEdit()
        self.childEID=QLineEdit()
        self.childSpouseEID=QLineEdit()
        self.addChildButton=QPushButton()
        self.addChildButton.setText("Add Child to tree")
        
        # set input mask Id only inputs 
        self.childSpouseEID.setInputMask("00000000000")
        self.childEID.setInputMask("00000000000")
        
        for i in [QLabel("Name"), self.childName, QLabel("EID"), self.childEID, QLabel("Spouse EID"), self.childSpouseEID, self.addChildButton]:
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
        
        mainWidget = QWidget()
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


    def pick_file(self):
        dlg = QFileDialog()
        dlg.setFileMode(QFileDialog.AnyFile)
        dlg.setNameFilter("Text files (*.txt)")
        dlg.setViewMode(QFileDialog.ViewMode.List)

        if dlg.exec():
            filenames = dlg.selectedFiles()

            if filenames:
                return filenames[0]

        
        return ""


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
            self.table_model.appendRow(row)

        if self.filter_eid.isChecked(): 
            labels.append("Estonian ID") 
        if self.filter_name.isChecked(): 
            labels.append("Name") 
        if self.filter_spouse_eid.isChecked(): 
            labels.append("Spouse EID") 
        if self.filter_spouse_name.isChecked(): 
            labels.append("Spouse name") 
        self.table_model.setHorizontalHeaderLabels(labels)


    def entry_changed(self, entry):

        # Check if EID column was changed
        if entry.column() == 0:
            new_eid = Id()
            new_eid.int_to_eid(int(self.table_model.item(entry.row(), entry.column()).text()))

            i = 0
            person = Person()
            for key in self.tree:
                if i == entry.row():
                    person = self.tree[key]
                    self.tree.pop(key)
                    break
                i += 1

            person.eid = new_eid
            self.tree[new_eid.format_int()] = person
        # Name column was changed
        elif entry.column() == 1:
            name = str(self.table_model.item(entry.row(), entry.column()).text())
            eid = int(self.table_model.item(entry.row(), 0).text())
            self.tree[eid].name = name
        # Spouse EID was changed
        elif entry.column() == 2:
            spouse_eid = Id()
            spouse_eid.int_to_eid(int(self.table_model.item(entry.row(), entry.column()).text()))
            eid = int(self.table_model.item(entry.row(), 0).text())
            self.tree[eid].spouse_eid = spouse_eid

        data.save(self.tree, self.filename)



    def searchby(self):
        text=self.SearchParam.text()
        if self.SearchBy.currentText()=="EID" or self.SearchBy.currentText()=="Spouse EID": 
            text = sub("[^\d\.]", "", text)

        if text == "": 
            return

        if self.SearchBy.currentText()=="EID":
            self.person=tree.search_by_int_eid(int(text), self.tree)

        elif self.SearchBy.currentText()=="Name":
            self.person=tree.search_by_name(text, self.tree)

        elif self.SearchBy.currentText()=="Spouse EID":
            self.person=tree.search_by_spouse_int_eid(int(text), self.tree)

        elif self.SearchBy.currentText()=="Spouse Name":
            self.person=tree.search_by_spouse_name(text, self.tree)

        # Output search result data to internal console
        if self.person is not None:
            children = tree.search_children(self.person, 1, self.tree)
            out = fmt.filter_and_output_person_data(self.person, self.tree, fmt.FILTER_BIT_ALL)
            out += fmt.filter_and_output_children_data(children, self.tree, fmt.FILTER_BIT_ALL)
            self.output.setText(out)
            
    def addperson(self):
        name= self.childName.text()
        child_eid = int(self.childEID.text())

        str_spouse = self.childSpouseEID.text()
        if str_spouse == '':
            str_spouse = '0'


        spouse_eid = int(str_spouse)
        if self.person:
            if not int(str_spouse) in self.tree:
                tree.add_child(self.person, None, self.tree, name, child_eid, spouse_eid, self.filename)
            else:
                tree.add_child(self.person, self.tree[int(str_spouse)], self.tree, name, child_eid, spouse_eid, self.filename)
        else:
            tree.add_child(None, None, self.tree, name, child_eid, spouse_eid, self.filename)

        self.update_table_view()
        

if __name__ == '__main__':
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()
