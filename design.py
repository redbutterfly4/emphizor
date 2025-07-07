# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'design.ui'
##
## Created by: Qt User Interface Compiler version 6.9.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QApplication, QFrame, QHBoxLayout, QLabel,
    QMainWindow, QMenu, QMenuBar, QPushButton,
    QSizePolicy, QSpacerItem, QStatusBar, QTextEdit,
    QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(800, 600)
        MainWindow.setDocumentMode(False)
        self.actionSave = QAction(MainWindow)
        self.actionSave.setObjectName(u"actionSave")
        self.actionfirst_color = QAction(MainWindow)
        self.actionfirst_color.setObjectName(u"actionfirst_color")
        self.actionsecond_color = QAction(MainWindow)
        self.actionsecond_color.setObjectName(u"actionsecond_color")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.mainHorizontalLayout = QHBoxLayout(self.centralwidget)
        self.mainHorizontalLayout.setObjectName(u"mainHorizontalLayout")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.pushButton = QPushButton(self.centralwidget)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setAutoDefault(False)

        self.verticalLayout.addWidget(self.pushButton)

        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")
        self.label.setFrameShape(QFrame.Shape.NoFrame)
        self.label.setFrameShadow(QFrame.Shadow.Plain)

        self.verticalLayout.addWidget(self.label)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)


        self.mainHorizontalLayout.addLayout(self.verticalLayout)

        self.AddCardInterfaceLayout = QVBoxLayout()
        self.AddCardInterfaceLayout.setObjectName(u"AddCardInterfaceLayout")
        self.CardDescripitionLayout = QHBoxLayout()
        self.CardDescripitionLayout.setObjectName(u"CardDescripitionLayout")
        self.CardDescriptionLabel = QLabel(self.centralwidget)
        self.CardDescriptionLabel.setObjectName(u"CardDescriptionLabel")
        self.CardDescriptionLabel.setMinimumSize(QSize(150, 0))
        self.CardDescriptionLabel.setMaximumSize(QSize(150, 70))

        self.CardDescripitionLayout.addWidget(self.CardDescriptionLabel)

        self.CardDescriptionTextEdit = QTextEdit(self.centralwidget)
        self.CardDescriptionTextEdit.setObjectName(u"CardDescriptionTextEdit")

        self.CardDescripitionLayout.addWidget(self.CardDescriptionTextEdit)


        self.AddCardInterfaceLayout.addLayout(self.CardDescripitionLayout)

        self.CardAnswerLayout = QHBoxLayout()
        self.CardAnswerLayout.setObjectName(u"CardAnswerLayout")
        self.CardAnswerLabel = QLabel(self.centralwidget)
        self.CardAnswerLabel.setObjectName(u"CardAnswerLabel")
        self.CardAnswerLabel.setMinimumSize(QSize(150, 0))
        self.CardAnswerLabel.setMaximumSize(QSize(150, 16777215))

        self.CardAnswerLayout.addWidget(self.CardAnswerLabel)

        self.textEdit = QTextEdit(self.centralwidget)
        self.textEdit.setObjectName(u"textEdit")

        self.CardAnswerLayout.addWidget(self.textEdit)


        self.AddCardInterfaceLayout.addLayout(self.CardAnswerLayout)

        self.buttonsLayout = QHBoxLayout()
        self.buttonsLayout.setObjectName(u"buttonsLayout")
        self.addCartButton = QPushButton(self.centralwidget)
        self.addCartButton.setObjectName(u"addCartButton")

        self.buttonsLayout.addWidget(self.addCartButton)

        self.viewCardsButton = QPushButton(self.centralwidget)
        self.viewCardsButton.setObjectName(u"viewCardsButton")

        self.buttonsLayout.addWidget(self.viewCardsButton)

        self.practiceButton = QPushButton(self.centralwidget)
        self.practiceButton.setObjectName(u"practiceButton")

        self.buttonsLayout.addWidget(self.practiceButton)


        self.AddCardInterfaceLayout.addLayout(self.buttonsLayout)

        self.contentVerticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.AddCardInterfaceLayout.addItem(self.contentVerticalSpacer)


        self.mainHorizontalLayout.addLayout(self.AddCardInterfaceLayout)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 800, 23))
        self.menuFile = QMenu(self.menubar)
        self.menuFile.setObjectName(u"menuFile")
        self.menuColor = QMenu(self.menubar)
        self.menuColor.setObjectName(u"menuColor")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuColor.menuAction())
        self.menuFile.addAction(self.actionSave)
        self.menuColor.addAction(self.actionfirst_color)
        self.menuColor.addAction(self.actionsecond_color)

        self.retranslateUi(MainWindow)

        self.pushButton.setDefault(True)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Emphizor", None))
        self.actionSave.setText(QCoreApplication.translate("MainWindow", u"Save", None))
#if QT_CONFIG(shortcut)
        self.actionSave.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+S", None))
#endif // QT_CONFIG(shortcut)
        self.actionfirst_color.setText(QCoreApplication.translate("MainWindow", u"first color", None))
        self.actionsecond_color.setText(QCoreApplication.translate("MainWindow", u"second color", None))
        self.pushButton.setText(QCoreApplication.translate("MainWindow", u"Add tag ", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"Your tags:", None))
        self.CardDescriptionLabel.setText(QCoreApplication.translate("MainWindow", u"Enter card description:", None))
        self.CardAnswerLabel.setText(QCoreApplication.translate("MainWindow", u"Enter card answer:", None))
        self.addCartButton.setText(QCoreApplication.translate("MainWindow", u"Add card", None))
        self.viewCardsButton.setText(QCoreApplication.translate("MainWindow", u"View Cards", None))
        self.practiceButton.setText(QCoreApplication.translate("MainWindow", u"Practice", None))
        self.menuFile.setTitle(QCoreApplication.translate("MainWindow", u"File", None))
        self.menuColor.setTitle(QCoreApplication.translate("MainWindow", u"Color", None))
    # retranslateUi

