#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Author: Tuncay ÇOLAK <tuncay.colak@tubitak.gov.tr>

import os
from api.config.config_manager import ConfigManager
from api.logger.installer_logger import Logger
from api.util.util import Util

class LiderConsoleInstaller(object):

    def __init__(self, ssh_api, ssh_status):
        self.ssh_api = ssh_api
        self.ssh_status = ssh_status
        self.logger = Logger()
        self.util = Util()
        self.config_manager = ConfigManager()
        self.lider_conf_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../conf/tr.org.liderahenk.cfg')
        self.db_conf_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../conf/tr.org.liderahenk.datasource.cfg')
        self.lider_conf_out_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../dist/tr.org.liderahenk.cfg')
        self.db_conf_out_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../dist/tr.org.liderahenk.datasource.cfg')

    def install(self, data):

        repo_key = data["repo_key"]
        repo_key = repo_key.rsplit("/")[-1]

        if self.ssh_status == "Successfully Authenticated" or data['location'] == 'local':
            cfg_data = self.config_manager.read()
            result_code = self.ssh_api.run_command(cfg_data["cmd_soft_properties"])
            if result_code == 0:
                self.logger.info("software-properties-common paketi kuruldu")
            else:
                self.logger.error("software-properties-common paketi kurulamadı, result_code: " + str(result_code))

            result_code = self.ssh_api.run_command(cfg_data["cmd_liderahenk_repo_key"].format(data["repo_key"], repo_key))
            if result_code == 0:
                self.logger.info("Lider Ahenk repo key dosyası indirildi")
            else:
                self.logger.error("Lider Ahenk repo key dosyası indirilemedi, result_code: " + str(result_code))

            result_code = self.ssh_api.run_command(cfg_data["cmd_liderahenk_repo_add"].format(data["repo_addr"]))
            if result_code == 0:
                self.logger.info("Lider Ahenk repo adresi eklendi")
            else:
                self.logger.error("Lider Ahenk repo adresi eklenemedi, result_code: "+str(result_code))

            result_code = self.ssh_api.run_command(cfg_data["cmd_update"])
            if result_code == 0:
                self.logger.info("Paket listesi güncellendi(apt update)")
            else:
                self.logger.error("Paket listesi güncellenemdi, result_code: "+str(result_code))

            result_code = self.ssh_api.run_command(cfg_data["cmd_lider_console_install"])
            if result_code == 0:
                self.logger.info("Lider Console paketi kurulumu yapıldı")
            else:
                self.logger.error("Lider Console paketi kurulamadı, result_code: "+str(result_code))

        else:
            self.logger.error("Lider Arayüz makinesine bağlantı sağlanamadığı için kurulum yapılamadı. Lütfen bağlantı ayarlarını kontrol ediniz!")
