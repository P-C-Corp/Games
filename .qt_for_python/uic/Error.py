# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'c:\Users\mathe\Documents\code\Games\Morpion\GUI\ui\Error.ui'
#
# Created by: PyQt5 UI code generator 5.15.6
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(531, 130)
        Form.setStyleSheet("")
        self.Comment = QtWidgets.QLabel(Form)
        self.Comment.setGeometry(QtCore.QRect(530, 90, 171, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.Comment.setFont(font)
        self.Comment.setObjectName("Comment")
        self.logText = QtWidgets.QTextBrowser(Form)
        self.logText.setGeometry(QtCore.QRect(0, 130, 531, 192))
        self.logText.setObjectName("logText")
        self.label = QtWidgets.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(20, -20, 491, 91))
        font = QtGui.QFont()
        font.setPointSize(13)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(Form)
        self.label_2.setGeometry(QtCore.QRect(20, 50, 501, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.here = QtWidgets.QLabel(Form)
        self.here.setGeometry(QtCore.QRect(310, 55, 55, 21))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.here.setFont(font)
        self.here.setObjectName("here")
        self.View = QtWidgets.QPushButton(Form)
        self.View.setGeometry(QtCore.QRect(320, 90, 93, 28))
        self.View.setObjectName("View")
        self.cancel = QtWidgets.QPushButton(Form)
        self.cancel.setGeometry(QtCore.QRect(420, 90, 93, 28))
        self.cancel.setObjectName("cancel")
        self.ResetFiles = QtWidgets.QPushButton(Form)
        self.ResetFiles.setGeometry(QtCore.QRect(220, 90, 93, 28))
        self.ResetFiles.setObjectName("ResetFiles")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Morpion by PetchouDev"))
        self.Comment.setText(_translate("Form", "You won the game !"))
        self.label.setText(_translate("Form", "The application went into an internal error"))
        self.label_2.setText(_translate("Form", "Please consider report this error        and include logs."))
        self.here.setText(_translate("Form", "here"))
        self.View.setText(_translate("Form", "view the log"))
        self.cancel.setText(_translate("Form", "Cancel"))
        self.ResetFiles.setText(_translate("Form", "Reset files"))