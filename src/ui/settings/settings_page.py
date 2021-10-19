#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Author: Tuncay ÇOLAK <tuncay.colak@tubitak.gov.tr>

import json
import os

from PyQt5.QtWidgets import (QGridLayout, QGroupBox, QLabel, QLineEdit, QPushButton, QVBoxLayout, QWidget, QTableWidget,
                             QTableWidgetItem, QComboBox, QCheckBox)
from install_manager import InstallManager
from ui.message_box.message_box import MessageBox
from ui.lider.lider_page import LiderPage
from api.util.util import Util

class SettingsPage(QWidget):
    def __init__(self, parent=None):

        super(SettingsPage, self).__init__(parent)
        self.liderahenk_params_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../dist/liderahenk_params.json')
        if not os.path.exists(os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../dist')):
            os.makedirs(os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../dist'))

        self.im = InstallManager()
        self.msg_box = MessageBox()
        self.util = Util()
        self.repo_type = None
        self.lider_page = LiderPage()

        self.allComponentChekbox = QCheckBox("Tüm Bileşenler Tek Sunucuya Kurulsun")

        # database server
        self.databaseCheckBox = QCheckBox("Veritabanı")
        self.databaseCheckBox.setChecked(True)
        self.db_server_addr = QLineEdit()
        self.db_server_addr.setPlaceholderText("Veritabanı Adresi")
        self.db_server_username = QLineEdit()
        self.db_server_username.setPlaceholderText("Kullanıcı Adı")
        self.db_server_username_pwd = QLineEdit()
        self.db_server_username_pwd.setPlaceholderText("Kullanıcı Parolası")
        self.db_server_username_pwd.setEchoMode(QLineEdit.Password)
        self.db_checkControlButton = QPushButton("Bağlantıyı Kontrol Et")

        self.databaseGroup = QGroupBox()
        self.databaseLayout = QGridLayout()
        self.databaseLayout.addWidget(self.databaseCheckBox, 0, 0)
        self.databaseLayout.addWidget(self.db_server_addr, 1, 0)
        self.databaseLayout.addWidget(self.db_server_username, 2, 0)
        self.databaseLayout.addWidget(self.db_server_username_pwd, 3, 0)
        self.databaseLayout.addWidget(self.db_checkControlButton, 4, 0)
        self.databaseGroup.setLayout(self.databaseLayout)

        # ldap server
        self.ldapCheckBox = QCheckBox("OpenLDAP")
        self.ldapCheckBox.setChecked(True)
        self.ldap_server_addr = QLineEdit()
        self.ldap_server_addr.setPlaceholderText("OpenLDAP Adresi")
        self.ldap_server_username = QLineEdit()
        self.ldap_server_username.setPlaceholderText("Kullanıcı Adı")
        self.ldap_server_username_pwd = QLineEdit()
        self.ldap_server_username_pwd.setPlaceholderText("Kullanıcı Parolası")
        self.ldap_server_username_pwd.setEchoMode(QLineEdit.Password)
        self.ldap_checkControlButton = QPushButton("Bağlantıyı Kontrol Et")

        self.ldapGroup = QGroupBox()
        self.ldapLayout = QGridLayout()
        self.ldapLayout.addWidget(self.ldapCheckBox, 0, 0)
        self.ldapLayout.addWidget(self.ldap_server_addr, 1, 0)
        self.ldapLayout.addWidget(self.ldap_server_username, 2, 0)
        self.ldapLayout.addWidget(self.ldap_server_username_pwd, 3, 0)
        self.ldapGroup.setLayout(self.ldapLayout)

        # ejabberd server
        self.ejabberdCheckBox = QCheckBox("XMPP")
        self.ejabberdCheckBox.setChecked(True)
        self.ejabberd_server_addr = QLineEdit()
        self.ejabberd_server_addr.setPlaceholderText("XMPP Adresi")
        self.ejabberd_server_username = QLineEdit()
        self.ejabberd_server_username.setPlaceholderText("Kullanıcı Adı")
        self.ejabberd_server_username_pwd = QLineEdit()
        self.ejabberd_server_username_pwd.setPlaceholderText("Kullanıcı Parolası")
        self.ejabberd_server_username_pwd.setEchoMode(QLineEdit.Password)
        self.ejabberd_checkControlButton = QPushButton("Bağlantıyı Kontrol Et")

        self.ejabberdGroup = QGroupBox()
        self.ejabberdLayout = QGridLayout()
        self.ejabberdLayout.addWidget(self.ejabberdCheckBox, 0, 0)
        self.ejabberdLayout.addWidget(self.ejabberd_server_addr, 1, 0)
        self.ejabberdLayout.addWidget(self.ejabberd_server_username, 2, 0)
        self.ejabberdLayout.addWidget(self.ejabberd_server_username_pwd, 3, 0)
        self.ejabberdGroup.setLayout(self.ejabberdLayout)

        # lider server
        self.liderCheckBox = QCheckBox("Lider")
        self.liderCheckBox.setChecked(True)
        self.lider_server_addr = QLineEdit()
        self.lider_server_addr.setPlaceholderText("Lider Adresi")
        self.lider_server_username = QLineEdit()
        self.lider_server_username.setPlaceholderText("Kullanıcı Adı")
        self.lider_server_username_pwd = QLineEdit()
        self.lider_server_username_pwd.setPlaceholderText("Kullanıcı Parolası")
        self.lider_server_username_pwd.setEchoMode(QLineEdit.Password)
        self.lider_checkControlButton = QPushButton("Bağlantıyı Kontrol Et")

        self.liderGroup = QGroupBox()
        self.liderLayout = QGridLayout()
        self.liderLayout.addWidget(self.liderCheckBox, 0, 0)
        self.liderLayout.addWidget(self.lider_server_addr, 1, 0)
        self.liderLayout.addWidget(self.lider_server_username, 2, 0)
        self.liderLayout.addWidget(self.lider_server_username_pwd, 3, 0)
        self.liderGroup.setLayout(self.liderLayout)

        ## Connect Layout
        self.connectGroup = QGroupBox("Liderahenk Sunucu Erişim Bilgileri")
        self.connectLayout = QGridLayout()
        self.connectLayout.addWidget(self.allComponentChekbox, 0, 0)
        self.connectLayout.addWidget(self.databaseCheckBox, 1, 0)
        self.connectLayout.addWidget(self.db_server_addr, 2, 0)
        self.connectLayout.addWidget(self.db_server_username, 3, 0)
        self.connectLayout.addWidget(self.db_server_username_pwd, 4, 0)
        self.connectLayout.addWidget(self.db_checkControlButton, 5, 0)

        self.connectLayout.addWidget(self.ldapCheckBox, 1, 1)
        self.connectLayout.addWidget(self.ldap_server_addr, 2, 1)
        self.connectLayout.addWidget(self.ldap_server_username, 3, 1)
        self.connectLayout.addWidget(self.ldap_server_username_pwd, 4, 1)
        self.connectLayout.addWidget(self.ldap_checkControlButton, 5, 1)

        self.connectLayout.addWidget(self.ejabberdCheckBox, 1, 2)
        self.connectLayout.addWidget(self.ejabberd_server_addr, 2, 2)
        self.connectLayout.addWidget(self.ejabberd_server_username, 3, 2)
        self.connectLayout.addWidget(self.ejabberd_server_username_pwd, 4, 2)
        self.connectLayout.addWidget(self.ejabberd_checkControlButton, 5, 2)

        self.connectLayout.addWidget(self.liderCheckBox, 1, 3)
        self.connectLayout.addWidget(self.lider_server_addr, 2, 3)
        self.connectLayout.addWidget(self.lider_server_username, 3, 3)
        self.connectLayout.addWidget(self.lider_server_username_pwd, 4, 3)
        self.connectLayout.addWidget(self.lider_checkControlButton, 5, 3)
        self.connectGroup.setLayout(self.connectLayout)

        ## lider configure layout
        self.ldapAdminLabel = QLabel("LDAP Admin:")
        self.ldap_admin = QLineEdit()
        self.ldapAdminPwdLabel = QLabel("Sistem Admin Parolası")
        self.ldap_admin_pwd = QLineEdit()
        self.ldap_admin_pwd.setPlaceholderText("****")
        self.ldap_admin_pwd.setEchoMode(QLineEdit.Password)
        self.ldapBaseDnLabel = QLabel("LDAP Base DN:")
        self.ldap_base_dn = QLineEdit()
        self.ldap_base_dn.setPlaceholderText("liderahenk.org")
        self.ldapConfigPwdLabel = QLabel("LDAP Config Kullanıcı Parolası")
        self.l_config_pwd = QLineEdit()
        self.l_config_pwd.setPlaceholderText("****")
        self.l_config_pwd.setEchoMode(QLineEdit.Password)
        self.ladminLabel = QLabel("Lider Arayüz Kullanıcı Adı")
        self.ladmin_user = QLineEdit()
        self.ladmin_user.setPlaceholderText("lider_console")
        self.ladminPwdLabel = QLabel("Lider Arayüz Kullanıcı Parolası")
        self.ladmin_pwd = QLineEdit()
        self.ladmin_pwd.setPlaceholderText("****")
        self.ladmin_pwd.setEchoMode(QLineEdit.Password)
        self.ladminMailLabel = QLabel("Lider Arayüz Kullanıcı Mail Adresi")
        self.ladmin_mail_addr = QLineEdit()
        self.ladmin_mail_addr.setPlaceholderText("lider_console@liderahenk.org")

        # Active Directory params
        self.adSelectionBox = QCheckBox("Active Directory Bilgilerini Düzenle")
        self.ad_host_label = QLabel("AD Adresi:")
        self.ad_host = QLineEdit()
        self.ad_host.setPlaceholderText("192.168.*.*")
        self.ad_hostname_label = QLabel("AD Sunucu Adı:")
        self.ad_hostname = QLineEdit()
        self.ad_hostname.setPlaceholderText("server.ad.liderahenk.org")
        self.ad_domain_name_label = QLabel("AD Etki Alanı Adı:")
        self.ad_domain_name = QLineEdit()
        self.ad_domain_name.setPlaceholderText("ad.liderahenk.org")
        self.ad_username_label = QLabel("AD Kullanıcı Adı:")
        self.ad_username = QLineEdit()
        self.ad_username.setPlaceholderText("administrator")
        self.ad_user_pwd_label = QLabel("AD Kullanıcı Parolası:")
        self.ad_user_pwd = QLineEdit()
        self.ad_user_pwd.setPlaceholderText("****")
        self.ad_user_pwd.setEchoMode(QLineEdit.Password)
        self.ad_user_dn_label = QLabel("AD Kullanıcı DN Bilgisi:")
        self.ad_user_dn = QLineEdit()
        self.ad_user_dn.setPlaceholderText("cn=Administrator,cn=Users,dc=ad,dc=liderahenk,dc=org")
        self.ad_port_label = QLabel("AD Port:")
        self.ad_port = QLineEdit()
        self.ad_port.setPlaceholderText("389")

        self.install_button = QPushButton("Kuruluma Başla")

        self.configGroup = QGroupBox("Liderahenk Sunucu Konfigürasyonları")
        self.configLayout = QGridLayout()
        self.configLayout.addWidget(self.ldapBaseDnLabel, 0, 0)
        self.configLayout.addWidget(self.ldap_base_dn, 0, 1)
        self.configLayout.addWidget(self.ldapAdminPwdLabel, 1, 0)
        self.configLayout.addWidget(self.ldap_admin_pwd, 1, 1)
        self.configLayout.addWidget(self.ladminLabel, 2, 0)
        self.configLayout.addWidget(self.ladmin_user, 2, 1)
        self.configLayout.addWidget(self.ladminPwdLabel, 3, 0)
        self.configLayout.addWidget(self.ladmin_pwd, 3, 1)
        self.configLayout.addWidget(self.ladminMailLabel, 4, 0)
        self.configLayout.addWidget(self.ladmin_mail_addr, 4, 1)

        # self.configLayout.addWidget(self.adSelectionBox, 4, 0)
        # self.configLayout.addWidget(self.ad_host_label, 5, 0)
        # self.configLayout.addWidget(self.ad_host, 5, 1)
        # self.configLayout.addWidget(self.ad_domain_name_label, 6, 0)
        # self.configLayout.addWidget(self.ad_domain_name, 6, 1)
        # self.configLayout.addWidget(self.ad_hostname_label, 7, 0)
        # self.configLayout.addWidget(self.ad_hostname, 7, 1)
        # self.configLayout.addWidget(self.ad_username_label, 8, 0)
        # self.configLayout.addWidget(self.ad_username, 8, 1)
        # self.configLayout.addWidget(self.ad_user_pwd_label, 9, 0)
        # self.configLayout.addWidget(self.ad_user_pwd, 9, 1)
        # self.configLayout.addWidget(self.ad_user_dn_label, 10, 0)
        # self.configLayout.addWidget(self.ad_user_dn, 10, 1)
        # self.configLayout.addWidget(self.ad_port_label, 11, 0)
        # self.configLayout.addWidget(self.ad_port, 11, 1)

        self.configGroup.setLayout(self.configLayout)

        # self.adSelectionBox.stateChanged.connect(self.ad_change_state)
        # self.ad_conf_set_visible()

        ## server selection layout
        self.connectSelectionGroup = QGroupBox("Liderahenk Sunucu Platform Bilgileri")
        self.connectSelectionLayout = QGridLayout()
        self.connectSelectionGroup.setLayout(self.connectSelectionLayout)

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
        self.repoGroup = QGroupBox("Liderahenk Paket Deposu Ayarları")
        self.repoLayout = QGridLayout()
        self.repoLayout.addWidget(self.repoMainBox, 0, 0)
        self.repoLayout.addWidget(self.repoTestBox, 0, 1)
        self.repoLayout.addWidget(self.repoLabel, 1, 0)
        self.repoLayout.addWidget(self.repo_addr, 1, 1)
        self.repoLayout.addWidget(self.repoKeyLdabel, 2, 0)
        self.repoLayout.addWidget(self.repo_key, 2, 1)
        self.repoGroup.setLayout(self.repoLayout)

        self.statusLabel = QLabel("Lider kurulum durumu")
        self.install_status = QLineEdit()
        self.install_status.setReadOnly(True)
        self.install_status.setPlaceholderText("Liderahenk Kurulum")

        ## Install Status Layout
        self.statusGroup = QGroupBox()
        self.statusLayout = QGridLayout()
        self.statusLayout.addWidget(self.statusLabel, 0, 0)
        self.statusLayout.addWidget(self.install_status, 0, 1)
        self.statusGroup.setLayout(self.statusLayout)

        self.mainLayout = QVBoxLayout()
        self.mainLayout.addWidget(self.connectGroup)
        self.mainLayout.addSpacing(12)
        self.mainLayout.addWidget(self.repoGroup)
        self.mainLayout.addSpacing(10)
        self.mainLayout.addWidget(self.configGroup)
        self.mainLayout.addWidget(self.install_button)
        self.mainLayout.addWidget(self.statusGroup)
        self.mainLayout.addStretch(1)
        self.setLayout(self.mainLayout)

        self.db_checkControlButton.clicked.connect(lambda: self.ssh_control("db"))
        self.ldap_checkControlButton.clicked.connect(lambda: self.ssh_control("ldap"))
        self.ejabberd_checkControlButton.clicked.connect(lambda: self.ssh_control("ejabberd"))
        self.lider_checkControlButton.clicked.connect(lambda: self.ssh_control("lider"))

        self.databaseCheckBox.stateChanged.connect(self.change_database_checkbox)
        self.ldapCheckBox.stateChanged.connect(self.change_ldap_checkbox)
        self.ejabberdCheckBox.stateChanged.connect(self.change_ejabberd_checkbox)
        self.liderCheckBox.stateChanged.connect(self.change_lider_checkbox)
        self.allComponentChekbox.stateChanged.connect(self.all_components_install)

        self.install_button.clicked.connect(self.get_params)
        self.allComponentChekbox.setChecked(True)
        self.get_server_settings()

    def change_database_checkbox(self):
        if self.databaseCheckBox.isChecked():
            self.db_server_username.setDisabled(False)
            self.db_server_username_pwd.setDisabled(False)
            self.db_checkControlButton.setDisabled(False)
        else:
            self.db_server_username.setDisabled(True)
            self.db_server_username_pwd.setDisabled(True)
            self.db_checkControlButton.setDisabled(True)

    def change_ldap_checkbox(self):
        if self.ldapCheckBox.isChecked():
            self.ldap_server_username.setDisabled(False)
            self.ldap_server_username_pwd.setDisabled(False)
            self.ldap_checkControlButton.setDisabled(False)
        else:
            self.ldap_server_username.setDisabled(True)
            self.ldap_server_username_pwd.setDisabled(True)
            self.ldap_checkControlButton.setDisabled(True)

    def change_ejabberd_checkbox(self):
        if self.ejabberdCheckBox.isChecked():
            self.ejabberd_server_username.setDisabled(False)
            self.ejabberd_server_username_pwd.setDisabled(False)
            self.ejabberd_checkControlButton.setDisabled(False)
        else:
            self.ejabberd_server_username.setDisabled(True)
            self.ejabberd_server_username_pwd.setDisabled(True)
            self.ejabberd_checkControlButton.setDisabled(True)

    def change_lider_checkbox(self):
        if self.liderCheckBox.isChecked():
            self.lider_server_username.setDisabled(False)
            self.lider_server_username_pwd.setDisabled(False)
            self.lider_checkControlButton.setDisabled(False)
        else:
            self.lider_server_username.setDisabled(True)
            self.lider_server_username_pwd.setDisabled(True)
            self.lider_checkControlButton.setDisabled(True)

    def all_components_install(self):
        if self.allComponentChekbox.isChecked():
            self.databaseCheckBox.setChecked(True)
            self.ldapCheckBox.setChecked(True)
            self.ejabberdCheckBox.setChecked(True)
            self.liderCheckBox.setChecked(True)
            self.databaseCheckBox.setDisabled(True)

            self.ejabberdCheckBox.setDisabled(True)
            self.ejabberd_server_addr.setDisabled(True)
            self.ejabberd_server_username.setDisabled(True)
            self.ejabberd_server_username_pwd.setDisabled(True)
            self.ejabberd_checkControlButton.setDisabled(True)

            self.liderCheckBox.setDisabled(True)
            self.lider_server_addr.setDisabled(True)
            self.lider_server_username.setDisabled(True)
            self.lider_server_username_pwd.setDisabled(True)
            self.lider_checkControlButton.setDisabled(True)

            self.ldapCheckBox.setDisabled(True)
            self.ldap_server_addr.setDisabled(True)
            self.ldap_server_username.setDisabled(True)
            self.ldap_server_username_pwd.setDisabled(True)
            self.ldap_checkControlButton.setDisabled(True)
        else:
            self.databaseCheckBox.setDisabled(False)
            self.ejabberdCheckBox.setDisabled(False)
            self.ejabberd_server_addr.setDisabled(False)
            self.ejabberd_server_username.setDisabled(False)
            self.ejabberd_server_username_pwd.setDisabled(False)
            self.ejabberd_checkControlButton.setDisabled(False)

            self.liderCheckBox.setDisabled(False)
            self.lider_server_addr.setDisabled(False)
            self.lider_server_username.setDisabled(False)
            self.lider_server_username_pwd.setDisabled(False)
            self.lider_checkControlButton.setDisabled(False)

            self.ldapCheckBox.setDisabled(False)
            self.ldap_server_addr.setDisabled(False)
            self.ldap_server_username.setDisabled(False)
            self.ldap_server_username_pwd.setDisabled(False)
            self.ldap_checkControlButton.setDisabled(False)

    def ad_change_state(self):
        if self.adSelectionBox.isChecked() is True:
            self.ad_host_label.setVisible(True)
            self.ad_host.setVisible(True)
            self.ad_hostname_label.setVisible(True)
            self.ad_hostname.setVisible(True)
            self.ad_domain_name_label.setVisible(True)
            self.ad_domain_name.setVisible(True)
            self.ad_username_label.setVisible(True)
            self.ad_username.setVisible(True)
            self.ad_user_pwd_label.setVisible(True)
            self.ad_user_pwd.setVisible(True)
            self.ad_port_label.setVisible(True)
            self.ad_port.setVisible(True)
            self.ad_user_dn.setVisible(True)
            self.ad_user_dn_label.setVisible(True)
        else:
            self.ad_conf_set_visible()

    def ad_conf_set_visible(self):
        self.ad_host_label.setVisible(False)
        self.ad_host.setVisible(False)
        self.ad_hostname_label.setVisible(False)
        self.ad_hostname.setVisible(False)
        self.ad_domain_name_label.setVisible(False)
        self.ad_domain_name.setVisible(False)
        self.ad_username_label.setVisible(False)
        self.ad_username.setVisible(False)
        self.ad_user_pwd_label.setVisible(False)
        self.ad_user_pwd.setVisible(False)
        self.ad_port_label.setVisible(False)
        self.ad_port.setVisible(False)
        self.ad_user_dn.setVisible(False)
        self.ad_user_dn_label.setVisible(False)

    def main_repo(self):
        if self.repoMainBox.isChecked() is True:
            self.repo_type = "main"
            self.repoTestBox.setChecked(False)
            if self.util.is_exist(self.liderahenk_params_path):
                with open(self.liderahenk_params_path) as f:
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
            if self.util.is_exist(self.liderahenk_params_path):
                with open(self.liderahenk_params_path) as f:
                    data = json.load(f)
                    self.repo_key.setText(data["repo_key"])
                    if data["repo_type"] == "test":
                        self.repoTestBox.setChecked(True)
                        self.repo_addr.setText(data["repo_addr"])
                    else:
                        self.repo_addr.setText("deb [arch=amd64] http://repo.liderahenk.org/liderahenk-test testing main")
            else:
                self.repo_addr.setText("deb [arch=amd64] http://repo.liderahenk.org/liderahenk-test testing main")

    def get_params(self):
        lider_install = False
        if self.liderCheckBox.isChecked():
            lider_install = True

        ldap_install = False
        if self.ldapCheckBox.isChecked():
            ldap_install = True

        db_install = False
        if self.databaseCheckBox.isChecked():
            db_install = True

        ejabberd_install = False
        if self.ejabberdCheckBox.isChecked():
            ejabberd_install = True

        repo_key = self.repo_key.text()
        repo_addr = self.repo_addr.text()
        l_org_name = self.ldap_base_dn.text().split('.')
        l_org_name = l_org_name[0]

        all_components = False
        if self.allComponentChekbox.isChecked():
            all_components = True
            self.ldap_server_addr.setText(self.db_server_addr.text())
            self.ldap_server_username.setText(self.db_server_username.text())
            self.ldap_server_username_pwd.setText(self.db_server_username_pwd.text())
            self.ejabberd_server_addr.setText(self.db_server_addr.text())
            self.ejabberd_server_username.setText(self.db_server_username.text())
            self.ejabberd_server_username_pwd.setText(self.db_server_username_pwd.text())
            self.lider_server_addr.setText(self.db_server_addr.text())
            self.lider_server_username.setText(self.db_server_username.text())
            self.lider_server_username_pwd.setText(self.db_server_username_pwd.text())

        params = {
            'all_components': all_components,
            # Database Configuration
            'db_install': db_install,
            'db_server_addr': self.db_server_addr.text(),
            'db_server_username': self.db_server_username.text(),
            'db_server_username_pwd': self.db_server_username_pwd.text(),
            'db_name': "lidermysdb",
            'db_username': "root",
            'db_password': self.ldap_admin_pwd.text(),

            # Ejabberd Configuration
            'ejabberd_install': ejabberd_install,
            'ejabberd_server_addr': self.ejabberd_server_addr.text(),
            'ejabberd_server_username': self.ejabberd_server_username.text(),
            'ejabberd_server_username_pwd': self.ejabberd_server_username_pwd.text(),
            'e_service_name': "im.liderahenk.org",
            'e_hosts': self.ejabberd_server_addr.text(),
            'lider_username': 'lider_sunucu',
            'lider_user_pwd': self.ldap_admin_pwd.text(),
            'e_username': 'admin',
            'e_user_pwd': self.ldap_admin_pwd.text(),

            # OpenLDAP Configuration
            'ldap_install': ldap_install,
            'ldap_server_addr': self.ldap_server_addr.text(),
            'ldap_server_username': self.ldap_server_username.text(),
            'ldap_server_username_pwd': self.ldap_server_username_pwd.text(),
            'l_base_dn': self.ldap_base_dn.text(),
            'l_admin_cn': "admin",
            'l_admin_pwd': self.ldap_admin_pwd.text(),
            'ldap_servers': self.ldap_server_addr.text(),
            'l_config_pwd': self.ldap_admin_pwd.text(),
            'l_org_name': l_org_name,
            'l_config_admin_dn': "cn=admin,cn=config",
            'ladmin_user': self.ladmin_user.text(),
            'ladmin_pwd': self.ladmin_pwd.text(),
            'ladmin_mail_addr': self.ladmin_mail_addr.text(),
            'ldap_status': 'new',

            # AD Configuration
            'ad_host': self.ad_host.text(),
            'ad_hostname': self.ad_hostname.text(),
            'ad_domain_name': self.ad_domain_name.text(),
            'ad_username': self.ad_username.text(),
            'ad_user_pwd': self.ad_user_pwd.text(),
            'ad_port': self.ad_port.text(),
            'ad_user_dn': self.ad_user_dn.text(),

            # File Server Configuration
            'lider_install': lider_install,
            'lider_server_addr': self.lider_server_addr.text(),
            'lider_server_username': self.lider_server_username.text(),
            'lider_server_username_pwd': self.lider_server_username_pwd.text(),

            'file_server': self.lider_server_addr.text(),
            'fs_username': self.lider_server_username.text(),
            'fs_username_pwd': self.lider_server_username_pwd.text(),
            'fs_plugin_path': '/home/{username}'.format(username=self.lider_server_username.text()),
            'fs_agreement_path': '/home/{username}'.format(username=self.lider_server_username.text()),
            'fs_agent_file_path': '/home/{username}'.format(username=self.lider_server_username.text()),

            # repository parameters
            'repo_type': self.repo_type,
            'repo_key': repo_key,
            'repo_addr': repo_addr,
        }

        if self.databaseCheckBox.isChecked() or self.ldapCheckBox.isChecked() or self.ejabberdCheckBox.isChecked() or self.liderCheckBox.isChecked():
            if self.allComponentChekbox.isChecked() is not True:
                if self.databaseCheckBox.isChecked():
                    if self.db_server_addr.text() == "" or self.db_server_username.text() == "" or self.db_server_username_pwd.text() == "":
                        self.msg_box.information("Veritabanı sunucu erişim bilgilerini eksiksiz giriniz.")
                        return
                    else:
                        if self.ldap_server_addr.text() == "" or self.ejabberd_server_addr.text() == "" or self.lider_server_addr.text() == "":
                            self.msg_box.information("Veritabanı konfigürasyonu için OpenLDAP, Ejabberd ve Lider sunucu adresleri girilmelidir.")
                            return

                if self.ldapCheckBox.isChecked():
                    if self.ldap_server_addr.text() == "" or self.ldap_server_username.text() == "" or self.ldap_server_username_pwd.text() == "":
                        self.msg_box.information("OpenLDAP sunucu erişim bilgilerini eksiksiz giriniz.")
                        return

                if self.ejabberdCheckBox.isChecked():
                    if self.ejabberd_server_addr.text() == "" or self.ejabberd_server_username.text() == "" or self.ejabberd_server_username_pwd.text() == "":
                        self.msg_box.information("Ejabberd sunucu erişim bilgilerini eksiksiz giriniz.")
                        return
                    else:
                        if self.ldap_server_addr.text() == "":
                            self.msg_box.information("Ejabberd konfigürasyonu için OpenLDAP sunucu adresi girilmelidir.")
                            return

                if self.liderCheckBox.isChecked():
                    if self.lider_server_addr.text() == "" or self.lider_server_username.text() == "" or self.lider_server_username_pwd.text() == "":
                        self.msg_box.information("Lider sunucu erişim bilgilerini eksiksiz giriniz.")
                        return
                    else:
                        if self.db_server_addr.text() == "":
                            self.msg_box.information("Lider konfigürasyonu için Veritabanı sunucu adresi girilmelidir.")
                            return
            else:
                if self.db_server_addr.text() == "" or self.db_server_username.text() == "" or self.db_server_username_pwd.text() == "":
                    self.msg_box.information("Lütfen sunucu erişim bilgilerini eksiksiz giriniz")
                    return

            if self.ldap_base_dn.text() == "" or self.ldap_admin_pwd.text() == "" or self.ladmin_user.text() == "" or self.ladmin_pwd.text() == "" :
                self.msg_box.information("Liderahenk konfigürasyonu için tüm alanları doldurunuz.")
            else:
                install = self.msg_box.install_confirm("Liderahenk sunucu kurulumuna başlanacak. Devam etmek istiyor musunuz?")
                if install is True:
                    with open(self.liderahenk_params_path, 'w') as f:
                        json.dump(params, f, ensure_ascii=False)

                    self.install_status.setText("Liderahenk kurulumu devam ediyor")
                    self.install_status.setStyleSheet("background-color: green")
                    self.lider_page.lider_ahenk_install(params)
                    self.msg_box.information("Liderahenk kurulumu tamamlandı.")
                    self.install_status.setText("Liderahenk kurulumu tamamlandı")
                    self.install_status.setStyleSheet("background-color: cyan")
                else:
                    self.msg_box.information("Liderahenk sunucusu kurulmayacak")
        else:
            self.msg_box.information("Lütfen kuruluma başlamak için en bir tane bileşen seçiniz.")

    def ssh_control(self, server):
        ip = None
        username = None
        password = None

        if server == "db":
            ip = self.db_server_addr.text()
            username = self.db_server_username.text()
            password = self.db_server_username_pwd.text()

        if server == "ldap":
            ip = self.ldap_server_addr.text()
            username = self.ldap_server_username.text()
            password = self.ldap_server_username_pwd.text()

        if server == "ejabberd":
            ip = self.ejabberd_server_addr.text()
            username = self.ejabberd_server_username.text()
            password = self.ejabberd_server_username_pwd.text()

        if server == "lider":
            ip = self.lider_server_addr.text()
            username = self.lider_server_username.text()
            password = self.lider_server_username_pwd.text()

        data = {
            'location': "remote",
            # Server Configuration
            'ip': ip,
            'username': username,
            'password': password,
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
        if self.util.is_exist(self.liderahenk_params_path):
            with open(self.liderahenk_params_path) as f:
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

                if data["all_components"] is True:
                    self.allComponentChekbox.setChecked(True)
                else:
                    self.allComponentChekbox.setChecked(False)

                if data["lider_install"] is True:
                    self.liderCheckBox.setChecked(True)
                else:
                    self.liderCheckBox.setChecked(False)

                if data["ldap_install"] is True:
                    self.ldapCheckBox.setChecked(True)
                else:
                    self.ldapCheckBox.setChecked(False)

                if data["ejabberd_install"] is True:
                    self.ejabberdCheckBox.setChecked(True)
                else:
                    self.ejabberdCheckBox.setChecked(False)

                if data["db_install"] is True:
                    self.databaseCheckBox.setChecked(True)
                else:
                    self.databaseCheckBox.setChecked(False)

                self.db_server_addr.setText(data["db_server_addr"])
                self.db_server_username.setText(data["db_server_username"])
                self.db_server_username_pwd.setText(data["db_server_username_pwd"])

                self.ldap_server_addr.setText(data["ldap_server_addr"])
                self.ldap_server_username.setText(data["ldap_server_username"])
                self.ldap_server_username_pwd.setText(data["ldap_server_username_pwd"])

                self.ejabberd_server_addr.setText(data["ejabberd_server_addr"])
                self.ejabberd_server_username.setText(data["ejabberd_server_username"])
                self.ejabberd_server_username_pwd.setText(data["ejabberd_server_username_pwd"])

                self.lider_server_addr.setText(data["lider_server_addr"])
                self.lider_server_username.setText(data["lider_server_username"])
                self.lider_server_username_pwd.setText(data["lider_server_username_pwd"])

                self.ldap_base_dn.setText(data["l_base_dn"])
                self.ldap_admin_pwd.setText(data["l_admin_pwd"])
                self.ladmin_user.setText(data["ladmin_user"])
                self.ladmin_pwd.setText(data["l_admin_pwd"])
                self.ladmin_mail_addr.setText(data["ladmin_mail_addr"])
                self.ad_host.setText(data["ad_host"])
                self.ad_hostname.setText(data["ad_hostname"])
                self.ad_domain_name.setText(data["ad_domain_name"])
                self.ad_username.setText(data["ad_username"])
                self.ad_user_pwd.setText(data["ad_user_pwd"])
                self.ad_port.setText(data["ad_port"])
                self.ad_user_dn.setText(data["ad_user_dn"])
