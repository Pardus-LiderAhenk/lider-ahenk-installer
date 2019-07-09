#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Author: Tuncay ÇOLAK <tuncay.colak@tubitak.gov.tr>

from api.config.config_manager import ConfigManager
from api.logger.installer_logger import Logger

class AhenkInstaller(object):

    def __init__(self, ssh_api, ssh_status):
        self.ssh_api = ssh_api
        self.ssh_status = ssh_status
        self.logger = Logger()

    def install(self, data):

        repo_key = data["repo_key"]
        repo_key = repo_key.rsplit("/")[-1]

        config_manager = ConfigManager()
        cfg_data = config_manager.read()
        # print(cfg_data)
        if self.ssh_status == "Successfully Authenticated":

            result_code = self.ssh_api.run_command(cfg_data["cmd_soft_properties"])
            if result_code == 0:
                self.logger.info("software-properties-common paketi kuruldu")
            else:
                self.logger.error("software-properties-common paketi kurulamadı, result_code: "+str(result_code))

            result_code = self.ssh_api.run_command(cfg_data["cmd_liderahenk_repo_key"].format(data["repo_key"], repo_key))
            if result_code == 0:
                self.logger.info("Lider Ahenk repo key dosyası indirildi")
            else:
                self.logger.error("Lider Ahenk repo key dosyası indirilemedi, result_code: "+str(result_code))

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

            result_code = self.ssh_api.run_command(cfg_data["cmd_ahenk_install"])
            if result_code == 0:
                self.logger.info("Ahenk paketi kuruldu")
            else:
                self.logger.error("Ahenk paketi kurulamadı, result_code: "+str(result_code))

            result_code = self.ssh_api.run_command(cfg_data["cmd_ahenk_dep"])
            if result_code == 0:
                self.logger.info("Ahenk bağımlılıkları kuruldu")
                self.logger.info("Ahenk kurulumu tamamlandı")
            else:
                self.logger.error("Ahenk bağımlılıkları kurulamadı, result_code: "+str(result_code))

            result_code = self.ssh_api.run_command(cfg_data["cmd_ahenk_register"].format(data["host"], data["ldap_user"], data["ldap_user_pwd"]))
            if result_code == 0:
                self.logger.info("Ahenk  etki alanına başarıyla alındı")
            else:
                self.logger.error("Ahenk etki alanına alınamadı, result_code: "+str(result_code))

        else:
            self.logger.error("Ahenk kurulacak istemciye bağlantı sağlanamadığı için kurulum yapılamadı. Lütfen bağlantı ayarlarını kotrol ediniz!")
