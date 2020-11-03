#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Author: Tuncay ÇOLAK <tuncay.colak@tubitak.gov.tr>

import os
import json
import subprocess
import time

from PyQt5.QtWidgets import (QGridLayout, QGroupBox, QLabel, QLineEdit, QPushButton, QWidget, QVBoxLayout, QCheckBox)
from api.util.util import Util
from install_manager import InstallManager
from ui.message_box.message_box import MessageBox

class LiderPage(QWidget):
    def __init__(self, parent=None):
        super(LiderPage, self).__init__(parent)

        self.liderldap_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../dist/lider_ldap.json')
        self.liderejabberd_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../dist/lider_ejabberd.json')
        self.liderdb_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../dist/liderdb.json')
        self.lider_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../dist/lider.json')
        self.log_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../dist/installer.log')
        if not os.path.exists(os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../dist')):
            os.makedirs(os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../dist'))
        self.util = Util()
        self.im = InstallManager()
        self.msg_box = MessageBox()

    def lider_ahenk_install(self, params):
        lider_xterm = subprocess.Popen(["xterm", "-e", "tail", "-f", self.log_path])
        if params['db_install'] is True:
            self.database_install(params)
            time.sleep(5)
        if params['ldap_install'] is True:
            self.ldap_install(params)
            time.sleep(5)
        if params['ejabberd_install'] is True:
            self.ejabberd_install(params)
            time.sleep(5)
        if params['lider_install'] is True:
            self.lider_install(params)
        # time.sleep(5)
        # self.xterm.kill()

    def database_install(self, params):
        db_data = {
            # Server Configuration
            'ip': params["db_server_addr"],
            'username': params["db_server_username"],
            'password': params["db_server_username_pwd"],
            # Database Configuration
            'db_name': "lidermysdb",
            'db_username': "root",
            'db_password': params["db_password"],
            # Repo Configuration
        }
        with open(self.liderdb_path, 'w') as f:
            json.dump(db_data, f, ensure_ascii=False)

        ssh_status = self.im.ssh_connect(db_data)
        if ssh_status is True:
            self.im.install_mariadb(params)
            self.im.ssh_disconnect()
        else:
            self.msg_box.information("Veritabanı sunucusuna bağlantı sağlanamadı. Lütfen bağlantı ayarlarını kontrol ediniz.")

    def ldap_install(self, params):
        ldap_data = {
            # Server Configuration
            'ip': params["ldap_server_addr"],
            'username': params["ldap_server_username"],
            'password': params["ldap_server_username_pwd"],

            # OpenLDAP Configuration
            'l_base_dn': params["l_base_dn"],
            'l_config_pwd': params["l_config_pwd"],
            'l_org_name': params["l_org_name"],
            'l_config_admin_dn': "cn=admin,cn=config",
            'l_admin_cn': 'admin',
            'ladmin_user': params["ladmin_user"],
            'l_admin_pwd': params["l_admin_pwd"],
            'ladmin_pwd': params["ladmin_pwd"],
            'ladmin_mail_addr': params["ladmin_mail_addr"],
            'ldap_status': 'new',
            'lider_server_addr': params["lider_server_addr"],
            # yeni ldap kur ya da varolan ldapı konfigüre et 'new' ya da 'update' parametreleri alıyor

            # AD Configuration
            'ad_host': params["ad_host"],
            'ad_hostname': params["ad_hostname"],
            'ad_domain_name': params["ad_domain_name"],
            'ad_username': params["ad_username"],
            'ad_user_pwd': params["ad_user_pwd"],
            'ad_port': params["ad_port"]
        }
        with open(self.liderldap_path, 'w') as f:
            json.dump(ldap_data, f, ensure_ascii=False)

        ssh_status = self.im.ssh_connect(ldap_data)
        if ssh_status is True:
            self.im.install_ldap(params)
            self.im.ssh_disconnect()
        else:
            self.msg_box.information("OpenLDAP sunucusuna bağlantı sağlanamadı. Lütfen bağlantı ayarlarını kontrol ediniz.")

    def ejabberd_install(self, params):
        ejabberd_data = {
            # Server Configuration
            'ip': params["ejabberd_server_addr"],
            'username': params["ejabberd_server_username"],
            'password': params["ejabberd_server_username_pwd"],
            # Ejabberd Configuration
            'e_service_name': "im.liderahenk.org",
            # 'e_service_name': self.e_service_name.text(),
            'e_username': 'admin',
            # 'e_user_pwd': self.ejabberd_layout.e_user_pwd.text(),
            'e_user_pwd': params["e_user_pwd"],
            'e_hosts': params["ejabberd_server_addr"],
            'ldap_servers': params["ldap_server_addr"],
            'l_base_dn': params["l_base_dn"],

            # Lider Configuration
            'lider_username': 'lider_sunucu',
            'lider_user_pwd': params["lider_user_pwd"],
            'l_admin_pwd': params["l_admin_pwd"],
            'repo_key': params["repo_key"],
            'repo_addr': params["repo_addr"],
        }
        with open(self.liderejabberd_path, 'w') as f:
            json.dump(ejabberd_data, f, ensure_ascii=False)
        ssh_status = self.im.ssh_connect(ejabberd_data)
        if ssh_status is True:
            self.im.install_ejabberd(params)
            self.im.ssh_disconnect()
        else:
            self.msg_box.information("Ejabberd sunucusuna bağlantı sağlanamadı. Lütfen bağlantı ayarlarını kontrol ediniz.")

    def lider_install(self, params):
        lider_data = {
            # Server Configuration
            'ip': params["lider_server_addr"],
            'username': params["lider_server_username"],
            'password': params["lider_server_username_pwd"]
        }
        with open(self.lider_path, 'w') as f:
            json.dump(lider_data, f, ensure_ascii=False)
        ssh_status = self.im.ssh_connect(lider_data)
        if ssh_status is True:
            self.im.install_lider(params)
            self.im.ssh_disconnect()
        else:
            self.msg_box.information("Lider sunucusuna bağlantı sağlanamadı. Lütfen bağlantı ayarlarını kontrol ediniz.")
