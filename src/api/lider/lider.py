#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Author: Tuncay ÇOLAK <tuncay.colak@tubitak.gov.tr>

import os
from api.config.config_manager import ConfigManager
from api.logger.installer_logger import Logger
from api.util.util import Util

class LiderInstaller(object):

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
            self.configure_lider_cfg(data)
            self.configure_db_cfg(data)
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

            result_code = self.ssh_api.run_command(cfg_data["cmd_lider_install"])
            if result_code == 0:
                self.logger.info("lider-server paketi kurulumu yapıldı")
            else:
                self.logger.error("lider-server paketi kurulamadı, result_code: "+str(result_code))

            self.ssh_api.scp_file(self.lider_conf_out_path, cfg_data["lider_des_path"])
            self.ssh_api.scp_file(self.db_conf_out_path, cfg_data["lider_des_path"])
            self.ssh_api.run_command(cfg_data["cmd_cp_lider_cfg"])
            self.logger.info("lider konfigürasyon dosyası LİDER sunucusuna kopyalandı")
            self.ssh_api.run_command(cfg_data["cmd_cp_db_cfg"])
            self.logger.info("veritabanı konfigürasyon dosyası LİDER sunucusuna kopyalandı")
            result_code = self.ssh_api.run_command(cfg_data["cmd_lider_service"])
            if result_code == 0:
                self.logger.info("lider servisi başlatıldı")
            else:
                self.logger.error("lider servisi başlatılamadı, resuşt_code: "+str(result_code))

            result_code = self.ssh_api.run_command(cfg_data["cmd_fs_dep"])
            if result_code == 0:
                self.logger.info("sshpass ve rsync paketleri başarıyla kuruldu")
            else:
                self.logger.error("sshpass ve rsync paketleri kurulamadı")

            agent_files_path = data['fs_agent_file_path']+'/agent-files'
            if data['location'] == 'remote':
                self.ssh_api.run_command(cfg_data["cmd_agents_files"].format(agent_files_path))
                self.logger.info("agent-files dizini oluşturuldu")
                self.ssh_api.run_command(cfg_data["cmd_chown_agents_files"].format(data["username"], agent_files_path))
                self.logger.info("agent-files dizini için owner değiştirildi")
            else:
                if not self.util.is_exist(agent_files_path):
                    self.util.create_directory_local(agent_files_path)
                    self.logger.info("agent-files dizini oluşturuldu")
                    self.util.change_owner(agent_files_path, data['username'], data['username'])
                    self.logger.info("agent-files dizini için owner değiştirildi")
                else:
                    self.logger.info("{0} dizini zaten var".format(agent_files_path))

            result_code = self.ssh_api.run_command(cfg_data["cmd_enable_lider_service"])
            self.logger.info("Lider servis olarak ayarlandı.")
        
        else:
            self.logger.error("LİDER sunucusuna bağlantı sağlanamadığı için kurulum yapılamadı. Lütfen bağlantı ayarlarını kotrol ediniz!")

    def configure_lider_cfg(self, data):
        l_base_dn = self.base_dn_parse(data)
        l_admin_dn = "cn=admin,"+str(l_base_dn)

        lider_data = {
            "#LDAP_SERVER": data['ldap_servers'],
            "#LDAP_ADMIN_DN": l_admin_dn,
            "#LDAP_ADMIN_PWD": data['l_admin_pwd'],
            "#LDAP_ROOT_DN": l_base_dn,
            "#XMPP_SERVER": data['e_hosts'],
            "#LIDER_USERNAME": data['lider_username'],
            "#XMPP_USER_PWD": data['lider_user_pwd'],
            "#XMPP_SERVICE_NAME": data['e_service_name'],
            "#LDAP_BASE_DN": l_base_dn,
            "#FILE_SERVER": data['file_server'],
            "#FS_USERNAME": data['fs_username'],
            "#FS_PASSWORD": data['fs_username_pwd'],
            "#PLUGIN_PATH": data['fs_plugin_path'],
            "#AGREEMENT_PATH": data['fs_agreement_path'],
            "#AGENT_FILE_PATH": data['fs_agent_file_path']
        }

        self.f_lider = open(self.lider_conf_path, 'r+')
        lider_text = self.f_lider.read()

        txt = self.config_manager.replace_all(lider_text, lider_data)
        self.f_lider_out = open(self.lider_conf_out_path, 'w+')
        self.f_lider_out.write(str(txt))
        self.f_lider.close()
        self.f_lider_out.close()
        self.logger.info("tr.org.liderahenk.cfg dosyası oluşturuldu")

    def configure_db_cfg(self, data):
        db_data = {
            "#DBADDRESS": data['db_server'],
            "#DBDATABASE": data['db_name'],
            "#DBUSERNAME": data['db_username'],
            "#DBPASSWORD": data['db_password']
        }
        self.f_db = open(self.db_conf_path, 'r+')
        db_text = self.f_db.read()
        txt = self.config_manager.replace_all(db_text, db_data)
        self.f_db_out = open(self.db_conf_out_path, 'w+')
        self.f_db_out.write(txt)
        self.f_db.close()
        self.f_db_out.close()
        self.logger.info("tr.org.datasource.cfg dosyası oluşturuldu")

    def base_dn_parse(self, data):
        ### split for get data['base_dn']: liderahenk.org #BASECN and #BASEDN
        parse_dn = data["l_base_dn"].split('.')
        dn_list = []
        for dn in parse_dn:
            message = 'dc=' + str(dn) + ','
            dn_list.append(message)
        base_dn = ''.join(str(x) for x in dn_list)
        base_dn = base_dn.strip(',')
        return base_dn
