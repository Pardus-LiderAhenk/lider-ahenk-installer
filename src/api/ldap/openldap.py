#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Author: Tuncay ÇOLAK <tuncay.colak@tubitak.gov.tr>

import os
from api.config.config_manager import ConfigManager
from api.logger.installer_logger import Logger

class OpenLdapInstaller(object):

    def __init__(self, ssh_api, ssh_status):
        self.ssh_api = ssh_api
        self.ssh_status = ssh_status
        self.logger = Logger()
        self.ldap_config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../conf/ldapconfig_temp')
        self.update_ldap_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../conf/update_ldap_temp')
        self.liderahenk_ldif_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../conf/liderahenk.ldif')
        self.sudo_ldif_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../conf/sudo.ldif')
        self.ldap_config_out_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../dist/ldapconfig')
        self.update_ldap_out_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../dist/update_ldap')

    def install(self, data):

        config_manager = ConfigManager()
        cfg_data = config_manager.read()

        base_dn = self.base_dn_parse(data)
        l_admin_cn = "cn="+str(data['l_admin_cn'])

        ldap_data = {
            "#BASEDN": base_dn[0],
            "#CNAME": data["l_base_dn"],
            "#BASECN": base_dn[1],
            "#ORGANIZATION": data["l_org_name"],
            "#ADMINCN": l_admin_cn,
            "#ADMINPASSWD": data["l_admin_pwd"],
            "#CNCONFIGADMINDN": data['l_config_admin_dn'],
            "#CNCONFIGADMINPASSWD": data["l_config_pwd"],
            "#LIDERCONSOLEUSER": data["ladmin_user"],
            "#LIDERCONSOLEPWD": data["ladmin_pwd"],
            "#LIDER_SERVER_ADDR": data["lider_server_addr"]
        }

        # copy liderahenk.ldif file to ldap server
        self.ssh_api.scp_file(self.liderahenk_ldif_path, '/tmp')
        self.logger.info("liderahenk.ldif dosyası OpenLDAP sunucusuna koplayandı")

        if data["ldap_status"] == "new":

            #edit ldap_install_temp script
            self.f1 = open(self.ldap_config_path, 'r+')
            my_text = self.f1.read()

            txt = config_manager.replace_all(my_text, ldap_data)
            self.f2 = open(self.ldap_config_out_path, 'w+')
            self.f2.write(txt)
            self.f1.close()
            self.f2.close()

            if self.ssh_status == "Successfully Authenticated" or data['location'] == 'local':
                #copy ldap_install  script to ldap server
                self.ssh_api.scp_file(self.ldap_config_out_path, '/tmp')
                self.logger.info("ldapconfig betiği OpenLDAP sunucusuna kopyalandı")
                self.ssh_api.scp_file(self.sudo_ldif_path, '/tmp')

                ### install slapd package
                self.ssh_api.run_command(cfg_data["cmd_ldap_remove"])
                self.ssh_api.run_command(cfg_data["ldap_deb_frontend"])
                self.ssh_api.run_command(cfg_data["ldap_debconf_generated_password"].format(data["l_admin_pwd"]))
                self.ssh_api.run_command(cfg_data["ldap_debconf_admin_password"].format(data["l_admin_pwd"]))
                self.ssh_api.run_command(cfg_data["ldap_debconf_conf"])
                self.ssh_api.run_command(cfg_data["ldap_debconf_domain"].format(data["l_base_dn"]))
                self.ssh_api.run_command(cfg_data["ldap_debconf_organization"].format(data["l_org_name"]))
                self.ssh_api.run_command(cfg_data["ldap_debconf_pwd1"].format(data["l_admin_pwd"]))
                self.ssh_api.run_command(cfg_data["ldap_debconf_pwd2"].format(data["l_admin_pwd"]))
                self.ssh_api.run_command(cfg_data["ldap_debconf_selectdb"])
                self.ssh_api.run_command(cfg_data["ldap_debconf_purgedb"])
                self.ssh_api.run_command(cfg_data["ldap_debconf_movedb"])
                self.logger.info("LDAP bilgileri alındı")
                result_code = self.ssh_api.run_command(cfg_data["cmd_ldap_install"])
                if result_code == 0:
                    self.logger.info("slapd ve ldap-utils paketleri kuruldu")
                else:
                    self.logger.error("slapd ve ldap-utils paketleri kurulamadı, result_code: "+str(result_code))

                self.ssh_api.run_command(cfg_data["cmd_ldap_reconf"])
                self.logger.info("slapd paketi reconfigure edildi")
                self.ssh_api.run_command(cfg_data["cmd_ldapconfig_execute"])
                result_code = self.ssh_api.run_command(cfg_data["cmd_ldapconfig_run"])
                if result_code == 0:
                    self.logger.info("ldap config betiği çalıştırıldı ve lider ahenk konfigürasyonları tamamlandı")
                else:
                    self.logger.error("ldap config betiği çalıştırılırken hata oluştu ve lider ahenk konfigürasyonları tamamlanamadı")
                self.logger.info("OpenLDAP kurulumu tamamlandı")
            else:
                 self.logger.error("OpenLDAP sunucusuna bağlantı sağlanamadı için kurulum yapılamadı. Lütfen bağlantı ayarlarını kotrol ediniz!")
            #     # print("bağlantı sağlanamadığı için kurulum yapılamadı..")

        else:
            self.f1 = open(self.update_ldap_path, 'r+')
            my_text = self.f1.read()
            txt = config_manager.replace_all(my_text, ldap_data)
            self.f2 = open(self.update_ldap_out_path, 'w+')
            self.f2.write(txt)
            self.f1.close()
            self.f2.close()
            # copy ldap_config  script to ldap server
            self.ssh_api.scp_file(self.update_ldap_out_path, '/tmp')
            self.logger.info("update_ldap betiği OpenLDAP sunucusuna koplayandı")
            self.ssh_api.run_command(cfg_data["cmd_update_ldap_execute"])
            self.ssh_api.run_command(cfg_data["cmd_update_ldap_run"])
            self.logger.info("Varolan OpenLDAP Lider Ahenk uygulamasına göre ayarlandı")

    def base_dn_parse(self, data):
        ### split for get data['base_dn']: liderahenk.org #BASECN and #BASEDN
        parse_dn = data["l_base_dn"].split('.')
        base_cn = parse_dn[0]
        dn_list = []
        for dn in parse_dn:
            message = 'dc=' + str(dn) + ','
            dn_list.append(message)
        base_dn = ''.join(str(x) for x in dn_list)
        base_dn = base_dn.strip(',')
        return base_dn, base_cn