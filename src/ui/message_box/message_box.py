#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Author: Tuncay ÇOLAK <tuncay.colak@tubitak.gov.tr>

import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QMessageBox
from PyQt5.QtCore import QStringListModel

try:
    _fromUtf8 = QStringListModel.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

class MessageBox(QWidget):

    def __init__(self):
        super().__init__()
        self.title = 'Lider Ahenk Bilgilendirme'
        self.msgBox = QMessageBox()
        self.width = 320
        self.height = 500

    def information(self, message):
        self.msgBox.setMinimumSize(self.width, self.height)
        self.msgBox.setIcon(self.msgBox.Information)
        self.msgBox.setWindowTitle(self.title)

        self.msgBox.setInformativeText(_fromUtf8(str(message)))
        self.msgBox.setDefaultButton(QMessageBox.Ok)
        self.msgBox.exec_()
        self.msgBox.setDefaultButton(QMessageBox.No)

    def about(self, message):
        QMessageBox.about(self, "Lider Ahenk Kurulum Uygulaması", message)

    def warning(self, message):

        self.msgBox.setMinimumSize(self.width, self.height)
        self.msgBox.setIcon(self.msgBox.Warning)
        self.msgBox.setWindowTitle("UYARI")
        self.msgBox.setInformativeText(_fromUtf8(str(message)))
        self.msgBox.setDefaultButton(QMessageBox.Ok)
        self.msgBox.exec_()



if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MessageBox()