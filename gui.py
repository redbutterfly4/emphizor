from PySide6.QtWidgets import QApplication, QMainWindow, QDialog
from design import Ui_MainWindow
class MainWindow(QMainWindow):
    tags : list[str]
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.pushButton.clicked.connect(self.add_tag_clicked)

    def add_tag_clicked(self):
        dialog = QDialog(self)
        dialog.setFixedHeight(400)
        dialog.setFixedWidth(400)
        dialog.setWindowTitle('Add tag')
        dialog.show()
        

def main():
    app = QApplication()
    window = MainWindow()
    window.show()
    app.exec()

if __name__ == "__main__":
    main()