#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Author: Tuncay ÇOLAK <tuncay.colak@tubitak.gov.tr>

import os
from api.config.config_manager import ConfigManager
from api.logger.installer_logger import Logger
from argon2 import PasswordHasher

class OpenLdapInstaller(object):

    def __init__(self, ssh_api, ssh_status):
        self.ssh_api = ssh_api
        self.ssh_status = ssh_status
        self.logger = Logger()
        self.ldap_config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../conf/ldapconfig_temp')
        self.update_ldap_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../conf/update_ldap_temp')
        self.ldap_install_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../conf/ldap_install.sh')
        self.liderahenk_ldif_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../conf/liderahenk.ldif')
        self.sudo_ldif_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../conf/sudo.ldif')
        self.ldap_config_out_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../dist/ldapconfig')
        self.update_ldap_out_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../dist/update_ldap')

    def install(self, data):
        config_manager = ConfigManager()
        base_dn = self.base_dn_parse(data)
        l_admin_cn = "cn="+str(data['l_admin_cn'])
        # hashing password with argon2
        ph = PasswordHasher()
        ladmin_hash_password = ph.hash(data["ladmin_pwd"])
        test_ldap_user_hash_password = ph.hash("secret")
        admin_pwd_hash = ph.hash(data["l_admin_pwd"])
        config_pwd_hash = ph.hash(data["l_config_pwd"])

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
            "#LIDERCONSOLEPWD": "{ARGON2}" + str(ladmin_hash_password),
            "#LIDERCONSOLEMAILADDR": data["ladmin_mail_addr"],
            "#LIDER_SERVER_ADDR": data["lider_server_addr"],
            "#AD_DOMAIN_NAME": data["ad_domain_name"],
            "#AD_HOSTNAME": data["ad_hostname"],
            "#AD_HOST": data["ad_host"],
            "#ADUSER_PWD": data["ad_user_pwd"],
            "#AD_USER_NAME": data["ad_username"],
            "#AD_PORT": data["ad_port"],
            "#SIMPLELDAPUSER": "test_ldap_user",
            "#TESTLDAPUSERPWD": "{ARGON2}" + str(test_ldap_user_hash_password),
            "#NEWCONFIGPWD": "{ARGON2}" + str(config_pwd_hash),
            "#NEWADMINPWD": "{ARGON2}" + str(admin_pwd_hash)
        }

        # copy liderahenk.ldif file to ldap server
        self.ssh_api.scp_file(self.liderahenk_ldif_path, '/tmp')
        self.logger.info("liderahenk.ldif dosyası OpenLDAP sunucusuna koplayandı")

        if data["ldap_status"] == "new":
            #edit ldap_install_temp script
            self.ldap_config = open(self.ldap_config_path, 'r+')
            my_text = self.ldap_config.read()

            txt = config_manager.replace_all(my_text, ldap_data)
            self.ldap_config_out = open(self.ldap_config_out_path, 'w+')
            self.ldap_config_out.write(txt)
            self.ldap_config.close()
            self.ldap_config_out.close()

            if self.ssh_status == "Successfully Authenticated":
                cmd_ldap_remove = "sudo apt purge -y slapd ldap-utils && sudo rm -rf /var/ladps && sudo rm -rf /var/lib/ldap && sudo autoremove -y && apt autoclean -y"
                #copy ldap_install  script to ldap server
                self.ssh_api.scp_file(self.ldap_config_out_path, '/tmp')
                self.logger.info("ldapconfig betiği OpenLDAP sunucusuna kopyalandı")
                self.ssh_api.scp_file(self.sudo_ldif_path, '/tmp')

                ### install slapd package
                self.ssh_api.run_command(cmd_ldap_remove)
                self.ssh_api.run_command("export DEBIAN_FRONTEND='non-interactive'")
                self.ssh_api.run_command("echo 'slapd slapd/root_password password {0}' | sudo debconf-set-selections".format(data["l_admin_pwd"]))
                self.ssh_api.run_command("echo 'slapd slapd/root_password_again password {0}' | sudo debconf-set-selections".format(data["l_admin_pwd"]))
                self.ssh_api.run_command("echo 'slapd slapd/generated_adminpw password {0}' | sudo debconf-set-selections".format(data["l_admin_pwd"]))
                self.ssh_api.run_command("echo 'slapd slapd/adminpw password {0}' | sudo debconf-set-selections".format(data["l_admin_pwd"]))
                self.ssh_api.run_command("echo 'slapd slapd/password1 password {0}' | sudo debconf-set-selections".format(data["l_admin_pwd"]))
                self.ssh_api.run_command("echo 'slapd slapd/password2 password {0}' | sudo debconf-set-selections".format(data["l_admin_pwd"]))
                self.ssh_api.run_command("echo 'slapd slapd/no_configuration boolean false' | sudo debconf-set-selections")
                self.ssh_api.run_command("echo 'slapd slapd/invalid_config false' | sudo debconf-set-selections")
                self.ssh_api.run_command("echo 'slapd slapd/domain string {0}' | sudo debconf-set-selections".format(data["l_base_dn"]))
                self.ssh_api.run_command("echo 'slapd shared/organization string {0}' | sudo debconf-set-selections".format(data["l_org_name"]))
                self.ssh_api.run_command("echo 'slapd slapd/backend string MDB' | sudo debconf-set-selections")
                self.ssh_api.run_command("echo 'slapd slapd/purge_database boolean true' | sudo debconf-set-selections")
                self.ssh_api.run_command("echo 'slapd slapd/move_old_database boolean true' | sudo debconf-set-selections")
                self.logger.info("LDAP bilgileri alındı")
                result_code = self.ssh_api.run_command("sudo apt-get install -y slapd ldap-utils")
                if result_code == 0:
                    self.logger.info("slapd ve ldap-utils paketleri kuruldu")
                else:
                    self.logger.error("slapd ve ldap-utils paketleri kurulamadı, result_code: "+str(result_code))
                result_code = self.ssh_api.run_command("sudo DEBIAN_FRONTEND=noninteractive dpkg-reconfigure  slapd")
                if result_code == 0:
                    self.logger.info("slapd reconfigure edildi")
                else:
                    self.logger.error("slapd reconfigure edilemedi, result_code: " + str(result_code))
                self.ssh_api.run_command('sudo chmod +x /tmp/ldapconfig')
                result_code = self.ssh_api.run_command('sudo /bin/bash /tmp/ldapconfig')
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
            self.ssh_api.run_command('sudo chmod +x /tmp/update_ldap')
            self.ssh_api.run_command('sudo /bin/bash /tmp/update_ldap')
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
