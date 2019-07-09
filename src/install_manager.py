#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Author: Tuncay ÇOLAK <tuncay.colak@tubitak.gov.tr>

import json
import os

from api.ahenk.ahenk import AhenkInstaller
from api.database.mariadb import MariaDbInstaller
from api.ejabberd.ejabberd import EjabberInstaller
from api.ldap.openldap import OpenLdapInstaller
from api.lider_console.lider_console import LiderConsoleInstaller
from api.lider.lider import LiderInstaller
from api.logger.installer_logger import Logger
from api.util.util import Util
from api.config.config_manager import ConfigManager

class InstallManager(object):
    def __init__(self):
        super(InstallManager, self).__init__()
        self.util = Util()
        self.ssh_status = ""
        self.logger = Logger()
        self.config_maneger = ConfigManager()
        self.liderahenk_data_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'dist/liderahenk.json')
        self.liderldap_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../dist/lider_ldap.json')


    def install_mariadb(self, data):
        db_installer = MariaDbInstaller(self.util, self.ssh_status)
        self.logger.info("======>>>>> Veritabanı sunucu kurulumuna başlanıyor <<<<<======")
        db_installer.install(data)

    def install_ejabberd(self, data):
        ejabberd_installer = EjabberInstaller(self.util, self.ssh_status)
        self.logger.info("======>>>>> Ejabberd sunucu kurulumuna başlanıyor. <<<<<======")
        ejabberd_installer.install(data)

    def install_ldap(self, data):

        ldap_installer = OpenLdapInstaller(self.util, self.ssh_status)
        self.logger.info("======>>>>> OpenLDAP sunucu kurulumuna başlanıyor. <<<<<======")
        ldap_installer.install(data)

    def install_lider(self, data):
        lider_installer = LiderInstaller(self.util, self.ssh_status)
        self.logger.info("======>>>>> Lider sunucu Kurulumuna başlanıyor. <<<<<======")
        lider_installer.install(data)

    def install_lider_console(self, data):
        lider_console_installer = LiderConsoleInstaller(self.util, self.ssh_status)
        self.logger.info("======>>>>> Lider Arayüz Kurulumuna başlanıyor. <<<<<======")
        lider_console_installer.install(data)

    def install_ahenk(self, data):
        ahenk_installer = AhenkInstaller(self.util, self.ssh_status)
        self.logger.info("======>>>>> Ahenk Kurulumuna başlanıyor. <<<<<======")
        ahenk_installer.install(data)

    def ssh_connect(self, data):
        ssh_status = self.util.connect(data)
        self.ssh_status = ssh_status
        if self.ssh_status == "Successfully Authenticated":
            return True
        else:
            return False

    def ssh_disconnect(self):
        self.util.disconnect()
        # self.logger.info("installation successfull")

    def start_install(self):
        # copy installer.log file

        with open(self.liderahenk_data_path) as f:
            data = json.load(f)
        self.logger.info("liderahenk.json dosyasından veriler okunuyor")

        if data['location'] == 'remote':
            self.ssh_connect(data)
        if data['db_install'] is True:
            self.install_mariadb(data)
        if data['ldap_install'] is True:
            self.install_ldap(data)
        if data['ejabberd_install'] is True:
            self.install_ejabberd(data)
        if data['lider_install'] is True:
            self.install_lider(data)

        if data['location'] == 'remote':
            self.ssh_disconnect()
        else:
            self.logger.info("Lider Sunucu kurulumu tamamlandı")
            self.logger.info("installation successfull")

if __name__ == "__main__":
    data = {
        # where the application will be installed "remote" or "local" server
        'location': "remote",

        # util connection information
        'ip': "192.168.*.*",
        'username': "username",
        'password': "password",

        # Database Configuration
        'db_name': "liderdb",
        'db_password': "1",

        # Ejabberd Configuration
        'e_service_name': "im.liderahenk.org",
        'e_username': "admin",
        'e_user_pwd': "1222",
        'e_hosts': "im.liderahenk.org",
        'ldap_servers': "192.168.*.*",

        # OpenLDAP Configuration
        'l_admin_pwd': "1",
        'l_base_dn': "liderahenk.org",
        'l_config_pwd': "1",
        'l_org_name': "ankara",
        'l_config_admin_dn': "cn=admin,cn=config",
        'l_admin_cn': "admin",
        'ladmin_user': "ladmin",
        'ladmin_pwd': "1",
        'ldap_status': "new",  # yeni ldap kur ya da varolan ldapı konfigüre et 'new' ya da 'conf' parametreleri alıyor

        # Lider Configuration
        'lider_username': "lider_sunucu",
        'lider_user_pwd': "1",

        # File Server Configuration
        'file_server': "127.0.0.1",
        'fs_username': "lider",
        'fs_username_pwd': "1",
        'fs_plugin_path': '/home/lider',
        "fs_agreement_path": '/home/lider',
        "fs_agent_file_path": '/home/lider',

        # Database cfg Configuration
        'db_server': "localhost",
        'db_username': "root"
    }
    im = InstallManager()
    im.start_install()
