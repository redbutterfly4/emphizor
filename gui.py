from PySide6.QtWidgets import QApplication, QMainWindow, QDialog, QLineEdit, QVBoxLayout, QLabel, QHBoxLayout, QDialogButtonBox, QPushButton
from design import Ui_MainWindow
from EnterStringDialog import EnterStringDialog
class MainWindow(QMainWindow):
    tags : set[str]
    tag_buttons : list[QPushButton]
    tag_len_limit = 50
    def __init__(self):
        super().__init__()
        self.tags = []  # Initialize the tags attribute as an empty list
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.pushButton.clicked.connect(self.add_tag_clicked)

    def enter_string_dialog(self, label_message, title):
        temp_dialog = EnterStringDialog(label_message,title,self)
        

        

    def add_tag_button(self, tag_name):
        button = QPushButton(self)
        button.setText(tag_name)
        self.ui.verticalLayout.addWidget(button)
            
    def add_tag_clicked(self):
       new_tag_name = self.enter_string_dialog('Enter tag: ', 'Add tag')
       self.add_tag_button(new_tag_name)
       
def main():
    app = QApplication()
    window = MainWindow()
    window.show()
    app.exec()

if __name__ == "__main__":
    main()