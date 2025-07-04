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
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QFrame, QHBoxLayout, QLabel,
    QMainWindow, QMenuBar, QPushButton, QSizePolicy,
    QStatusBar, QTextEdit, QVBoxLayout, QWidget)
from PySide6.QtGui import QAction

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(800, 600)
        MainWindow.setDocumentMode(False)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayoutWidget = QWidget(self.centralwidget)
        self.verticalLayoutWidget.setObjectName(u"verticalLayoutWidget")
        self.verticalLayoutWidget.setGeometry(QRect(10, 0, 111, 551))
        self.verticalLayout = QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.pushButton = QPushButton(self.verticalLayoutWidget)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setAutoDefault(False)

        self.verticalLayout.addWidget(self.pushButton)

        self.label = QLabel(self.verticalLayoutWidget)
        self.label.setObjectName(u"label")
        self.label.setFrameShape(QFrame.Shape.NoFrame)
        self.label.setFrameShadow(QFrame.Shadow.Plain)

        self.verticalLayout.addWidget(self.label)

        self.verticalLayoutWidget_2 = QWidget(self.centralwidget)
        self.verticalLayoutWidget_2.setObjectName(u"verticalLayoutWidget_2")
        self.verticalLayoutWidget_2.setGeometry(QRect(129, 3, 511, 551))
        self.AddCartIntaerfaceLayout = QVBoxLayout(self.verticalLayoutWidget_2)
        self.AddCartIntaerfaceLayout.setObjectName(u"AddCartIntaerfaceLayout")
        self.AddCartIntaerfaceLayout.setContentsMargins(0, 0, 0, 0)
        self.CardDescripitionLayout = QHBoxLayout()
        self.CardDescripitionLayout.setObjectName(u"CardDescripitionLayout")
        self.CardDescriptionLabel = QLabel(self.verticalLayoutWidget_2)
        self.CardDescriptionLabel.setObjectName(u"CardDescriptionLabel")
        self.CardDescriptionLabel.setMinimumSize(QSize(175, 0))
        self.CardDescriptionLabel.setMaximumSize(QSize(175, 70))

        self.CardDescripitionLayout.addWidget(self.CardDescriptionLabel)

        self.CardDescriptionTextEdit = QTextEdit(self.verticalLayoutWidget_2)
        self.CardDescriptionTextEdit.setObjectName(u"CardDescriptionTextEdit")

        self.CardDescripitionLayout.addWidget(self.CardDescriptionTextEdit)


        self.AddCartIntaerfaceLayout.addLayout(self.CardDescripitionLayout)

        self.CardAnswerLayout = QHBoxLayout()
        self.CardAnswerLayout.setObjectName(u"CardAnswerLayout")
        self.CardAnswerLabel = QLabel(self.verticalLayoutWidget_2)
        self.CardAnswerLabel.setObjectName(u"CardAnswerLabel")
        self.CardAnswerLabel.setMinimumSize(QSize(175, 0))
        self.CardAnswerLabel.setMaximumSize(QSize(175, 16777215))

        self.CardAnswerLayout.addWidget(self.CardAnswerLabel)

        self.textEdit = QTextEdit(self.verticalLayoutWidget_2)
        self.textEdit.setObjectName(u"textEdit")

        self.CardAnswerLayout.addWidget(self.textEdit)


        self.AddCartIntaerfaceLayout.addLayout(self.CardAnswerLayout)

        self.addCartButton = QPushButton(self.verticalLayoutWidget_2)
        self.addCartButton.setObjectName(u"addCartButton")
        self.addCartButton.setMaximumSize(QSize(16777215, 16777215))
        self.addCartButton.setFlat(False)

        self.AddCartIntaerfaceLayout.addWidget(self.addCartButton)

        self.viewCardsButton = QPushButton(self.verticalLayoutWidget_2)
        self.viewCardsButton.setObjectName(u"viewCardsButton")
        self.viewCardsButton.setMaximumSize(QSize(16777215, 16777215))
        self.viewCardsButton.setFlat(False)

        self.AddCartIntaerfaceLayout.addWidget(self.viewCardsButton)

        self.practiceButton = QPushButton(self.verticalLayoutWidget_2)
        self.practiceButton.setObjectName(u"practiceButton")
        self.practiceButton.setMaximumSize(QSize(16777215, 16777215))
        self.practiceButton.setFlat(False)

        self.AddCartIntaerfaceLayout.addWidget(self.practiceButton)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 800, 23))
        self.menuFile = self.menubar.addMenu(u"File")
        self.menuFile.setObjectName(u"menuFile")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.actionSave = QAction(MainWindow)
        self.actionSave.setObjectName(u"actionSave")
        self.menuFile.addAction(self.actionSave)

        self.retranslateUi(MainWindow)

        self.pushButton.setDefault(True)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Emphizor", None))
        self.pushButton.setText(QCoreApplication.translate("MainWindow", u"Add tag ", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"Your tags:", None))
        self.CardDescriptionLabel.setText(QCoreApplication.translate("MainWindow", u"Enter card description:", None))
        self.CardAnswerLabel.setText(QCoreApplication.translate("MainWindow", u"Enter card answer:", None))
        self.addCartButton.setText(QCoreApplication.translate("MainWindow", u"Add card", None))
        self.viewCardsButton.setText(QCoreApplication.translate("MainWindow", u"View Cards", None))
        self.practiceButton.setText(QCoreApplication.translate("MainWindow", u"Practice", None))
        self.actionSave.setText(QCoreApplication.translate("MainWindow", u"Save", None))
        self.actionSave.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+S", None))
    # retranslateUi

