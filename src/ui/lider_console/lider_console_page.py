#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Author: Tuncay ÇOLAK <tuncay.colak@tubitak.gov.tr>

import os
import json
import subprocess
from PyQt5.QtWidgets import (QGridLayout, QGroupBox, QLabel, QLineEdit, QPushButton, QVBoxLayout, QWidget, QCheckBox)

from install_manager import InstallManager
from ui.message_box.message_box import MessageBox
from ui.log.status_page import StatusPage

class LiderConsolePage(QWidget):
    def __init__(self, parent=None):
        super(LiderConsolePage, self).__init__(parent)
        self.liderdb_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../dist/liderdb.json')
        self.server_list_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../dist/server_list.json')
        self.log_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../dist/installer.log')
        if not os.path.exists(os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../dist')):
            os.makedirs(os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../dist'))

        self.status = StatusPage()
        self.im = InstallManager()
        self.msg_box = MessageBox()
        self.data = None

        ## repository parameters
        self.repoMainBox = QCheckBox("Ana Paket Deposu")
        self.repoTestBox = QCheckBox("Test Paket Deposu")
        self.repoMainBox.setChecked(True)

        self.repoLabel = QLabel("Depo Adresi:")
        self.repo_addr = QLineEdit("deb [arch=amd64] http://repo.liderahenk.org/liderahenk stable main")

        self.repoKeyLdabel = QLabel("Depo Key Dosyası:")
        self.repo_key = QLineEdit("http://repo.liderahenk.org/liderahenk-archive-keyring.asc")

        self.repoMainBox.stateChanged.connect(self.main_repo)
        self.repoTestBox.stateChanged.connect(self.test_repo)

        ## Repository Layout
        self.repoGroup = QGroupBox("Lider Ahenk Paket Deposu Ayarları")
        self.repoLayout = QGridLayout()
        self.repoLayout.addWidget(self.repoMainBox, 0, 0)
        self.repoLayout.addWidget(self.repoTestBox, 0, 1)
        self.repoLayout.addWidget(self.repoLabel, 1, 0)
        self.repoLayout.addWidget(self.repo_addr, 1, 1)
        self.repoLayout.addWidget(self.repoKeyLdabel, 2, 0)
        self.repoLayout.addWidget(self.repo_key, 2, 1)
        self.repoGroup.setLayout(self.repoLayout)

        #self.serverIpLabel = QLabel("Sunucu Adresi:")
        #self.server_ip = QLineEdit()
        #self.server_ip.setPlaceholderText("192.168.*.*")
        self.usernameLabel = QLabel("Kullanıcı Adı:")
        self.username = QLineEdit()
        self.username.setPlaceholderText("lider")
        self.passwordLabel = QLabel("Kullanıcı Parolası:")
        self.password = QLineEdit()
        self.password.setPlaceholderText("****")
        self.password.setEchoMode(QLineEdit.Password)
        self.addButton = QPushButton("Ekle")
        #self.checkControlButton = QPushButton("Bağlantıyı Kontrol Et")
        self.saveButton = QPushButton("Ayarları Kaydet")
        # disabled by default saveButton
        # self.saveButton.setDisabled(True)
        self.addButton.setVisible(False)

        ## Connect Layout
        self.connectGroup = QGroupBox("Lider Arayüz Erişim Bilgileri")
        self.connectLayout = QGridLayout()

        #self.connectLayout.addWidget(self.serverIpLabel, 2, 0)
        #self.connectLayout.addWidget(self.server_ip, 2, 1)
        self.connectLayout.addWidget(self.usernameLabel, 3, 0)
        self.connectLayout.addWidget(self.username, 3, 1)
        self.connectLayout.addWidget(self.passwordLabel, 4, 0)
        self.connectLayout.addWidget(self.password, 4, 1)
        self.connectLayout.addWidget(self.addButton, 5, 2)
        #self.connectLayout.addWidget(self.checkControlButton, 5, 1)
        self.connectGroup.setLayout(self.connectLayout)

        self.installButton = QPushButton("Kuruluma Başla")

        # Install Status Layout
        #self.statusGroup = QGroupBox()
        #self.status.statusLabel.setText("Lİder Arayüz Kurulum Durumu:")
        #self.statusGroup.setLayout(self.status.statusLayout)

        self.mainLayout = QVBoxLayout()
        self.mainLayout.addWidget(self.repoGroup)
        self.mainLayout.addWidget(self.connectGroup)
        self.mainLayout.addSpacing(12)
        self.mainLayout.addWidget(self.installButton)
        #self.mainLayout.addWidget(self.statusGroup)
        self.mainLayout.addStretch(1)
        self.setLayout(self.mainLayout)

        self.installButton.clicked.connect(self.install_lider_console)

    def main_repo(self):

        if self.repoMainBox.isChecked() is True:
            self.repo_addr.setText("deb [trusted=yes] http://repo.liderahenk.org/liderahenk stable main")
            self.repoTestBox.setChecked(False)

    def test_repo(self):

        if self.repoTestBox.isChecked() is True:
            self.repo_addr.setText("deb [trusted=yes] http://repo.liderahenk.org/liderahenk-test testing main")
            self.repoMainBox.setChecked(False)

    def install_lider_console(self):

        self.data = {
            # Server Configuration
            # 'location': "local",
            'location': "remote",
            'ip': "127.0.0.1",
            'username': self.username.text(),
            'password': self.password.text(),
            # Repo Configuration
            'repo_addr': self.repo_addr.text(),
            'repo_key': self.repo_key.text()
        }

        if self.username.text() == "" or self.password.text() == "":
            self.msg_box.warning("Lütfen kullanıcı adını ve kullanıcı parolası giriniz!")
        else:
            #self.status.install_status.setText("Lider Arayüz kurulumu devam ediyor")
            #self.status.install_status.setStyleSheet("background-color: green")

            self.msg_box.information("Lider Arayüz kurulumana başlanacak.")

            subprocess.Popen(["xterm", "-e", "tail", "-f",
                               self.log_path])


            print(self.data)

            self.im.ssh_connect(self.data)
            self.im.install_lider_console(self.data)
            self.im.ssh_disconnect()

            self.msg_box.information("Lider Arayüz kurulumu tamamlandı.\n"
                                     "Kurulum loglarını Log sayfasından inceleyebilirsiniz")
