#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Author: Tuncay ÇOLAK <tuncay.colak@tubitak.gov.tr>

import os
import shutil

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
        self.tomcat_service_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../conf/tomcat.service')
        self.application_properties_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../conf/lider.properties')
        self.application_properties_out_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../dist/lider.properties')
        self.lider_web_url = "http://liderahenk.org/downloads/ROOT.war"
        self.tomcat_tar_file = "http://liderahenk.org/downloads/apache-tomcat-9.0.36.tar.gz"
        self.dist_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../dist')
        self.liderv2_app_properties_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../dist/liderv2/src/main/resources/lider.properties')

    def install(self, data):
        repo_key = data["repo_key"]
        repo_key = repo_key.rsplit("/")[-1]
        if self.ssh_status == "Successfully Authenticated":
            cfg_data = self.config_manager.read()
            self.configure_lider_cfg(data)
            self.configure_db_cfg(data)
            self.configure_app_properties(data)

            result_code = self.ssh_api.run_command(cfg_data["cmd_soft_properties"])
            if result_code == 0:
                self.logger.info("software-properties-common paketi kuruldu")
            else:
                self.logger.error("software-properties-common paketi kurulamadı, result_code: " + str(result_code))
            result_code = self.ssh_api.run_command(
                cfg_data["cmd_liderahenk_repo_key"].format(data["repo_key"], repo_key))
            if result_code == 0:
                self.logger.info("Lider Ahenk repo key dosyası indirildi")
            else:
                self.logger.error("Lider Ahenk repo key dosyası indirilemedi, result_code: " + str(result_code))
            result_code = self.ssh_api.run_command(cfg_data["cmd_liderahenk_repo_add"].format(data["repo_addr"]))
            if result_code == 0:
                self.logger.info("Lider Ahenk repo adresi eklendi")
            else:
                self.logger.error("Lider Ahenk repo adresi eklenemedi, result_code: " + str(result_code))
            result_code = self.ssh_api.run_command(cfg_data["cmd_update"])
            if result_code == 0:
                self.logger.info("Paket listesi güncellendi(apt update)")
            else:
                self.logger.error("Paket listesi güncellenemdi, result_code: " + str(result_code))

            result_code = self.ssh_api.run_command("sudo apt-get install openjdk-8-jdk-headless -y")
            if result_code == 0:
                self.logger.info("openjdk-8 paketi başarıyla kuruldu")
            else:
                self.logger.error("openjdk-8 paketi kurulamadı")
            result_code = self.ssh_api.run_command("sudo groupadd tomcat")
            if result_code == 0:
                self.logger.info("tomcat grubu oluşturuldu")
            result_code = self.ssh_api.run_command("sudo useradd -s /bin/false -g tomcat -d /opt/tomcat tomcat")
            if result_code == 0:
                self.logger.info("tomcat kullanıcısı oluşturuldu ve ev dizini ayarlandı.")
            result_code = self.ssh_api.run_command("wget {0}".format(self.tomcat_tar_file))
            if result_code == 0:
                self.logger.info("tomcat başarıyla indirildi.")
            else:
                self.logger.error("tomcat indirilirken hata oluştu")
            result_code = self.ssh_api.run_command("sudo mkdir /opt/tomcat")
            self.logger.info("tomcat dizini oluşturuldu")
            result_code = self.ssh_api.run_command("sudo tar xf apache-tomcat-*tar.gz -C /opt/tomcat --strip-components=1")
            result_code = self.ssh_api.run_command("sudo chgrp -R tomcat /opt/tomcat")
            result_code = self.ssh_api.run_command("sudo chmod -R g+r /opt/tomcat/conf")
            result_code = self.ssh_api.run_command("sudo chmod g+x /opt/tomcat/conf")
            result_code = self.ssh_api.run_command("sudo chown -R tomcat /opt/tomcat/webapps/ /opt/tomcat/work/ /opt/tomcat/temp/ /opt/tomcat/logs/")
            self.ssh_api.scp_file(self.tomcat_service_path, '/tmp/')
            result_code = self.ssh_api.run_command("sudo cp /tmp/tomcat.service /etc/systemd/system/")
            result_code = self.ssh_api.run_command("sudo systemctl daemon-reload")
            result_code = self.ssh_api.run_command("sudo systemctl enable tomcat")
            result_code = self.ssh_api.run_command("sudo systemctl start tomcat")
            self.logger.info("tomcat konfigürastonu tamamlandı")
            self.ssh_api.scp_file(self.application_properties_out_path, '/tmp')
            result_code = self.ssh_api.run_command("sudo mkdir -p /etc/lider")
            result_code = self.ssh_api.run_command("sudo cp /tmp/lider.properties /etc/lider/")
            result_code = self.ssh_api.run_command("wget {0}".format(self.lider_web_url))
            if result_code == 0:
                self.logger.info("ROOT.war başarıyla indirildi.")
            else:
                self.logger.error("ROOT.war indirilirken hata oluştu")
            result_code = self.ssh_api.run_command("sudo cp ROOT.war /opt/tomcat/webapps/")
            result_code = self.ssh_api.run_command("sudo chown tomcat:tomcat /opt/tomcat/webapps/ROOT.war")
            # result_code = self.ssh_api.run_command("sudo systemctl restart tomcat.service")

            result_code = self.ssh_api.run_command("sudo apt-get install guacd -y")
            if result_code == 0:
                self.logger.info("Uzak masaüstü sunucusu yapılandırıldı")
            else:
                self.logger.error("Uzak masaüstü sunucusu yapılandırılırken hata oluştu. guacd uygulaması kurulamadı")
            # filer server configuration
            self.ssh_api.run_command("mkdir -p {0}/agent-files".format(data["fs_agent_file_path"]))
            self.ssh_api.run_command("sudo chown {0}:{0} {1}/agent-files".format(data['fs_username'], data['fs_agent_file_path']))
            self.ssh_api.run_command("sudo apt-get install -y sshpass rsync")
            self.logger.info("lider kurulumu tamamlandı")
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
            "#AGENT_FILE_PATH": data['fs_agent_file_path'],
            "#AD_DOMAIN_NAME": data["ad_domain_name"],
            "#AD_HOSTNAME": data["ad_hostname"],
            "#AD_HOST": data["ad_host"],
            "#AD_USER_PWD": data["ad_user_pwd"],
            "#AD_USER_NAME": data["ad_username"],
            "#AD_PORT": data["ad_port"]
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
            "#DBADDRESS": data['db_server_addr'],
            "#DBDATABASE": data['db_name'],
            "#DBUSERNAME": data['db_username'],
            "#DBPASSWORD": data['db_password']
        }
        self.f_db = open(self.db_conf_path, 'r+')
        db_text = self.f_db.read()
        txt = self.config_manager.replace_all(db_text, db_data)
        self.f_db_out = open(self.db_conf_out_path, 'w+')
        self.f_db_out.write(str(txt))
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

    def configure_app_properties(self, data):
        db_server = data["db_server_addr"]
        # if data['ip'] == db_server:
        #     db_server = "127.0.0.1"
        db_data = {
            "##DATABASEADDRESS##": db_server,
            "##DATABASENAME##": data['db_name'],
            "##DATABASEUSERNAME##": data['db_username'],
            "##DATABASAPASSWORD##": data['db_password']
        }

        self.f_db = open(self.application_properties_path, 'r+')
        db_text = self.f_db.read()
        txt = self.config_manager.replace_all(db_text, db_data)
        self.f_db_out = open(self.application_properties_out_path, 'w+')
        self.f_db_out.write(str(txt))
        self.f_db.close()
        self.f_db_out.close()
        self.logger.info("application properties dosyası oluşturuldu")

