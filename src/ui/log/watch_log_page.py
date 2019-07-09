#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Author: Tuncay ÇOLAK <tuncay.colak@tubitak.gov.tr>

import os
from PyQt5.QtWidgets import (QGridLayout, QGroupBox, QVBoxLayout, QWidget, QTextEdit, QPushButton)
from ui.message_box.message_box import MessageBox

class WatchLog(QWidget):
    def __init__(self, parent=None):
        super(WatchLog, self).__init__(parent)
        self.liderdb_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../dist/liderdb.json')

        self.log_out_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../dist/installer.log')

        if not os.path.exists(os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../dist')):
            os.makedirs(os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../dist'))

        self.data = None
        self.msg = MessageBox()

        ## database parameters
        self.log_name = QTextEdit()
        self.log_name.setReadOnly(True)
        self.log_name.setMinimumSize(200, 600)
        self.refreshButton = QPushButton("Yenile")

        ## Log Layout
        logGroup = QGroupBox("Lider Ahenk Kurulum İzle")
        self.logLayout = QGridLayout()
        self.logLayout.addWidget(self.log_name)

        logGroup.setLayout(self.logLayout)

        mainLayout = QVBoxLayout()
        mainLayout.addWidget(logGroup)
        mainLayout.addSpacing(12)
        mainLayout.addWidget(self.refreshButton)
        mainLayout.addStretch(1)
        self.setLayout(mainLayout)
        self.append_logger()
        self.refreshButton.clicked.connect(self.refresh_log)


    def append_logger(self):
        if os.path.exists(self.log_out_path):
            self.log_name.setText("")
            with open(self.log_out_path) as f:
                for line in f:
                    self.log_name.append(str(line))

    def refresh_log(self):
        if os.path.exists(self.log_out_path):
            self.log_name.setText("")
            with open(self.log_out_path) as f:
                for line in f:
                    self.log_name.append(str(line))
        else:
            self.log_name.setText("")
            self.msg.information("installer.log dosyası bulunamadı")




