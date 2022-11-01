import json
import random

from PySide6 import QtCore, QtWidgets, QtGui
import sys


class MyWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        self.edit_window = None
        self.app = QtWidgets.QApplication([])
        super(MyWidget, self).__init__(parent)
        self.lineedits  = None
        self.field_one  = QtWidgets.QLineEdit()
        self.field_two  = QtWidgets.QLineEdit()
        add_btn    = QtWidgets.QPushButton("Add")
        mod_btn    = QtWidgets.QPushButton("Edit Labels")
        self.test_btn  = QtWidgets.QPushButton("TEST")

        self.form_layout = QtWidgets.QFormLayout()
        self.form_layout.setLabelAlignment(QtCore.Qt.AlignRight)

        button_layout = QtWidgets.QVBoxLayout()

        under_layout   = QtWidgets.QVBoxLayout(self)

        under_layout.addLayout(self.form_layout)
        under_layout.addLayout(button_layout)

        self.setLayout(under_layout)
        button_layout.addWidget(add_btn)
        button_layout.addWidget(mod_btn)
        button_layout.addWidget(self.test_btn)
        add_btn.clicked.connect(self.add_to_json)
        mod_btn.clicked.connect(self.edit_labels)
        self.test_btn.clicked.connect(self.test)
        self.refresh_main_window()

    def refresh_main_window(self):

        while self.form_layout.count()>0:
            self.form_layout.removeRow(0)

        with open('labels.json') as json_file:
            label_data = json.load(json_file)  # Loads file

        edit_col_list = []

        for count, values in enumerate(label_data.values()):
            edit_col_list.append(QtWidgets.QLineEdit())
            self.form_layout.addRow(QtWidgets.QLabel(str(values)), edit_col_list[count])

    def show_app(self):
        # self.resize(800, 600)
        self.show()
        sys.exit(self.app.exec_())

    def count(self):
        pass

    def add_to_json(self):
        data = self.create_dict()
        with open('data_dump.json', "w") as outfile:
            json.dump(data, outfile, indent=2)

    def create_dict(self):
        data = {
           random.randint(0,1000000000):
               [
                   {
                       'name':  self.field_one.text(),
                       'order': self.field_two.text()
                   }
               ]
        }
        print(data)
        return data

    def print(self):
        print(self.field_one.text())
        print(self.field_two.text())

    # TODO refresh main window with new labels
    def edit_labels(self):
        def update_labels():
            label_data_dict.clear()
            for counter, text in enumerate(label_edit_list):
                users_new_label = label_edit_list[counter].text()
                label_data_dict[str(counter)] = users_new_label

            with open('labels.json', 'w') as label_file:
                json.dump(label_data_dict, label_file, indent=2)

            self.refresh_main_window()
            self.edit_window.close()

        def del_row():
            last_row_num = len(label_edit_list)
            label_edit_list.pop()
            flayout.removeRow(last_row_num-1)

        def add_row():
            new_key = len(label_edit_list)+1
            label_data_dict[str(new_key)] = str(new_key)
            json_key_list.append(str(new_key))
            label_edit_list.append(QtWidgets.QLineEdit(text=str(new_key)))
            user_label_list.append(str(new_key))
            flayout.addRow(str(new_key), label_edit_list[new_key-1])

        self.edit_window = QtWidgets.QWidget()
        flayout = QtWidgets.QFormLayout()
        flayout.setLabelAlignment(QtCore.Qt.AlignRight)
        vlayout = QtWidgets.QVBoxLayout()
        vlayout.addLayout(flayout)
        self.edit_window.setLayout(vlayout)

        cancel_btn = QtWidgets.QPushButton("Cancel")
        add_btn = QtWidgets.QPushButton("Add Row")
        submit_btn = QtWidgets.QPushButton("Submit")
        del_btn = QtWidgets.QPushButton("Delete Last Row")

        label_data_dict = None
        json_key_list = []
        user_label_list = []
        label_edit_list = []

        with open('labels.json') as json_file:
            label_data_dict = json.load(json_file)  # Loads file

        for count, key in enumerate(label_data_dict):
            value = label_data_dict[key]
            json_key_list.append(key)
            user_label_list.append(value)
            label_edit_list.append(QtWidgets.QLineEdit(text=value))
            flayout.addRow(key, label_edit_list[count])

        vlayout.addWidget(add_btn)
        vlayout.addWidget(del_btn)
        vlayout.addWidget(submit_btn)
        vlayout.addWidget(cancel_btn)

        submit_btn.clicked.connect(update_labels)
        cancel_btn.clicked.connect(self.edit_window.close)
        add_btn.clicked.connect(add_row)
        del_btn.clicked.connect(del_row)

        self.edit_window.show()

    def test(self):
        dict = {
          "employees": [
            {
              "name": "John Doe",
              "department": "Marketing",
              "place": "Remote"
            }
          ]
        }
        with open('test.json', 'w') as label_file:
            json.dump(dict, label_file, indent=2)
        print("TEST FUN END")


if __name__ == "__main__":

    widget = MyWidget()
    widget.show_app()