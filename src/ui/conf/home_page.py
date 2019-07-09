#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Author: Tuncay ÇOLAK <tuncay.colak@tubitak.gov.tr>

import os
from PyQt5.QtWidgets import (QGridLayout, QGroupBox, QLabel, QLineEdit, QWidget, QPushButton, QVBoxLayout)
from install_manager import InstallManager
from api.util.util import Util
from ui.message_box.message_box import MessageBox
import ui.conf.configdialog_rc


class HomePage(QWidget):
    def __init__(self, parent=None):
        super(HomePage, self).__init__(parent)

        self.im = InstallManager()
        self.msg_box = MessageBox()
        self.data = None

        ## database parameters
        self.dbNameLabel = QLabel("Veritabanı Adı:")
        self.db_name = QLineEdit()
        self.db_name.setPlaceholderText("liderdb")
        self.dbUsernameLabel = QLabel("Veritabanı Kullanıcı Adı:")
        self.db_username = QLineEdit()
        self.db_username.setPlaceholderText("root")
        self.dbPwdLabel = QLabel("Veritabanı Kullanıcı Parolası:")
        self.db_password = QLineEdit()
        self.db_password.setEchoMode(QLineEdit.Password)
        self.db_password.setPlaceholderText("****")
        self.startUpdateButton = QPushButton("Kuruluma Başla")

        ## Database Layout
        dbGroup = QGroupBox()
        dbGroup.setMinimumHeight(600)
        dbGroup.setStyleSheet("border-image: url(:/images/liderahenk-wiev.png)")


        self.dbLayout = QGridLayout()
        # self.dbLayout.addWidget(self.dbNameLabel, 0, 0)
        # self.dbLayout.addWidget(self.db_name, 0, 1)
        # self.dbLayout.addWidget(self.dbUsernameLabel, 1, 0)
        # self.dbLayout.addWidget(self.db_username, 1, 1)
        # self.dbLayout.addWidget(self.dbPwdLabel, 2, 0)
        # self.dbLayout.addWidget(self.db_password, 2, 1)
        dbGroup.setLayout(self.dbLayout)


        mainLayout = QVBoxLayout()
        mainLayout.addWidget(dbGroup)
        mainLayout.addSpacing(12)
        mainLayout.addStretch(1)
        self.setLayout(mainLayout)






