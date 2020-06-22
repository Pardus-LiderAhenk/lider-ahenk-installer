#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Author: Tuncay ÇOLAK <tuncay.colak@tubitak.gov.tr>

import os
import signal
import sys

import psutil
from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (QApplication, QDialog, QHBoxLayout, QListView, QListWidget, QListWidgetItem, QPushButton,
                             QStackedWidget, QVBoxLayout, QSlider)
import ui.conf.configdialog_rc
from ui.conf.home_page import HomePage
from ui.settings.settings_page import SettingsPage
from ui.ejabberd.ejabberd_page import EjabberdPage
from ui.database.db_page import DatabasePage
from ui.ldap.ldap_page import OpenLdapPage
from ui.lider.lider_page import LiderPage
from ui.message_box.message_box import MessageBox
from ui.ahenk.ahenk_page import AhenkPage
from ui.log.watch_log_page import WatchLog
from ui.lider_console.lider_console_page import LiderConsolePage

class ConfigDialog(QDialog):
    def __init__(self, parent=None):
        super(ConfigDialog, self).__init__(parent)

        self.msg_box = MessageBox()
        self.ejabberd = EjabberdPage()
        self.lider_page = LiderPage()

        self.contentsWidget = QListWidget()
        self.contentsWidget.setViewMode(QListView.IconMode)
        self.contentsWidget.setIconSize(QSize(64, 64))
        self.contentsWidget.setMovement(QListView.Static)
        self.contentsWidget.setMaximumWidth(128)
        self.contentsWidget.setMinimumWidth(128)
        self.contentsWidget.setMinimumHeight(700)
        self.contentsWidget.setSpacing(12)

        self.pagesWidget = QStackedWidget()
        self.pagesWidget.setMinimumHeight(800)
        self.pagesWidget.setMinimumWidth(1024)

        self.pagesWidget.addWidget(SettingsPage())
        # self.pagesWidget.addWidget(DatabasePage())
        # self.pagesWidget.addWidget(OpenLdapPage())
        # self.pagesWidget.addWidget(EjabberdPage())
        # self.pagesWidget.addWidget(LiderPage())
        # self.pagesWidget.addWidget(LiderConsolePage())
        # self.pagesWidget.addWidget(AhenkPage())
        # self.pagesWidget.addWidget(WatchLog())
        closeButton = QPushButton("Kapat")
        aboutButton = QPushButton("Hakkında")
        # self.createIcons()
        self.contentsWidget.setCurrentRow(0)
        closeButton.clicked.connect(self.close_page)
        aboutButton.clicked.connect(self.about_lider_installer)

        horizontalLayout = QHBoxLayout()
        # horizontalLayout.addWidget(self.contentsWidget)
        horizontalLayout.addWidget(self.pagesWidget, 1)

        buttonsLayout = QHBoxLayout()
        buttonsLayout.addStretch(0)
        buttonsLayout.addWidget(aboutButton)
        buttonsLayout.addStretch(1)
        buttonsLayout.addWidget(closeButton)

        mainLayout = QVBoxLayout()
        mainLayout.addLayout(horizontalLayout)
        mainLayout.addStretch(1)
        mainLayout.addSpacing(12)
        mainLayout.addLayout(buttonsLayout)

        self.setLayout(mainLayout)
        self.setWindowTitle("Lider Ahenk Kurulum Uygulaması")
        self.setWindowIcon(QIcon(":/images/liderahenk-32.png"))

    def close_page(self):
        for proc in psutil.process_iter():
            # check whether the process name matches
            if proc.name() == "xterm":
                proc.kill()
        self.close()

    def about_lider_installer(self):
        self.msg_box.about("Lider Ahenk Merkezi Yönetim Sistemi Kurulum Uygulaması\nDaha fazla bilgi için...\nwww.liderahenk.org\nVersiyon: 2.0")

    def changePage(self, current, previous):
        if not current:
            current = previous
        self.pagesWidget.setCurrentIndex(self.contentsWidget.row(current))

    def createIcons(self):
        vagrantButton = QListWidgetItem(self.contentsWidget)
        vagrantButton.setIcon(QIcon(':/images/settings.png'))
        vagrantButton.setText("Sunucu\nAyarları")
        vagrantButton.setTextAlignment(Qt.AlignHCenter)
        vagrantButton.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)

        # dbButton = QListWidgetItem(self.contentsWidget)
        # dbButton.setIcon(QIcon(':/images/database.png'))
        # dbButton.setText("Veritabanı")
        # dbButton.setTextAlignment(Qt.AlignHCenter)
        # dbButton.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
        #
        # ldapButton = QListWidgetItem(self.contentsWidget)
        # ldapButton.setIcon(QIcon(':/images/ldap.png'))
        # ldapButton.setText("OpenLDAP")
        # ldapButton.setTextAlignment(Qt.AlignHCenter)
        # ldapButton.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
        #
        # xmppButton = QListWidgetItem(self.contentsWidget)
        # xmppButton.setIcon(QIcon(':/images/ejabberd.png'))
        # xmppButton.setText("Ejabberd")
        # xmppButton.setTextAlignment(Qt.AlignHCenter)
        # xmppButton.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)

        # liderButton = QListWidgetItem(self.contentsWidget)
        # liderButton.setIcon(QIcon(':/images/liderahenk.png'))
        # liderButton.setText("Lider Kur")
        # liderButton.setTextAlignment(Qt.AlignHCenter)
        # liderButton.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)

        # consoleButton = QListWidgetItem(self.contentsWidget)
        # consoleButton.setIcon(QIcon(':/images/lider_console.png'))
        # consoleButton.setText("Lider\nArayüz")
        # consoleButton.setTextAlignment(Qt.AlignHCenter)
        # consoleButton.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)

        # ahenkButton = QListWidgetItem(self.contentsWidget)
        # ahenkButton.setIcon(QIcon(':/images/ahenk.png'))
        # ahenkButton.setText("Ahenk Kur")
        # ahenkButton.setTextAlignment(Qt.AlignHCenter)
        # ahenkButton.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
        #
        # logButton = QListWidgetItem(self.contentsWidget)
        # logButton.setIcon(QIcon(':/images/log.png'))
        # logButton.setText("Log")
        # logButton.setTextAlignment(Qt.AlignHCenter)
        # logButton.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)

        self.contentsWidget.currentItemChanged.connect(self.changePage)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    dialog = ConfigDialog()
    sys.exit(dialog.exec_())
