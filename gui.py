from PySide6.QtWidgets import QApplication, QMainWindow, QDialog, QLineEdit, QVBoxLayout, QLabel, QHBoxLayout, QDialogButtonBox, QPushButton
from design import Ui_MainWindow
from EnterStringDialog import EnterStringDialog
from base_classes import FullCard
class MainWindow(QMainWindow):
    tags : set[str]
    tag_buttons : list[QPushButton]
    tag_len_limit = 50
    enter_string_dialog : EnterStringDialog
    def __init__(self):
        super().__init__()
        self.tags = []  # Initialize the tags attribute as an empty list
        self.tag_buttons = [] # Initialize empty list of buttons
        self.ui = Ui_MainWindow() 
        self.ui.setupUi(self) # setting ui from Qt Designer
        self.ui.pushButton.clicked.connect(self.add_tag_clicked) # connect "Add tag button" with slot
    def create_enter_string_dialog(self, label_message, title):
        self.enter_string_dialog = EnterStringDialog(label_message,title,self,self.tag_len_limit)
        self.enter_string_dialog.accepted.connect(self.add_tag_button)
    def add_tag_button(self):
        if not self.enter_string_dialog.line_edit.text() in self.tags:
            self.tags.append(self.enter_string_dialog.line_edit.text())
            button = QPushButton(self)
            button.setText(self.enter_string_dialog.line_edit.text())
            self.ui.verticalLayout.addWidget(button)
            self.tag_buttons.append(button)
    def add_tag_clicked(self):
       self.create_enter_string_dialog('Enter tag: ', 'Add tag')
def main():
    app = QApplication()
    window = MainWindow()
    window.show()
    app.exec()

if __name__ == "__main__":
    main()