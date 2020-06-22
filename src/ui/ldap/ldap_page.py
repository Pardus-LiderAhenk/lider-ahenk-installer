#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Author: Tuncay ÇOLAK <tuncay.colak@tubitak.gov.tr>

import os
import json
import subprocess

from PyQt5.QtWidgets import (QComboBox, QGridLayout, QGroupBox, QLabel, QLineEdit, QPushButton, QVBoxLayout, QWidget, QCheckBox)
from install_manager import InstallManager
from ui.message_box.message_box import MessageBox
from ui.log.status_page import StatusPage

class OpenLdapPage(QWidget):

    def __init__(self, parent=None):
        super(OpenLdapPage, self).__init__(parent)

        self.liderldap_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../dist/lider_ldap.json')
        self.log_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../dist/installer.log')
        self.server_list_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../dist/server_list.json')
        if not os.path.exists(os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../dist')):
            os.makedirs(os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../dist'))

        self.im = InstallManager()
        self.msg_box = MessageBox()
        self.status = StatusPage()
        self.data = None

        #OpenLDAP parameters
        self.ldapStatusLabel = QLabel("LDAP İçin İşlem Seçiniz:")
        self.ldapStatusCombo = QComboBox()
        self.ldapStatusCombo.addItem("OpenLDAP Kur")
        self.ldapStatusCombo.addItem("OpenLDAP Güncelle")
        self.ldapAdminLabel = QLabel("LDAP Admin:")
        self.ldap_admin = QLineEdit()
        self.ldapAdminPwdLabel = QLabel("Sistem Admin Parolası:")
        self.ldap_admin_pwd = QLineEdit()
        self.ldap_admin_pwd.setPlaceholderText("****")
        self.ldap_admin_pwd.setEchoMode(QLineEdit.Password)
        self.ldapBaseDnLabel = QLabel("LDAP Base DN:")
        self.ldap_base_dn = QLineEdit()
        self.ldap_base_dn.setPlaceholderText("liderahenk.org")
        self.ldapConfigPwdLabel = QLabel("LDAP Config Kullanıcı Parolası:")
        self.l_config_pwd = QLineEdit()
        self.l_config_pwd.setPlaceholderText("****")
        self.l_config_pwd.setEchoMode(QLineEdit.Password)
        self.ladminLabel = QLabel("Lider Arayüz Kullanıcı Adı:")
        self.ladmin_user = QLineEdit()
        self.ladmin_user.setPlaceholderText("lider_console")
        self.ladminPwdLabel = QLabel("Lider Arayüz Kullanıcı Parolası:")
        self.ladmin_pwd = QLineEdit()
        self.ladmin_pwd.setPlaceholderText("****")
        self.ladmin_pwd.setEchoMode(QLineEdit.Password)
        self.startUpdateButton = QPushButton("Kuruluma Başla")
        # Active Directory Parameters
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
        self.ad_port_label = QLabel("AD Port:")
        self.ad_port = QLineEdit()
        self.ad_port.setPlaceholderText("389")

        ## LDAP configuration Layout
        ldapGroup = QGroupBox("OpenLDAP Konfigürasyon Bilgileri")
        self.ldapLayout = QGridLayout()

        # Install Status Layout
        statusGroup = QGroupBox()
        self.status.statusLabel.setText("OpenLDAP Kurulum Durumu:")
        statusGroup.setLayout(self.status.statusLayout)

        # self.ldapLayout.addWidget(self.ldapStatusLabel, 0, 0)
        # self.ldapLayout.addWidget(self.ldapStatusCombo, 0, 1)
        self.ldapLayout.addWidget(self.ldapBaseDnLabel, 1, 0)
        self.ldapLayout.addWidget(self.ldap_base_dn, 1, 1)
        #self.ldapLayout.addWidget(self.ldapAdminLabel, 2, 0)
        #self.ldapLayout.addWidget(self.ldap_admin, 2, 1)
        self.ldapLayout.addWidget(self.ldapAdminPwdLabel, 3, 0)
        self.ldapLayout.addWidget(self.ldap_admin_pwd, 3, 1)
        #self.ldapLayout.addWidget(self.ldapConfigPwdLabel, 4, 0)
        #self.ldapLayout.addWidget(self.l_config_pwd, 4, 1)
        self.ldapLayout.addWidget(self.ladminLabel, 5, 0)
        self.ldapLayout.addWidget(self.ladmin_user, 5, 1)
        self.ldapLayout.addWidget(self.ladminPwdLabel, 6, 0)
        self.ldapLayout.addWidget(self.ladmin_pwd, 6, 1)
        self.ldapLayout.addWidget(self.adSelectionBox, 7, 0)

        self.ldapLayout.addWidget(self.ad_host_label, 8, 0)
        self.ldapLayout.addWidget(self.ad_host, 8, 1)
        self.ldapLayout.addWidget(self.ad_hostname_label, 9, 0)
        self.ldapLayout.addWidget(self.ad_hostname, 9, 1)
        self.ldapLayout.addWidget(self.ad_domain_name_label, 10, 0)
        self.ldapLayout.addWidget(self.ad_domain_name, 10, 1)
        self.ldapLayout.addWidget(self.ad_username_label, 11, 0)
        self.ldapLayout.addWidget(self.ad_username, 11, 1)
        self.ldapLayout.addWidget(self.ad_user_pwd_label, 12, 0)
        self.ldapLayout.addWidget(self.ad_user_pwd, 12, 1)
        self.ldapLayout.addWidget(self.ad_port_label, 13, 0)
        self.ldapLayout.addWidget(self.ad_port, 13, 1)

        ldapGroup.setLayout(self.ldapLayout)
        mainLayout = QVBoxLayout()
        mainLayout.addWidget(ldapGroup)
        # mainLayout.addWidget(packageGroup)
        mainLayout.addSpacing(12)
        mainLayout.addWidget(self.startUpdateButton)
        mainLayout.addWidget(statusGroup)
        mainLayout.addStretch(1)

        self.setLayout(mainLayout)
        self.startUpdateButton.clicked.connect(self.save_ldap_data)
        self.adSelectionBox.stateChanged.connect(self.ad_change_state)
        self.ad_conf_set_visible()

    def save_ldap_data(self):
        with open(self.server_list_path) as f:
            server_data = json.load(f)
            if server_data["selection"] == "multi":
                ip = server_data["OpenLDAP"][0]["ip"]
                username = server_data["OpenLDAP"][0]["username"]
                password = server_data["OpenLDAP"][0]["password"]
                location = server_data["OpenLDAP"][0]["location"]
            else:
                ip = server_data["ip"]
                username = server_data["username"]
                password = server_data["password"]
                location = server_data["location"]

        if self.ldapStatusCombo.currentIndex() == 0:
            ldap_status = 'new'
        else:
            # if ldap_status is 'Güncelle'
            ldap_status = 'update'

        l_org_name = self.ldap_base_dn.text().split('.')
        l_org_name = l_org_name[0]

        self.data = {
            'location': location,
            # Server Configuration
            'ip': ip,
            'username': username,
            'password': password,

            # OpenLDAP Configuration
            'l_base_dn': self.ldap_base_dn.text(),
            'l_config_pwd': self.l_config_pwd.text(),
            'l_org_name': l_org_name,
            'l_config_admin_dn': "cn=admin,cn=config",
            'l_admin_cn': 'admin',
            'ladmin_user': self.ladmin_user.text(),
            'l_admin_pwd': self.ldap_admin_pwd.text(),
            'ladmin_pwd': self.ladmin_pwd.text(),
            'ldap_status': ldap_status,
            'repo_addr': server_data["repo_addr"],
            'repo_key': server_data["repo_key"]
        # yeni ldap kur ya da varolan ldapı konfigüre et 'new' ya da 'update' parametreleri alıyor
        }
        if self.data['l_base_dn'] == "" or self.data['l_config_pwd'] == "" or self.data['ladmin_user'] == "" or self.data['l_admin_pwd'] == "" or self.data['ladmin_pwd'] == ""\
                or self.data['ip'] =="" or self.data['username'] == "" or self.data['password'] =="":
            self.msg_box.warning("Lütfen aşağıdaki alanları doldurunuz.\n"
                                     "- LDAP sunucu bağlantı bilgileri\n"
                                     "- LDAP base dn\n"
                                     "- LDAP admin parolası\n"
                                     "- LDAP config kullanıcı parolası\n"
                                     "- Lider arayüz kullanıcı parolası")

        else:
            self.status.install_status.setText("OpenLDAP kurulumu devam ediyor...")
            self.status.install_status.setStyleSheet("background-color: green")
            if os.path.exists(self.liderldap_path) and os.stat(self.liderldap_path).st_size != 0:
                with open(self.liderldap_path) as f:
                    read_data = json.load(f)
                read_data.update(self.data)
                with open(self.liderldap_path, 'w') as f:
                    json.dump(read_data, f, ensure_ascii=False)
                print("Lider Ahenk json dosyası güncellendi")
                # self.logger.info("Lider Ahenk json dosyası güncellendi")
                self.msg_box.information("LDAP bilgileri güncellendi\n"
                                         "LDAP kurulumuna başlanacak.")
            else:
                with open(self.liderldap_path, 'w') as f:
                    json.dump(self.data, f, ensure_ascii=False)
                    print("Lider Ahenk json dosyası oluşturuldu")
                # self.logger.info("Lider Ahenk json dosyası oluşturuldu")
                # self.message_box("Lider Ahenk json dosyası oluşturuldu")
                self.msg_box.information("LDAP bilgileri kaydedildi\n"
                                         "LDAP kurulumana başlanacak.")

            subprocess.Popen(["xterm", "-e", "tail", "-f",
                              self.log_path])

            if self.data['location'] == 'remote':
                self.im.ssh_connect(self.data)
                # self.im.install_ldap(self.data)
                self.im.ssh_disconnect()
            else:
                self.im.install_ejabberd(self.data)

            self.status.install_status.setText("OpenLDAP kurulumu tamamlandı")
            self.status.install_status.setStyleSheet("background-color: cyan")
            self.msg_box.information("OpenLDAP kurulumu tamamlandı")

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
