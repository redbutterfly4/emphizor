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
    QStatusBar, QTextEdit, QVBoxLayout, QWidget, QSpacerItem)
from PySide6.QtGui import QAction

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(800, 600)
        MainWindow.setDocumentMode(False)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        
        self.mainHorizontalLayout = QHBoxLayout(self.centralwidget)
        self.mainHorizontalLayout.setObjectName(u"mainHorizontalLayout")
        
        self.sidebarWidget = QWidget(self.centralwidget)
        self.sidebarWidget.setObjectName(u"sidebarWidget")
        self.sidebarWidget.setMaximumSize(QSize(250, 16777215))
        self.sidebarWidget.setMinimumSize(QSize(200, 0))
        
        self.verticalLayout = QVBoxLayout(self.sidebarWidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        
        self.pushButton = QPushButton(self.sidebarWidget)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setAutoDefault(False)
        self.pushButton.setDefault(True)
        self.verticalLayout.addWidget(self.pushButton)

        self.label = QLabel(self.sidebarWidget)
        self.label.setObjectName(u"label")
        self.label.setFrameShape(QFrame.Shape.NoFrame)
        self.label.setFrameShadow(QFrame.Shadow.Plain)
        self.verticalLayout.addWidget(self.label)
        
        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        self.verticalLayout.addItem(self.verticalSpacer)
        
        self.mainHorizontalLayout.addWidget(self.sidebarWidget)

        self.contentWidget = QWidget(self.centralwidget)
        self.contentWidget.setObjectName(u"contentWidget")
        
        self.AddCartIntaerfaceLayout = QVBoxLayout(self.contentWidget)
        self.AddCartIntaerfaceLayout.setObjectName(u"AddCartIntaerfaceLayout")
        
        self.CardDescripitionLayout = QHBoxLayout()
        self.CardDescripitionLayout.setObjectName(u"CardDescripitionLayout")
        
        self.CardDescriptionLabel = QLabel(self.contentWidget)
        self.CardDescriptionLabel.setObjectName(u"CardDescriptionLabel")
        self.CardDescriptionLabel.setMinimumSize(QSize(150, 0))
        self.CardDescriptionLabel.setMaximumSize(QSize(150, 70))
        self.CardDescripitionLayout.addWidget(self.CardDescriptionLabel)

        self.CardDescriptionTextEdit = QTextEdit(self.contentWidget)
        self.CardDescriptionTextEdit.setObjectName(u"CardDescriptionTextEdit")
        self.CardDescripitionLayout.addWidget(self.CardDescriptionTextEdit)

        self.AddCartIntaerfaceLayout.addLayout(self.CardDescripitionLayout)

        self.CardAnswerLayout = QHBoxLayout()
        self.CardAnswerLayout.setObjectName(u"CardAnswerLayout")
        
        self.CardAnswerLabel = QLabel(self.contentWidget)
        self.CardAnswerLabel.setObjectName(u"CardAnswerLabel")
        self.CardAnswerLabel.setMinimumSize(QSize(150, 0))
        self.CardAnswerLabel.setMaximumSize(QSize(150, 16777215))
        self.CardAnswerLayout.addWidget(self.CardAnswerLabel)

        self.textEdit = QTextEdit(self.contentWidget)
        self.textEdit.setObjectName(u"textEdit")
        self.CardAnswerLayout.addWidget(self.textEdit)

        self.AddCartIntaerfaceLayout.addLayout(self.CardAnswerLayout)

        self.buttonsLayout = QHBoxLayout()
        self.buttonsLayout.setObjectName(u"buttonsLayout")
        
        self.addCartButton = QPushButton(self.contentWidget)
        self.addCartButton.setObjectName(u"addCartButton")
        self.buttonsLayout.addWidget(self.addCartButton)

        self.viewCardsButton = QPushButton(self.contentWidget)
        self.viewCardsButton.setObjectName(u"viewCardsButton")
        self.buttonsLayout.addWidget(self.viewCardsButton)

        self.practiceButton = QPushButton(self.contentWidget)
        self.practiceButton.setObjectName(u"practiceButton")
        self.buttonsLayout.addWidget(self.practiceButton)
        
        self.AddCartIntaerfaceLayout.addLayout(self.buttonsLayout)
        
        self.contentVerticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        self.AddCartIntaerfaceLayout.addItem(self.contentVerticalSpacer)

        self.mainHorizontalLayout.addWidget(self.contentWidget)

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

