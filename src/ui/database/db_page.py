#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Author: Tuncay ÇOLAK <tuncay.colak@tubitak.gov.tr>

import os
import json
from PyQt5.QtWidgets import (QGridLayout, QGroupBox, QLabel, QLineEdit, QPushButton, QVBoxLayout, QWidget, QTableWidget)

from install_manager import InstallManager
from ui.message_box.message_box import MessageBox
from ui.log.status_page import StatusPage

class DatabasePage(QWidget):
    def __init__(self, parent=None):
        super(DatabasePage, self).__init__(parent)
        self.liderdb_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../dist/liderdb.json')
        self.server_list_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../dist/server_list.json')
        if not os.path.exists(os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../dist')):
            os.makedirs(os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../dist'))

        self.status = StatusPage()
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
        self.dbGroup = QGroupBox("Veritabanı Konfigürasyon Bilgileri")
        self.dbLayout = QGridLayout()
        self.dbLayout.addWidget(self.dbNameLabel, 0, 0)
        self.dbLayout.addWidget(self.db_name, 0, 1)
        self.dbLayout.addWidget(self.dbUsernameLabel, 1, 0)
        self.dbLayout.addWidget(self.db_username, 1, 1)
        self.dbLayout.addWidget(self.dbPwdLabel, 2, 0)
        self.dbLayout.addWidget(self.db_password, 2, 1)
        self.dbGroup.setLayout(self.dbLayout)

        # Install Status Layout
        self.statusGroup = QGroupBox()
        self.status.statusLabel.setText("Veritabanı Kurulum Durumu:")
        self.statusGroup.setLayout(self.status.statusLayout)

        self.mainLayout = QVBoxLayout()
        self.mainLayout.addWidget(self.dbGroup)
        self.mainLayout.addSpacing(12)
        self.mainLayout.addWidget(self.startUpdateButton)
        self.mainLayout.addWidget(self.statusGroup)
        self.mainLayout.addStretch(1)
        self.setLayout(self.mainLayout)

        self.startUpdateButton.clicked.connect(self.save_db_data)


    def save_db_data(self):

        with open(self.server_list_path) as f:
            server_data = json.load(f)
            if server_data["selection"] == "multi":
                ip = server_data["Veritabanı"][0]["ip"]
                username = server_data["Veritabanı"][0]["username"]
                password = server_data["Veritabanı"][0]["password"]
                location = server_data["Veritabanı"][0]["location"]
            else:
                ip = server_data["ip"]
                username = server_data["username"]
                password = server_data["password"]
                location = server_data["location"]

        self.data = {
            'location': location,

            # Server Configuration
            'ip': ip,
            'username': username,
            'password': password,
            # Database Configuration
            'db_name': self.db_name.text(),
            'db_username': self.db_username.text(),
            'db_password': self.db_password.text(),
            # Repo Configuration
            'repo_addr': server_data["repo_addr"],
            'repo_key': server_data["repo_key"]
        }

        if self.data['db_name'] == "" or self.data['db_username'] == "" or self.data['db_password'] == "":
            self.msg_box.warning("Lütfen aşağıdaki alanları doldurunuz.\n"
                                     "- Veritabanı sunucu bağlantı bilgileri\n"
                                     "- Veritabanı adı\n"
                                     "- Veritabanı kullanıcı adı ve parolası")
        else:
            self.status.install_status.setText("Veritabanı kurulumu devam ediyor...")
            self.status.install_status.setStyleSheet("background-color: green")
            if os.path.exists(self.liderdb_path) and os.stat(self.liderdb_path).st_size != 0:
                with open(self.liderdb_path) as f:
                    read_data = json.load(f)
                read_data.update(self.data)
                with open(self.liderdb_path, 'w') as f:
                    json.dump(read_data, f, ensure_ascii=False)
                print('Lider Ahenk json dosyası güncellendi')
                # self.logger.info("Lider Ahenk json dosyası güncellendi")
                self.msg_box.information("Veritabanı bilgileri güncellendi\n"
                                         "Veritabanı kurulumana başlanacak.")
            else:
                with open(self.liderdb_path, 'w') as f:
                    json.dump(self.data, f, ensure_ascii=False)
                    print("Lider Ahenk json dosyası oluşturuldu")
                # self.logger.info("Lider Ahenk json dosyası oluşturuldu")
                self.msg_box.information("Veritabanı bilgileri kaydedildi\n"
                                     "Veritabanı kurulumuna başlanacak.")

            if self.data['location'] == 'remote':
                self.im.ssh_connect(self.data)
                self.im.install_mariadb(self.data)
                self.im.ssh_disconnect()
            else:
                self.im.install_mariadb(self.data)

            self.status.install_status.setText("Veritabanı kurulumu tamamlandı")
            self.status.install_status.setStyleSheet("background-color: cyan")
            self.msg_box.information("Veritabanı kurulumu tamamlandı\n"
                                     "Kurulum loglarını \n"
                                     "Log ekranında bulabilirsiniz")
