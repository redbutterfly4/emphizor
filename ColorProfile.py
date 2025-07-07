from PySide6.QtGui import QColor
class ColorProfile:
    main_color: QColor
    gradient_end_color: QColor
    def __init__(self, main_color = '#667eea', gradient_end_color = '#764ba2'):
        self.main_color = QColor(main_color)
        self.gradient_end_color = QColor(gradient_end_color)
