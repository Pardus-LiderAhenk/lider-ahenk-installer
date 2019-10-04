#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Author: Tuncay ÇOLAK <tuncay.colak@tubitak.gov.tr>

import json
import os

from PyQt5.QtWidgets import (QGridLayout, QGroupBox, QLabel, QLineEdit, QPushButton, QVBoxLayout, QWidget, QTableWidget,
                             QTableWidgetItem, QComboBox, QCheckBox)

from install_manager import InstallManager
from ui.lider.lider_page import LiderPage
from ui.message_box.message_box import MessageBox
from api.util.util import Util

class SettingsPage(QWidget):
    def __init__(self, parent=None):

        super(SettingsPage, self).__init__(parent)
        self.server_list_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../dist/server_list.json')
        if not os.path.exists(os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../dist')):
            os.makedirs(os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../dist'))

        self.im = InstallManager()
        self.msg_box = MessageBox()
        self.lider_page = LiderPage()

        self.util = Util()
        self.repo_type = None

        #server selection parameters
        self.standartSelectionBox = QCheckBox("Standart")
        self.advancedSelectionBox = QCheckBox("Gelişmiş")
        self.standartSelectionBox.setChecked(True)

        ## server selection layout
        self.connectSelectionGroup = QGroupBox("Lider Ahenk Sunucu Platform Bilgileri")
        self.connectSelectionLayout = QGridLayout()
        self.connectSelectionLayout.addWidget(self.standartSelectionBox,0,0)
        self.connectSelectionLayout.addWidget(self.advancedSelectionBox,0,1)
        self.connectSelectionGroup.setLayout(self.connectSelectionLayout)

        self.standartSelectionBox.stateChanged.connect(self.standart_selection)
        self.advancedSelectionBox.stateChanged.connect(self.advanced_selection)

        ## server settings parameters
        self.serverSelectionCombo = QComboBox()
        # self.serverSelectionCombo.setDisabled(True)
        self.serverSelectionCombo.setVisible(False)
        self.serverSelectionLabel = QLabel("Bileşen Seç:")
        self.serverSelectionLabel.setVisible(False)
        self.serverSelectionCombo.addItem("Veritabanı")
        self.serverSelectionCombo.addItem("OpenLDAP")
        self.serverSelectionCombo.addItem("XMPP")
        self.serverSelectionCombo.addItem("Lider")

        self.serverIpLabel = QLabel("Sunucu Adresi:")
        self.server_ip = QLineEdit()
        self.server_ip.setPlaceholderText("192.168.*.*")
        self.usernameLabel = QLabel("Kullanıcı Adı:")
        self.username = QLineEdit()
        self.username.setPlaceholderText("lider")
        self.passwordLabel = QLabel("Kullanıcı Parolası:")
        self.password = QLineEdit()
        self.password.setPlaceholderText("****")
        self.password.setEchoMode(QLineEdit.Password)
        self.addButton = QPushButton("Ekle")
        self.checkControlButton = QPushButton("Bağlantıyı Kontrol Et")
        self.saveButton = QPushButton("Ayarları Kaydet")
        # disabled by default saveButton
        # self.saveButton.setDisabled(True)
        self.addButton.setVisible(False)

        ## Connect Layout
        self.connectGroup = QGroupBox("Lider Ahenk Sunucu Erişim Bilgileri")
        self.connectLayout = QGridLayout()
        self.connectLayout.addWidget(self.serverSelectionLabel, 0, 0)
        self.connectLayout.addWidget(self.serverSelectionCombo, 0, 1)
        self.connectLayout.addWidget(self.serverIpLabel, 2, 0)
        self.connectLayout.addWidget(self.server_ip, 2, 1)
        self.connectLayout.addWidget(self.usernameLabel, 3, 0)
        self.connectLayout.addWidget(self.username, 3, 1)
        self.connectLayout.addWidget(self.passwordLabel, 4, 0)
        self.connectLayout.addWidget(self.password, 4, 1)
        self.connectLayout.addWidget(self.addButton, 5,2)
        self.connectLayout.addWidget(self.checkControlButton, 5, 1)
        self.connectGroup.setLayout(self.connectLayout)

        ## server list table
        self.serverlistGroup = QGroupBox("Lider Ahenk Sunucu Listesi")
        self.serverlistLayout = QGridLayout()
        self.tableWidget = QTableWidget()
        # self.tableWidget.setMinimumHeight(250)
        self.serverlistGroup.setVisible(False)

        ## set read only table
        self.tableWidget.setEditTriggers(QTableWidget.NoEditTriggers)

        # set column count
        self.tableWidget.setColumnCount(5)
        headers = self.tableWidget.horizontalHeader()
        # headers.setSectionResizeMode(QHeaderView.ResizeToContents)
        headers.setStretchLastSection(True)
        self.tableWidget.setHorizontalHeaderLabels(["Bileşen Adı", "Sunucu Adresi", "Kullanıcı Adı", "Kullanıcı Parolası", "İşlem"])
        self.serverlistLayout.addWidget(self.tableWidget)
        self.serverlistGroup.setLayout(self.serverlistLayout)

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

        ## Connect Settings Layout
        self.connectSettingsGroup = QGroupBox("1-LİDER AHENK SUNUCU BAĞLANTI AYARLARI")
        self.connectSettingsLayout = QGridLayout()
        self.connectSettingsLayout.addWidget(self.connectSelectionGroup)
        self.connectSettingsLayout.addWidget(self.connectGroup)
        self.connectSettingsLayout.addWidget(self.serverlistGroup)
        self.connectSettingsGroup.setLayout(self.connectSettingsLayout)

        ## Repository Layout
        self.repoGroup = QGroupBox("2-LİDER AHENK PAKET DEPOSU AYARLARI")
        self.repoLayout = QGridLayout()
        self.repoLayout.addWidget(self.repoMainBox, 0, 0)
        self.repoLayout.addWidget(self.repoTestBox, 0, 1)
        self.repoLayout.addWidget(self.repoLabel, 1, 0)
        self.repoLayout.addWidget(self.repo_addr, 1, 1)
        self.repoLayout.addWidget(self.repoKeyLdabel, 2, 0)
        self.repoLayout.addWidget(self.repo_key, 2, 1)
        self.repoGroup.setLayout(self.repoLayout)

        mainLayout = QVBoxLayout()
        mainLayout.addWidget(self.connectSettingsGroup)
        mainLayout.addSpacing(10)
        mainLayout.addWidget(self.repoGroup)
        mainLayout.addSpacing(12)
        mainLayout.addWidget(self.saveButton)
        mainLayout.addStretch(1)
        self.setLayout(mainLayout)

        self.saveButton.clicked.connect(self.save_settings)
        self.addButton.clicked.connect(self.add_server)
        self.checkControlButton.clicked.connect(self.ssh_control)
        self.get_server_settings()

    def main_repo(self):

        if self.repoMainBox.isChecked() is True:
            self.repo_type = "main"
            self.repoTestBox.setChecked(False)

            if self.util.is_exist(self.server_list_path):
                with open(self.server_list_path) as f:
                    data = json.load(f)
                    self.repo_key.setText(data["repo_key"])
                    if data["repo_type"] == "main":
                        self.repoMainBox.setChecked(True)
                        self.repo_addr.setText(data["repo_addr"])
                    else:
                        self.repo_addr.setText("deb [arch=amd64] http://repo.liderahenk.org/liderahenk stable main")
            else:
                self.repo_addr.setText("deb [arch=amd64] http://repo.liderahenk.org/liderahenk stable main")

    def test_repo(self):

        if self.repoTestBox.isChecked() is True:
            self.repo_type = "test"
            self.repoMainBox.setChecked(False)

            if self.util.is_exist(self.server_list_path):
                with open(self.server_list_path) as f:
                    data = json.load(f)
                    self.repo_key.setText(data["repo_key"])
                    if data["repo_type"] == "test":
                        self.repoTestBox.setChecked(True)
                        self.repo_addr.setText(data["repo_addr"])
                    else:
                        self.repo_addr.setText("deb [arch=amd64] http://repo.liderahenk.org/liderahenk-test testing main")
            else:
                self.repo_addr.setText("deb [arch=amd64] http://repo.liderahenk.org/liderahenk-test testing main")

    def standart_selection(self):

        if self.standartSelectionBox.isChecked() is True:
            self.advancedSelectionBox.setChecked(False)
            # self.serverSelectionCombo.setDisabled(True)
            self.serverSelectionCombo.setVisible(False)
            self.serverSelectionLabel.setVisible(False)
            self.serverlistGroup.setVisible(False)
            self.addButton.setVisible(False)
            self.saveButton.setEnabled(True)

    def advanced_selection(self):

        if self.advancedSelectionBox.isChecked() is True:
            self.standartSelectionBox.setChecked(False)
            # self.serverSelectionCombo.setEnabled(True)
            self.serverSelectionCombo.setVisible(True)
            self.serverSelectionLabel.setVisible(True)
            self.serverlistGroup.setVisible(True)
            self.addButton.setVisible(True)

            if self.tableWidget.rowCount() == 4:
                self.saveButton.setEnabled(True)
            else:
                self.saveButton.setDisabled(True)

    def add_server(self):

        if self.advancedSelectionBox.isChecked() is True:
            server_name = self.serverSelectionCombo.currentText()
            server_index = self.serverSelectionCombo.currentIndex()
            if server_index != self.serverSelectionCombo.count() - 1:
                self.serverSelectionCombo.setCurrentIndex(server_index + 1)
            ip = self.server_ip.text()
            username = self.username.text()
            password = self.password.text()
            server_status = self.check_server(server_name)
            # location = self.serverCombo.currentText()
            if server_status is False:
                if ip is "" or username is "" or password is "":
                    self.msg_box.warning("Lütfen Sunucu adresini, kullanıcı adını ve kullanıcı parolası giriniz!")
                else:
                    rowPosition = self.tableWidget.rowCount()
                    self.tableWidget.insertRow(rowPosition)
                    numcols = self.tableWidget.columnCount()
                    numrows = self.tableWidget.rowCount()
                    self.tableWidget.setRowCount(numrows)
                    self.tableWidget.setAlternatingRowColors(True)
                    self.tableWidget.setColumnCount(numcols)
                    self.tableWidget.setItem(numrows - 1, 0, QTableWidgetItem(server_name))
                    self.tableWidget.setItem(numrows - 1, 1, QTableWidgetItem(ip))
                    self.tableWidget.setItem(numrows - 1, 2, QTableWidgetItem(username))
                    self.tableWidget.setItem(numrows - 1, 3, QTableWidgetItem(password))

                    self.delButton = QPushButton(self.tableWidget)
                    self.delButton.setText('Sil')
                    self.delButton.clicked.connect(self.del_server)
                    self.tableWidget.setCellWidget(numrows - 1, 4, self.delButton)
                    self.tableWidget.selectRow(numrows - 1)

                    if self.tableWidget.rowCount() == 4:
                        self.saveButton.setEnabled(True)
                    else:
                        self.saveButton.setDisabled(True)
            else:
                self.msg_box.warning("Kayıt zaten var")

    def check_server(self, server_name):

        row_count = self.tableWidget.rowCount()
        server_list = []
        if row_count != 0:
            for row in range(row_count):
                server_item = self.tableWidget.item(row, 0)
                server_name_1 = server_item.text()
                server_list.append(server_name_1)
            # check if server name exist in a list return True
            if server_name in server_list:
                return True
            else:
                return False
        else:
            return False

    def del_server(self):

        rows = sorted(set(index.row() for index in
        self.tableWidget.selectedIndexes()))
        for row in rows:
            self.tableWidget.selectRow(row)
            self.tableWidget.removeRow(self.tableWidget.currentRow())
            self.msg_box.information("Kayıt Silindi")
            self.tableWidget.selectRow(row - 1)

        if self.tableWidget.rowCount() != 4:
            self.saveButton.setDisabled(True)

    def save_settings(self):

        repo_key = self.repo_key.text()
        repo_addr = self.repo_addr.text()

        ## if selection advanced installation
        if self.advancedSelectionBox.isChecked() is True:
            if self.tableWidget.rowCount() == 4:
                self.server_list = {}
                self.repo_data = {
                    'repo_key': repo_key,
                    'repo_addr': repo_addr,
                    'repo_type': self.repo_type
                }
                ## get item from server list table
                row_count = self.tableWidget.rowCount()
                if row_count != 0:

                    for row in range(row_count):

                        server_name_item = self.tableWidget.item(row, 0)
                        server_name = server_name_item.text()

                        ip_item = self.tableWidget.item(row, 1)
                        ip = ip_item.text()

                        username_item = self.tableWidget.item(row, 2)
                        username = username_item.text()

                        password_item = self.tableWidget.item(row, 3)
                        password = password_item.text()

                        self.data = {
                            server_name: [
                                {
                                'location': "remote",
                                'ip': ip,
                                'username': username,
                                'password': password,
                                'server_name': server_name
                                }
                            ]
                        }
                        self.server_list.update(self.data)
                    self.server_list.update(self.repo_data)
                    self.server_list.update({'selection': "advanced"})

                    with open(self.server_list_path, 'w') as f:
                        json.dump(self.server_list, f, ensure_ascii=False)
                    self.msg_box.information("Ayarlar kaydedildi.")
            else:
                self.msg_box.information("Lütfen Lider Ahenk bileşenlerine ait bağlantı bilgilerini giriniz.")

        ## if selection standart installation
        if self.standartSelectionBox.isChecked() is True:
            ip = self.server_ip.text()
            username = self.username.text()
            password = self.password.text()

            self.data = {
                'location': "remote",
                'selection': "standart",
                'ip': ip,
                'username': username,
                'password': password,
                'server_name': "all",
                'repo_key': repo_key,
                'repo_addr': repo_addr,
                'repo_type': self.repo_type
            }

            if ip is "" or username is "" or password is "":
                self.msg_box.warning("Lütfen Sunucu adresini, kullanıcı adını ve kullanıcı parolası giriniz!")
            else:
                with open(self.server_list_path, 'w') as f:
                    json.dump(self.data, f, ensure_ascii=False)
                self.msg_box.information("Ayarlar kaydedildi ve tüm Lider Ahenk Sunucu\n"
                                         "bileşenşeri tek bir sunucuya kurulacaktır.")

    def check_control_button(self, idx):

        ## if select location is remote server
        if idx == 0:
            self.server_ip.setText("")
        else:
            self.server_ip.setText("127.0.0.1")

    def ssh_control(self):

        data = {
            'location': "remote",
            # Server Configuration
            'ip': self.server_ip.text(),
            'username': self.username.text(),
            'password': self.password.text(),
        }

        if data["ip"] == "" or data["username"] == "" or data["password"] == "":
            self.msg_box.warning("Lütfen sunucu adresini, kullanıcı adını ve parolasını giriniz!")

        else:
            ssh_status = self.im.ssh_connect(data)
            if ssh_status is True:
                self.msg_box.information("Bağlantı Başarılı. Kuruluma Devam Edebilirsiniz.")
            else:
                msg = "Bağlantı Sağlanamadı. Bağlantı Ayarlarını Kontrol Ederek Daha Sonra Tekrar Deneyiniz!\n"
                self.msg_box.information(msg)


    def get_server_settings(self):

        if self.util.is_exist(self.server_list_path):
            with open(self.server_list_path) as f:
                data = json.load(f)
                self.repo_key.setText(data["repo_key"])
                if data["repo_type"] == "main":
                    self.repoMainBox.setChecked(True)
                    self.repoTestBox.setChecked(False)
                    self.repo_addr.setText(data["repo_addr"])
                else:
                    self.repoTestBox.setChecked(True)
                    self.repoMainBox.setChecked(False)
                    self.repo_addr.setText(data["repo_addr"])

                if data["selection"] == "standart":
                    self.standartSelectionBox.setChecked(True)
                    self.server_ip.setText(data["ip"])
                    self.username.setText(data["username"])
                    self.password.setText(data["password"])
                else:
                    self.advancedSelectionBox.setChecked(True)

                    servers = "Veritabanı", "OpenLDAP", "XMPP", "Lider"
                    for i in servers:
                        rowPosition = self.tableWidget.rowCount()
                        self.tableWidget.insertRow(rowPosition)
                        numcols = self.tableWidget.columnCount()
                        numrows = self.tableWidget.rowCount()
                        self.tableWidget.setRowCount(numrows)
                        self.tableWidget.setAlternatingRowColors(True)
                        self.tableWidget.setColumnCount(numcols)
                        self.tableWidget.setItem(numrows - 1, 0, QTableWidgetItem(i))
                        self.tableWidget.setItem(numrows - 1, 1, QTableWidgetItem(data[i][0]["ip"]))
                        self.tableWidget.setItem(numrows - 1, 2, QTableWidgetItem(data[i][0]["username"]))
                        self.tableWidget.setItem(numrows - 1, 3, QTableWidgetItem(data[i][0]["password"]))

                        self.delButton = QPushButton(self.tableWidget)
                        self.delButton.setText('Sil')
                        self.delButton.clicked.connect(self.del_server)
                        self.tableWidget.setCellWidget(numrows - 1, 4, self.delButton)
                        self.tableWidget.selectRow(numrows - 1)

                        if self.tableWidget.rowCount() == 4:
                            self.saveButton.setEnabled(True)
                        else:
                            self.saveButton.setDisabled(True)