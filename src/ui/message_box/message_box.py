#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Author: Tuncay ÇOLAK <tuncay.colak@tubitak.gov.tr>

import sys
from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QMessageBox
from PyQt6.QtCore import QStringListModel

try:
    _fromUtf8 = QStringListModel.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

class MessageBox(QWidget):

    def __init__(self):
        super().__init__()
        self.title = 'Liderahenk Bilgilendirme'
        self.width = 1024
        self.height = 500

    def information(self, message):
        msgBox = QMessageBox()
        msgBox.setMinimumSize(self.width, self.height)
        msgBox.setIcon(msgBox.Icon.Information)
        msgBox.setWindowTitle(self.title)
        msgBox.setInformativeText(_fromUtf8(str(message)))
        # msgBox.setDefaultButton(QMessageBox.Ok)
        msgBox.addButton('Tamam', QMessageBox.ButtonRole.NoRole)
        msgBox.exec()
        # self.msgBox.setDefaultButton(QMessageBox.No)

    def about(self, message):
        QMessageBox.about(self, "Liderahenk Kurulum Uygulaması", message)

    def warning(self, message):
        msgBox = QMessageBox()
        msgBox.setMinimumSize(self.width, self.height)
        msgBox.setIcon(msgBox.Warning)
        msgBox.setWindowTitle("UYARI")
        msgBox.setInformativeText(_fromUtf8(str(message)))
        # msgBox.setDefaultButton(QMessageBox.Ok)
        msgBox.addButton('Tamam', QMessageBox.ButtonRole.NoRole)
        msgBox.exec()

    def install_confirm(self, message):
        msgBox = QMessageBox()
        msgBox.setMinimumSize(self.width, self.height)
        msgBox.setIcon(msgBox.Icon.Information)
        msgBox.setWindowTitle(self.title)
        msgBox.setInformativeText(_fromUtf8(str(message)))
        yes_install_button = msgBox.addButton('Evet', QMessageBox.ButtonRole.YesRole)
        no_install_button = msgBox.addButton('Hayır', QMessageBox.ButtonRole.NoRole)
        msgBox.exec()

        if msgBox.clickedButton() == yes_install_button:
            return True
        if msgBox.clickedButton() == no_install_button:
            return False

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MessageBox()
