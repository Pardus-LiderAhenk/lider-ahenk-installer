#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Author: Tuncay ÇOLAK <tuncay.colak@tubitak.gov.tr>

from PyQt5.QtWidgets import (QGridLayout, QGroupBox, QLabel, QLineEdit, QWidget)

class StatusPage(QWidget):
    def __init__(self, parent=None):
        super(StatusPage, self).__init__(parent)
        self.install_status = QLineEdit()
        self.statusLabel = QLabel()
        # self.log_name.setMinimumHeight(100)
        self.install_status.setReadOnly(True)
        self.install_status.setPlaceholderText("Lider Ahenk Kurulum")

        ## Install Status Layout
        self.statusGroup = QGroupBox()
        self.statusLayout = QGridLayout()
        self.statusLayout.addWidget(self.statusLabel,0,0)
        self.statusLayout.addWidget(self.install_status,0,1)
        self.statusGroup.setLayout(self.statusLayout)