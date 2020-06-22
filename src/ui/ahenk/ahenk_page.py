#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Author: Tuncay ÇOLAK <tuncay.colak@tubitak.gov.tr>

import os
import subprocess
import time

from PyQt5 import QtGui
from PyQt5.QtWidgets import (QGridLayout, QGroupBox, QLabel, QLineEdit, QPushButton, QVBoxLayout, QWidget, QTableWidget,
                             QHeaderView, QTableWidgetItem, QCheckBox)
from install_manager import InstallManager
from ui.log.status_page import StatusPage
from ui.message_box.message_box import MessageBox

class AhenkPage(QWidget):
    def __init__(self, parent=None):
        super(AhenkPage, self).__init__(parent)
        self.ahenk_list_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../dist/ahenk_list.txt')
        self.log_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../dist/installer.log')
        if not os.path.exists(os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../dist')):
            os.makedirs(os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../dist'))

        self.status = StatusPage()
        self.im = InstallManager()
        self.msg_box = MessageBox()
        self.data = None

        ## client settings parameters
        self.serverIpLabel = QLabel("İstemci Adresi:")
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

        ## Connect Layout
        self.connectGroup = QGroupBox("Ahenk Kurulacak İstemci Erişim Bilgileri")
        self.connectLayout = QGridLayout()
        self.connectLayout.addWidget(self.serverIpLabel, 0, 0)
        self.connectLayout.addWidget(self.server_ip, 0, 1)
        self.connectLayout.addWidget(self.usernameLabel, 1, 0)
        self.connectLayout.addWidget(self.username, 1, 1)
        self.connectLayout.addWidget(self.passwordLabel, 2, 0)
        self.connectLayout.addWidget(self.password, 2, 1)
        self.connectLayout.addWidget(self.addButton, 0, 2)
        self.connectGroup.setLayout(self.connectLayout)

        ## repository layout
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

        ## ahenk parameters
        self.hostLabel = QLabel("XMPP Sunucu Adresi:")
        self.host = QLineEdit()
        self.host.setPlaceholderText("192.168.*.*")
        # self.serviceNameLabel = QLabel("XMPP Servis Adı:")
        # self.service_name = QLineEdit()
        # self.service_name.setPlaceholderText("im.liderahenk.org")
        self.startUpdateButton = QPushButton("Kuruluma Başla")

        ## ahenk Layout
        self.ahenkGroup = QGroupBox("Ahenk Konfigürasyon Bilgileri")
        self.ahenkLayout = QGridLayout()
        self.ahenkLayout.addWidget(self.hostLabel, 0, 0)
        self.ahenkLayout.addWidget(self.host, 0, 1)
        # self.ahenkLayout.addWidget(self.serviceNameLabel, 1, 0)
        # self.ahenkLayout.addWidget(self.service_name, 1, 1)
        self.ahenkGroup.setLayout(self.ahenkLayout)

        ## ahenk list table
        self.ahenklistGroup = QGroupBox("Ahenk Kurulacak İstemci Listesi")
        self.ahenklistLayout = QGridLayout()
        self.tableWidget = QTableWidget()
        # self.tableWidget.setMinimumHeight(250)

        ## set read only table
        self.tableWidget.setEditTriggers(QTableWidget.NoEditTriggers)

        # set column count
        self.tableWidget.setColumnCount(4)
        headers = self.tableWidget.horizontalHeader()
        headers.setSectionResizeMode(0, QHeaderView.Stretch)
        headers.setSectionResizeMode(1, QHeaderView.Stretch)
        headers.setSectionResizeMode(2, QHeaderView.Stretch)
        self.tableWidget.setHorizontalHeaderLabels(["İstemci Adresi", "Kullanıcı Adı", "Kullanıcı Parolası", "İşlem"])
        self.ahenklistLayout.addWidget(self.tableWidget)
        self.ahenklistGroup.setLayout(self.ahenklistLayout)

        # Install Status Layout
        statusGroup = QGroupBox()
        self.status.statusLabel.setText("Ahenk Kurulum Durumu:")
        statusGroup.setLayout(self.status.statusLayout)

        mainLayout = QVBoxLayout()
        mainLayout.addWidget(self.ahenkGroup)
        mainLayout.addWidget(self.repoGroup)
        mainLayout.addWidget(self.connectGroup)
        mainLayout.addWidget(self.ahenklistGroup)
        mainLayout.addSpacing(12)
        mainLayout.addWidget(self.startUpdateButton)
        mainLayout.addWidget(statusGroup)
        mainLayout.addStretch(1)
        self.setLayout(mainLayout)
        self.startUpdateButton.clicked.connect(self.install_ahenk)
        self.addButton.clicked.connect(self.add_ahenk)

    def main_repo(self):

        if self.repoMainBox.isChecked() is True:
            self.repo_addr.setText("deb [arch=amd64] http://repo.liderahenk.org/liderahenk stable main")
            self.repoTestBox.setChecked(False)

    def test_repo(self):
        if self.repoTestBox.isChecked() is True:
            self.repo_addr.setText("deb [arch=amd64] http://repo.liderahenk.org/liderahenk-test testing main")
            self.repoMainBox.setChecked(False)

    def add_ahenk(self):
        ip = self.server_ip.text()
        username = self.username.text()
        password = self.password.text()
        ip_status = self.check_ip(ip)
        if ip_status is False:
            if ip is "" or username is "" or password is "":
                self.msg_box.warning("Lütfen istemci adresini, kullanıcı adını ve kullanıcı parolası giriniz!")
            else:
                self.server_ip.setText("")
                self.username.setText("")
                self.password.setText("")
                rowPosition = self.tableWidget.rowCount()
                self.tableWidget.insertRow(rowPosition)
                numcols = self.tableWidget.columnCount()
                numrows = self.tableWidget.rowCount()
                self.tableWidget.setAlternatingRowColors(True)
                self.tableWidget.setRowCount(numrows)
                self.tableWidget.setColumnCount(numcols)
                self.tableWidget.setItem(numrows - 1, 0, QTableWidgetItem(ip))
                self.tableWidget.setItem(numrows - 1, 1, QTableWidgetItem(username))
                self.tableWidget.setItem(numrows - 1, 2, QTableWidgetItem("*" * len(password)))
                self.delButton = QPushButton(self.tableWidget)
                self.delButton.setText('Sil')
                self.delButton.clicked.connect(self.del_ahenk)
                self.tableWidget.setCellWidget(numrows - 1, 3, self.delButton)
                self.tableWidget.selectRow(numrows - 1)
        else:
            self.msg_box.warning("Kayıt zaten var")

    def check_ip(self, ip):
        row_count = self.tableWidget.rowCount()
        ip_list = []
        if row_count != 0:
            for row in range(row_count):
                ip_item = self.tableWidget.item(row, 0)
                ip_addr = ip_item.text()
                ip_list.append(ip_addr)

            # check if ip exist in a list return True
            if ip in ip_list:
                return True
            else:
                return False
        else:
            return False

    def del_ahenk(self):
        rows = sorted(set(index.row() for index in
        self.tableWidget.selectedIndexes()))
        for row in rows:
            self.tableWidget.selectRow(row)
            self.tableWidget.removeRow(self.tableWidget.currentRow())
            self.msg_box.information("Kayıt Silindi")

    def install_ahenk(self):
        ## get item from ahenk list table
        row_count = self.tableWidget.rowCount()
        if row_count != 0:
            install = self.msg_box.install_confirm(
                "Lider Ahenk sunucu kurulumuna başlanacak. Devam edtmek istiyor musunuz?")
            if install is True:
                self.status.install_status.setText("Ahenk kurulumu devam ediyor...")
                self.status.install_status.setStyleSheet("background-color: green")
                xterm = subprocess.Popen(["xterm", "-e", "tail", "-f",  self.log_path])
                for row in range(row_count):
                    ip_item = self.tableWidget.item(row, 0)
                    ip = ip_item.text()

                    username_item = self.tableWidget.item(row, 1)
                    username = username_item.text()

                    password_item = self.tableWidget.item(row, 2)
                    password = password_item.text()

                    repo_key = self.repo_key.text()
                    repo_addr = self.repo_addr.text()

                    self.data = {
                        # Client Configuration
                        'location': "remote",
                        'ip': ip,
                        'username': username,
                        'password': password,
                        # ahenk.conf Configuration
                        'host': self.host.text(),
                        'repo_key': repo_key,
                        'repo_addr': repo_addr,
                        'ldap_user': "test_ldap_user",
                        'ldap_user_pwd': "secret"
                    }

                    f = open(self.ahenk_list_file, "a+")
                    f.write(ip + "\n")

                    ssh_status = self.im.ssh_connect(self.data)
                    if ssh_status is True:
                        self.im.install_ahenk(self.data)
                        self.im.ssh_disconnect()
                        for col in range(3):
                            self.tableWidget.item(row, col).setBackground(QtGui.QColor("cyan"))
                    else:
                        msg = "Bağlantı Sağlanamadı. Bağlantı Ayarlarını Kontrol Ederek Daha Sonra Tekrar Deneyiniz!\n"
                        for col in range(3):
                            self.tableWidget.item(row, col).setBackground(QtGui.QColor("grey"))
                        #self.msg_box.information(msg)
                time.sleep(5)
                xterm.kill()
            else:
                self.msg_box.information("İstemciye Ahenk kurulmayacak")

            self.status.install_status.setText("Ahenk kurulumları tamamlandı")
            self.status.install_status.setStyleSheet("background-color: cyan")
            self.msg_box.information("Ahenk kurulumları tamamlandı\n"
                                     "Bağlantı sağlanamayan istemciler gri renktedirler\n"
                                     "Ayrıntı için\n"
                                     "Log ekranını inceleyiniz")

        else:
            self.msg_box.warning("Kayıt bulunamadı!\n"
                                 "Lütfen istemci bilgisi giriniz")
