from PySide6.QtWidgets import QApplication, QMainWindow, QDialog, QLineEdit, QVBoxLayout, QLabel
from design import Ui_MainWindow
class MainWindow(QMainWindow):
    tags : list[str]
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.pushButton.clicked.connect(self.add_tag_clicked)

    def add_tag_clicked(self):
        temp_dialog = QDialog(self)
        temp_dialog.setFixedHeight(400)
        temp_dialog.setFixedWidth(400)
        temp_dialog.setWindowTitle('Add tag')
        temp_layout = QVBoxLayout(temp_dialog)
        temp_label = QLabel(temp_dialog)
        temp_label.setFixedWidth(150)
        temp_label.setText('Enter tag name:')

        
        
        temp_dialog.show()

        
        

def main():
    app = QApplication()
    window = MainWindow()
    window.show()
    app.exec()

if __name__ == "__main__":
    main()