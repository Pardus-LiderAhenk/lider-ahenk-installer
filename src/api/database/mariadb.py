#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Author: Tuncay ÇOLAK <tuncay.colak@tubitak.gov.tr>

from api.config.config_manager import ConfigManager
from api.logger.installer_logger import Logger

class MariaDbInstaller(object):

    def __init__(self, ssh_api, ssh_status):
        self.ssh_api = ssh_api
        self.ssh_status = ssh_status
        self.logger = Logger()

        self.cmd_db_grant_privileges = "mysql -uroot -p{0} -e \"GRANT ALL PRIVILEGES ON *.* TO 'root'@'%' IDENTIFIED BY '{1}' WITH GRANT OPTION;\""

    def install(self, data):

        config_manager = ConfigManager()
        cfg_data = config_manager.read()
        # print(cfg_data)
        repo_key = data["repo_key"]
        repo_key = repo_key.rsplit("/")[-1]

        if self.ssh_status == "Successfully Authenticated" or data['location'] == 'local':

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

            result_code = self.ssh_api.run_command(cfg_data["cmd_deb_frontend"])
            result_code = self.ssh_api.run_command(cfg_data["db_debconf_pwd"].format(data["db_password"]))
            result_code = self.ssh_api.run_command(cfg_data["db_debconf_pwd_again"].format(data["db_password"]))

            result_code = self.ssh_api.run_command(cfg_data["cmd_db_install"])
            if result_code == 0:
                self.logger.info("Mariadb paketi kuruldu")
            else:
                self.logger.error("Mariadb paketi kurulamadı, result_code: "+str(result_code))

            result_code = self.ssh_api.run_command(cfg_data["cmd_db_dep"])
            if result_code == 0:
                self.logger.info("Veritabanı bağımlılıkları kuruldu")
            else:
                self.logger.error("Veritabanı bağımlılıkları kurulamadı, result_code: "+str(result_code))

            result_code = self.ssh_api.run_command(cfg_data["cmd_create_db"].format(data["db_password"], data["db_name"]))
            if result_code == 0:
                self.logger.info("liderdb veritabanı oluşturuldu")
            else:
                self.logger.error("liderdb veritabanı oluşturulamadı, result_code: "+str(result_code))

            print("---------->>>> "+str(self.cmd_db_grant_privileges.format(data["db_password"], data["db_password"])))
            self.logger.info("---------->>>> "+str(self.cmd_db_grant_privileges.format(data["db_password"], data["db_password"])))
            result_code = self.ssh_api.run_command(self.cmd_db_grant_privileges.format(data["db_password"], data["db_password"]))
            if result_code == 0:
                self.logger.info("Veritabanı grant yetkisi verildi")
            else:
                self.logger.error("Veritabanı grant yetkisi verilemedi, result_code: "+str(result_code))

            result_code = self.ssh_api.run_command(cfg_data["cmd_db_replace_bind_addr"])
            result_code = self.ssh_api.run_command(cfg_data["cmd_db_service"])
            if result_code == 0:
                self.logger.info("Veritabanı servisi başlatıldı.")
            else:
                self.logger.error("Veritabanı servisi başlatılamadı, result_code: "+str(result_code))
        else:
            self.logger.error("Veritabanı sunucusuna bağlantı sağlanamadığı için kurulum yapılamadı. Lütfen bağlantı ayarlarını kotrol ediniz!")
