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
        self.width = 1024
        self.height = 500

    def information(self, message):
        msgBox = QMessageBox()
        msgBox.setMinimumSize(self.width, self.height)
        msgBox.setIcon(msgBox.Information)
        msgBox.setWindowTitle(self.title)
        msgBox.setInformativeText(_fromUtf8(str(message)))
        # msgBox.setDefaultButton(QMessageBox.Ok)
        msgBox.addButton('Tamam', QMessageBox.NoRole)
        msgBox.exec_()
        # self.msgBox.setDefaultButton(QMessageBox.No)

    def about(self, message):
        QMessageBox.about(self, "Lider Ahenk Kurulum Uygulaması", message)

    def warning(self, message):
        msgBox = QMessageBox()
        msgBox.setMinimumSize(self.width, self.height)
        msgBox.setIcon(msgBox.Warning)
        msgBox.setWindowTitle("UYARI")
        msgBox.setInformativeText(_fromUtf8(str(message)))
        # msgBox.setDefaultButton(QMessageBox.Ok)
        msgBox.addButton('Tamam', QMessageBox.NoRole)
        msgBox.exec_()

    def install_confirm(self, message):
        msgBox = QMessageBox()
        msgBox.setMinimumSize(self.width, self.height)
        msgBox.setIcon(msgBox.Information)
        msgBox.setWindowTitle(self.title)
        msgBox.setInformativeText(_fromUtf8(str(message)))
        yes_install_button = msgBox.addButton('Evet', QMessageBox.YesRole)
        no_install_button = msgBox.addButton('Hayır', QMessageBox.NoRole)
        msgBox.exec_()

        if msgBox.clickedButton() == yes_install_button:
            return True
        if msgBox.clickedButton() == no_install_button:
            return False

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MessageBox()
