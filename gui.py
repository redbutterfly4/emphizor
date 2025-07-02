from PySide6.QtWidgets import QApplication, QMainWindow, QDialog, QLineEdit, QVBoxLayout, QLabel, QHBoxLayout, QDialogButtonBox, QPushButton
from design import Ui_MainWindow
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
        temp_dialog = QDialog(self)
        temp_dialog.setFixedHeight(400)
        temp_dialog.setFixedWidth(400)
        temp_dialog.setWindowTitle(title)
        temp_layout = QHBoxLayout(temp_dialog)
        temp_label = QLabel(temp_dialog)
        temp_label.setFixedWidth(75)
        temp_label.setText(label_message)
        temp_line_edit = QLineEdit(temp_dialog)
        temp_line_edit.setFixedWidth(250)
        temp_layout.addWidget(temp_label)
        temp_layout.addWidget(temp_line_edit)

        temp_button_box = QDialogButtonBox(QDialogButtonBox.Ok)

        temp_button_box.setParent(temp_dialog)
        temp_layout.addWidget(temp_button_box)

        def accept_button_pressed():
            temp_dialog.close()
            
        
        temp_dialog.show()
        temp_button_box.accepted.connect(accept_button_pressed)
        return temp_line_edit.text()

    def add_tag_button(self, tag_name):
        pass
            
    def add_tag_clicked(self):
       new_tag_name = self.enter_string_dialog('Enter tag: ', 'Add tag')
       
           
           

        
        

def main():
    app = QApplication()
    window = MainWindow()
    window.show()
    app.exec()

if __name__ == "__main__":
    main()