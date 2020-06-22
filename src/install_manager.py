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

