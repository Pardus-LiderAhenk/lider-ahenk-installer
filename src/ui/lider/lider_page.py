#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Author: Tuncay ÇOLAK <tuncay.colak@tubitak.gov.tr>

import os
import json
import subprocess
import time
import random
import string

from PyQt5.QtWidgets import (QGridLayout, QGroupBox, QLabel, QLineEdit, QPushButton, QWidget, QVBoxLayout)
from ui.ldap.ldap_page import OpenLdapPage
from ui.ejabberd.ejabberd_page import EjabberdPage
from ui.database.db_page import DatabasePage
from install_manager import InstallManager
from ui.log.status_page import StatusPage
from ui.message_box.message_box import MessageBox
from api.util.util import Util

class LiderPage(QWidget):
    def __init__(self, parent=None):
        super(LiderPage, self).__init__(parent)

        self.liderldap_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../dist/lider_ldap.json')
        self.liderejabberd_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../dist/lider_ejabberd.json')
        self.liderdb_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../dist/liderdb.json')
        self.lider_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../dist/lider.json')
        self.server_list_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../dist/server_list.json')
        self.log_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../dist/installer.log')
        if not os.path.exists(os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../dist')):
            os.makedirs(os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../dist'))

        self.ldap_layout = OpenLdapPage()
        self.ejabberd_layout = EjabberdPage()
        self.db_layout = DatabasePage()
        self.im = InstallManager()
        self.msg_box = MessageBox()
        self.status = StatusPage()
        self.lider_sunucu_pwd = None
        self.db_password = None
        self.util = Util()

        ## db parameters
        self.dbServerLabel = QLabel("Veritabanı Sunucu Adresi:")
        self.db_server_layout = QLineEdit()
        self.db_server_layout.setPlaceholderText("192.168.*.*")

        # OpenLDAP parameters
        self.ldapServerLabel = QLabel("LDAP Sunucu Adresi:")
        self.ldap_server = QLineEdit()
        self.ldap_server.setPlaceholderText("192.168.*.*")

        # Ejabberd parameters
        self.ejabberdServerLabel = QLabel("XMPP Sunucu Adresi:")
        self.ejabberd_server = QLineEdit()
        self.ejabberd_server.setPlaceholderText("192.168.*.*")

        self.fileServerLabel = QLabel("Dosya Sunucu Adresi:")
        self.file_server = QLineEdit()
        self.file_server.setPlaceholderText("192.168.*.*")
        # self.file_server.setDisabled(True)
        self.file_server.setVisible(False)
        self.fileServerLabel.setVisible(False)

        self.installButton = QPushButton("Kuruluma Başla")

        # if not os.path.exists(self.server_list_path):
        #     self.installButton.setDisabled(True)

        self.installButton.clicked.connect(self.lider_ahenk_install)

        self.liderLdapGroup = QGroupBox("Lider Ahenk Sunucu Konfigürasyon Bilgileri")
        self.liderXmppGroup = QGroupBox("XMPP Konfigürasyon Bilgileri")
        self.liderDbGroup = QGroupBox("Veritabanı Konfigürasyon Bilgileri")

        # Install Status Layout
        statusGroup = QGroupBox()
        self.status.statusLabel.setText("Lider Kurulum Durumu:")
        statusGroup.setLayout(self.status.statusLayout)

        # add server ip to database layout
        self.liderDbGroup.setLayout(self.db_layout.dbLayout)

        # add server ip to ldap layout
        self.liderLdapGroup.setLayout(self.ldap_layout.ldapLayout)

        # add server ip to ejabberd layout
        self.ejabberd_layout.ejabberdLayout.removeWidget(self.ejabberd_layout.ldapServerLabel)
        self.ejabberd_layout.ejabberdLayout.removeWidget(self.ejabberd_layout.ldap_server)
        # self.ejabberd_layout.ejabberdLayout.addWidget(self.ejabberdServerLabel, 8, 0)
        # self.ejabberd_layout.ejabberdLayout.addWidget(self.ejabberd_server, 8, 1)
        self.liderXmppGroup.setLayout(self.ejabberd_layout.ejabberdLayout)

        self.liderGroup = QGroupBox()
        # liderLayout = QVBoxLayout()
        liderLayout = QGridLayout()
        # liderLayout.addSpacing(12)
        liderLayout.addWidget(self.installButton,0,1)
        # liderLayout.addStretch(1)
        self.liderGroup.setLayout(liderLayout)

        mainLayout = QVBoxLayout()
        # mainLayout.addWidget(self.liderDbGroup)
        mainLayout.addWidget(self.liderLdapGroup)
        # mainLayout.addWidget(self.liderXmppGroup)
        mainLayout.addWidget(self.liderGroup)
        mainLayout.addWidget(statusGroup)
        mainLayout.addSpacing(12)
        mainLayout.addStretch(1)

        self.setLayout(mainLayout)

        if self.util.is_exist(self.liderldap_path):
            with open(self.liderldap_path) as f:
                data = json.load(f)
            self.ldap_layout.ldap_base_dn.setText(data["l_base_dn"])
            self.ldap_layout.ldap_admin_pwd.setText(data["l_admin_pwd"])
            self.ldap_layout.ladmin_user.setText(data["ladmin_user"])
            self.ldap_layout.ladmin_pwd.setText(data["l_admin_pwd"])

    def check_control_button(self, idx):
        ## if select location is remote server
        if idx == 0:
            # self.checkControlButton.setEnabled(True)
            # self.file_server.setDisabled(True)
            self.file_server.setVisible(False)
            self.fileServerLabel.setVisible(False)

        else:
            # self.file_server.setDisabled(False)
            self.file_server.setVisible(True)
            self.fileServerLabel.setVisible(True)

    def lider_ahenk_install(self):

        if self.ldap_layout.ldap_base_dn.text() == "" or self.ldap_layout.ldap_admin_pwd.text() == "" or self.ldap_layout.ladmin_user.text() == "" or self.ldap_layout.ladmin_pwd.text() == "":
            self.msg_box.information("Lütfen LDAP ve XMPP bilgilerini giriniz")
        else:
            self.status.install_status.setText("Lider Ahenk kurulumu devam ediyor")
            self.status.install_status.setStyleSheet("background-color: green")

            self.msg_box.information("Lider Ahenk sunucu kurulumana başlanacak.")

            subprocess.Popen(["xterm", "-e", "tail", "-f",
                              self.log_path])

            ## get connect and repo settings data
            with open(self.server_list_path) as f:
                server_data = json.load(f)

                self.database_install(server_data)
                time.sleep(5)
                self.ldap_install(server_data)
                time.sleep(5)
                self.ejabberd_install(server_data)
                time.sleep(5)
                self.lider_install(server_data)

    def database_install(self, server_data):

        if server_data["selection"] == "advanced":
            ip = server_data["Veritabanı"][0]["ip"]
            username = server_data["Veritabanı"][0]["username"]
            password = server_data["Veritabanı"][0]["password"]
            location = server_data["Veritabanı"][0]["location"]

        else:
            # selection is standart
            ip = server_data["ip"]
            username = server_data["username"]
            password = server_data["password"]
            location = server_data["location"]

        ## Random Password Generator for "databases user's password"
        chars = string.ascii_letters + string.digits
        rnd = random.SystemRandom()
        self.db_password = ''.join(rnd.choice(chars) for i in range(10))

        self.data = {
            'location': location,
            # Server Configuration
            'ip': ip,
            'username': username,
            'password': password,
            # Database Configuration
            'db_name': "liderdb",
            'db_username': "root",
            'db_password': self.db_password,
            # Repo Configuration
            'repo_addr': server_data["repo_addr"],
            'repo_key': server_data["repo_key"]
        }

        with open(self.liderdb_path, 'w') as f:
            json.dump(self.data, f, ensure_ascii=False)

        if self.data['location'] == 'remote':
            self.im.ssh_connect(self.data)
            self.im.install_mariadb(self.data)
            self.im.ssh_disconnect()
        else:
            self.im.install_mariadb(self.data)

    def ldap_install(self, server_data):

        if server_data["selection"] == "advanced":
            ip = server_data["OpenLDAP"][0]["ip"]
            username = server_data["OpenLDAP"][0]["username"]
            password = server_data["OpenLDAP"][0]["password"]
            location = server_data["OpenLDAP"][0]["location"]
            lider_server_addr = server_data["Lider"][0]["ip"]
        else:
            # selection is standart
            ip = server_data["ip"]
            username = server_data["username"]
            password = server_data["password"]
            location = server_data["location"]
            lider_server_addr = server_data["ip"]

        if self.ldap_layout.ldapStatusCombo.currentIndex() == 0:
            ldap_status = 'new'
        else:
            # if ldap_status is 'Güncelle'
            ldap_status = 'update'

        l_org_name = self.ldap_layout.ldap_base_dn.text().split('.')
        l_org_name = l_org_name[0]

        self.data = {

            'location': location,
            # Server Configuration
            'ip': ip,
            'username': username,
            'password': password,

            # OpenLDAP Configuration
            'l_base_dn': self.ldap_layout.ldap_base_dn.text(),
            'l_config_pwd': self.ldap_layout.ldap_admin_pwd.text(),
            'l_org_name': l_org_name,
            'l_config_admin_dn': "cn=admin,cn=config",
            'l_admin_cn': 'admin',
            'ladmin_user': self.ldap_layout.ladmin_user.text(),
            'l_admin_pwd': self.ldap_layout.ldap_admin_pwd.text(),
            'ladmin_pwd': self.ldap_layout.ldap_admin_pwd.text(),
            'ldap_status': ldap_status,
            'repo_addr': server_data["repo_addr"],
            'repo_key': server_data["repo_key"],
            'lider_server_addr': lider_server_addr,
            'simple_ldap_user': "test_ldap_user",
            'simple_ldap_user_pwd': "secret"

            # yeni ldap kur ya da varolan ldapı konfigüre et 'new' ya da 'update' parametreleri alıyor
        }

        with open(self.liderldap_path, 'w') as f:
            json.dump(self.data, f, ensure_ascii=False)

        if self.data['location'] == 'remote':
            self.im.ssh_connect(self.data)
            self.im.install_ldap(self.data)
            self.im.ssh_disconnect()
        else:
            self.im.install_ldap(self.data)

    def ejabberd_install(self, server_data):

        if server_data["selection"] == "advanced":
            ip = server_data["XMPP"][0]["ip"]
            username = server_data["XMPP"][0]["username"]
            password = server_data["XMPP"][0]["password"]
            location = server_data["XMPP"][0]["location"]
            self.ldap_server = server_data["OpenLDAP"][0]["ip"]
        else:
            # selection is standart
            ip = server_data["ip"]
            username = server_data["username"]
            password = server_data["password"]
            location = server_data["location"]
            self.ldap_server = server_data["ip"]

        ## Random Password Generator for "lider_sunucu"
        chars = string.ascii_letters + string.digits
        rnd = random.SystemRandom()
        self.lider_sunucu_pwd = ''.join(rnd.choice(chars) for i in range(10))

        self.data = {

            'location': location,
            # Server Configuration
            'ip': ip,
            'username': username,
            'password': password,
            # Ejabberd Configuration
            'e_service_name': "im.liderahenk.org",
            # 'e_service_name': self.e_service_name.text(),
            'e_username': 'admin',
            # 'e_user_pwd': self.ejabberd_layout.e_user_pwd.text(),
            'e_user_pwd': self.ldap_layout.ldap_admin_pwd.text(),
            'e_hosts': ip,
            'ldap_servers': self.ldap_server,
            'l_base_dn': self.ldap_layout.ldap_base_dn.text(),

            # Lider Configuration
            'lider_username': 'lider_sunucu',
            'lider_user_pwd': self.lider_sunucu_pwd,
            'l_admin_pwd': self.ldap_layout.ldap_admin_pwd.text(),
            'repo_key': server_data["repo_key"],
            'repo_addr': server_data["repo_addr"]
        }

        with open(self.liderejabberd_path, 'w') as f:
            json.dump(self.data, f, ensure_ascii=False)

        if self.data['location'] == 'remote':
            self.im.ssh_connect(self.data)
            self.im.install_ejabberd(self.data)
            self.im.ssh_disconnect()
        else:
            self.im.install_ejabberd(self.data)

    def lider_install(self, server_data):

        if server_data["selection"] == "advanced":
            ip = server_data["Lider"][0]["ip"]
            username = server_data["Lider"][0]["username"]
            password = server_data["Lider"][0]["password"]
            location = server_data["Lider"][0]["location"]
            self.ldap_server = server_data["OpenLDAP"][0]["ip"]
            self.db_server = server_data["Veritabanı"][0]["ip"]
            self.ejabberd_server = server_data["XMPP"][0]["ip"]
            if server_data["Veritabanı"][0]["ip"] == ip:
                self.db_server = "127.0.0.1"
            else:
                self.db_server = server_data["Veritabanı"][0]["ip"]

        else:
            # selection is standart
            ip = server_data["ip"]
            username = server_data["username"]
            password = server_data["password"]
            location = server_data["location"]
            self.ldap_server = server_data["ip"]
            self.db_server = server_data["ip"]
            self.ejabberd_server = server_data["ip"]
            self.db_server = "127.0.0.1"

        self.data = {
            'location': location,

            # Server Configuration
            'ip': ip,
            'username': username,
            'password': password,
            # Database Configuration
            'db_server': self.db_server,
            'db_name': "liderdb",
            'db_username': "root",
            'db_password': self.db_password,

            # Ejabberd Configuration
            'e_service_name': "im.liderahenk.org",
            'e_hosts': self.ejabberd_server,
            'lider_username': 'lider_sunucu',
            'lider_user_pwd': self.lider_sunucu_pwd,

            # OpenLDAP Configuration
            'l_base_dn': self.ldap_layout.ldap_base_dn.text(),
            'l_admin_cn': "admin",
            'l_admin_pwd': self.ldap_layout.ldap_admin_pwd.text(),
            'ldap_servers': self.ldap_server,

            # File Server Configuration
            'file_server': ip,
            'fs_username': username,
            'fs_username_pwd': password,
            'fs_plugin_path': '/home/{username}'.format(username=username),
            'fs_agreement_path': '/home/{username}'.format(username=username),
            'fs_agent_file_path': '/home/{username}'.format(username=username),

            # repository parameters
            'repo_key': server_data["repo_key"],
            'repo_addr': server_data["repo_addr"]
        }

        with open(self.lider_path, 'w') as f:
            json.dump(self.data, f, ensure_ascii=False)

        if self.data['location'] == 'remote':
            self.im.ssh_connect(self.data)
            self.im.install_lider(self.data)
            self.im.ssh_disconnect()
        else:
            self.im.install_lider(self.data)

        self.msg_box.information("Lider Ahenk kurulumu tamamlandı.\n"
                                 "Kurulum loglarını Log sayfasından inceleyebilirsiniz")
        self.status.install_status.setText("Lider Ahenk kurulumu tamamlandı")
        self.status.install_status.setStyleSheet("background-color: cyan")











