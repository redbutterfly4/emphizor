from PySide6.QtWidgets import QApplication, QMainWindow, QDialog, QLineEdit, QVBoxLayout, QLabel, QHBoxLayout, QDialogButtonBox, QPushButton
class EnterStringDialog(QDialog):
    layout : QHBoxLayout
    label : QLabel
    button_box : QDialogButtonBox
    line_edit : QLineEdit
    def accept_button_pressed(self):
        self.close() 
    def __init__(self, label_message,  title, parent):
        super().__init__(parent)
        self.setFixedHeight(400)
        self.setFixedWidth(400)
        self.setWindowTitle(title)
        self.layout = QHBoxLayout(self)
        self.label = QLabel(self)
        self.label.setFixedWidth(75)
        self.label.setText(label_message)
        self.line_edit = QLineEdit(self)
        self.line_edit.setFixedWidth(250)
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.line_edit)

        self.button_box = QDialogButtonBox(QDialogButtonBox.Ok)

        self.button_box.setParent(self)
        self.layout.addWidget(self.button_box)

        self.show()
        self.button_box.accepted.connect(self.accept_button_pressed())

           
        
        