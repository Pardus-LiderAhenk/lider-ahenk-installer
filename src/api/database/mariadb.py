#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Author: Tuncay ÇOLAK <tuncay.colak@tubitak.gov.tr>

from api.config.config_manager import ConfigManager
from api.logger.installer_logger import Logger
import mysql.connector
import time
import json

class MariaDbInstaller(object):

    def __init__(self, ssh_api, ssh_status):
        self.ssh_api = ssh_api
        self.ssh_status = ssh_status
        self.logger = Logger()
        self.data = None
        self.liderdb = None

        # Database configuration
        self.cmd_deb_frontend = "export DEBIAN_FRONTEND = \"noninteractive\""
        self.db_debconf_pwd = "echo \'mariadb-server mysql-server/root_password password {0}\' | sudo debconf -set -selections"
        self.db_debconf_pwd_again = "echo \'mariadb-server mysql-server/root_password_again password {0}\' | sudo debconf -set -selections"
        self.cmd_db_install = "sudo apt-get install -y mariadb-server"
        self.cmd_db_dep = "sudo apt-get -f install"
        self.cmd_db_set_password = "sudo mysql -uroot -e \"SET PASSWORD FOR 'root'@'localhost' = PASSWORD('{0}')\";"
        # self.cmd_create_db = "sudo mysql -uroot -p{0} -e \'CREATE DATABASE {1} DEFAULT CHARACTER SET utf8 DEFAULT COLLATE utf8_general_ci\'"
        self.cmd_create_db = "CREATE DATABASE {0} DEFAULT CHARACTER SET utf8 DEFAULT COLLATE utf8_general_ci"
        # self.cmd_db_replace_bind_addr = "sudo sed -i \'s/^bind-address/#&/\' /etc/mysql/my.cnf"
        self.cmd_db_replace_bind_addr = "sudo sed -i \'s/^bind-address/#&/\' /etc/mysql/mariadb.conf.d/50-server.cnf"
        self.cmd_db_service = "sudo systemctl restart mysql.service"
        self.cmd_db_grant_privileges = "mysql -uroot -p{0} -e \"GRANT ALL PRIVILEGES ON *.* TO 'root'@'%' IDENTIFIED BY '{1}' WITH GRANT OPTION;\""
        # self.cmd_create_config_table = "mysql -uroot -p{0} -e \"CREATE TABLE {1}.c_config (config_id INT NOT NULL, create_date VARCHAR(45) NOT NULL, modify_date VARCHAR(45) NULL, name VARCHAR(45) NOT NULL, value VARCHAR(45) NULL, PRIMARY KEY (config_id));\""
        self.cmd_create_config_table = "CREATE TABLE c_config (config_id INT NOT NULL, create_date VARCHAR(45) NOT NULL, modify_date VARCHAR(45) NULL, name VARCHAR(45) NOT NULL, value LONGTEXT NULL, PRIMARY KEY (config_id));"

    def install(self, data):
        self.data = data
        config_manager = ConfigManager()

        if self.ssh_status == "Successfully Authenticated":
            result_code = self.ssh_api.run_command("sudo apt update")
            if result_code == 0:
                self.logger.info("Paket listesi güncellendi(apt update)")
            else:
                self.logger.error("Paket listesi güncellenemdi, result_code: "+str(result_code))
            # result_code = self.ssh_api.run_command(self.cmd_deb_frontend)
            # result_code = self.ssh_api.run_command(self.db_debconf_pwd.format(data["db_password"]))
            # result_code = self.ssh_api.run_command(self.db_debconf_pwd_again.format(data["db_password"]))
            result_code = self.ssh_api.run_command(self.cmd_db_install)
            if result_code == 0:
                self.logger.info("Mariadb paketi kuruldu")
            else:
                self.logger.error("Mariadb paketi kurulamadı, result_code: "+str(result_code))
            result_code = self.ssh_api.run_command(self.cmd_db_dep)
            if result_code == 0:
                self.logger.info("Veritabanı bağımlılıkları kuruldu")
            else:
                self.logger.error("Veritabanı bağımlılıkları kurulamadı, result_code: "+str(result_code))
            result_code = self.ssh_api.run_command(self.cmd_db_set_password.format(data['db_password']))
            if result_code == 0:
                self.logger.info("Veritabanı parolası tanımlandı.")
            else:
                self.logger.error("Veritabanı parolası tanımlanırken hata oluştu. Result Code: {0}".format(result_code))
            result_code = self.ssh_api.run_command(self.cmd_db_service)
            if result_code == 0:
                self.logger.info("Veritabanı servisi başlatıldı.")
            else:
                self.logger.error("Veritabanı servisi başlatılamadı, result_code: " + str(result_code))
            result_code = self.ssh_api.run_command(self.cmd_db_replace_bind_addr)
            result_code = self.ssh_api.run_command(self.cmd_db_service)
            if result_code == 0:
                self.logger.info("Veritabanı servisi başlatıldı.")
            else:
                self.logger.error("Veritabanı servisi başlatılamadı, result_code: " + str(result_code))
            self.logger.info("---------->>>> "+str(self.cmd_db_grant_privileges.format(data["db_password"], data["db_password"])))
            result_code = self.ssh_api.run_command(self.cmd_db_grant_privileges.format(data["db_password"], data["db_password"]))
            if result_code == 0:
                self.logger.info("Veritabanı grant yetkisi verildi")
            else:
                self.logger.error("Veritabanı grant yetkisi verilemedi, result_code: "+str(result_code))
            self.connect_db()
            self.create_liderdb()
            self.create_config_table()
            self.insert_to_config()
        else:
            self.logger.error("Veritabanı sunucusuna bağlantı sağlanamadığı için kurulum yapılamadı. Lütfen bağlantı ayarlarını kotrol ediniz!")
        self.liderdb.close()

    def connect_db(self):
        try:
            self.liderdb = mysql.connector.connect(
                host=self.data["db_server_addr"],
                user="root",
                password=self.data["db_password"]
            )
            self.logger.info("Veritabanına bağlantı kuruldu")
        except Exception as e:
            self.logger.error("Veritabanına bağlantı kurulurken hata oluştu. HATA:{0}".format(str(e)))

    def create_liderdb(self):
        try:
            create_database = self.liderdb.cursor()
            create_database.execute(self.cmd_create_db.format(self.data["db_name"]))
            create_database.close()
            self.logger.info("liderdb veritabanı oluşturuldu")
        except Exception as e:
            self.logger.error("lidermysdb oluşturulurken hata oluştu. HATA:{0}".format(str(e)))

    def create_config_table(self):
        try:
            liderdb = mysql.connector.connect(
                user='root', password=self.data["db_password"], host=self.data["db_server_addr"], database=self.data["db_name"]
            )
            cursor = liderdb.cursor()
            cursor.execute(self.cmd_create_config_table)
            cursor.close()
            liderdb.close()
            self.logger.info("c_config tablosu oluşturuldu")
        except Exception as e:
            self.logger.error("c_config tablosu oluşturulurken hata oluştu. HATA:{0}".format(str(e)))

    def insert_to_config(self):
        params = {
        "adAdminPassword": self.data['ad_user_pwd'],
        "adAdminUserName": self.data['ad_username'],
        "adDomainName": self.data['ad_domain_name'],
        "adHostName": self.data['ad_hostname'],
        "adIpAddress": self.data['ad_host'],
        "adPort": self.data['ad_port'],
        "adAdminUserFullDN": self.data['ad_user_dn'],
        "agentLdapBaseDn": "ou=Agents,{0}".format(self.base_dn_parse()),
        "agentLdapIdAttribute": "cn",
        "agentLdapJidAttribute": "uid",
        "agentLdapObjectClasses": "pardusDevice,device",
        "ahenkGroupLdapBaseDn": "ou=Agent,ou=Groups,{0}".format(self.base_dn_parse()),
        "alarmCheckReport": None,
        "cronIntervalEntrySize": None,
        "cronTaskList": None,
        "disableLocalUser": False,
        "domainType": "LDAP",
        "entrySizeLimit": None,
        "fileServerAgentFilePath": "{path}/agent-files/{agent}/".format(path=self.data['fs_agent_file_path'], agent="{0}"),
        "fileServerAgreementPath": "{0}/sample-agreement.txt".format(self.data['fs_agreement_path']),
        "fileServerHost": self.data['file_server'],
        "fileServerPassword": self.data['fs_username_pwd'],
        "fileServerPluginPath": "{path}/plugins/ahenk-{param1}_{param2}_amd64.deb".format(path=self.data['fs_plugin_path'], param1="{0}", param2="{1}"),
        "fileServerPort": 22,
        "fileServerProtocol": "SSH",
        "fileServerUsername": self.data['fs_username'],
        "groupLdapBaseDn": "ou=Groups,{0}".format(self.base_dn_parse()),
        "groupLdapObjectClasses": "groupOfNames",
        "hotDeploymentPath": None,
        "ldapAllowSelfSignedCert": False,
        "ldapEmailAttribute": "mail",
        "ldapMailNotifierAttributes": "cn, mail, departmentNumber, uid",
        "ldapPassword": self.data['l_admin_pwd'],
        "ldapPort": "389",
        "ldapRootDn": self.base_dn_parse(),
        "ldapSearchAttributes": "cn,objectClass,uid,liderPrivilege",
        "ldapServer": self.data['ldap_servers'],
        "ldapUseSsl": False,
        "ldapUsername": "cn=admin,{0}".format(self.base_dn_parse()),
        "liderLocale": "tr",
        "mailAddress": None,
        "mailCheckPolicyCompletionPeriod": None,
        "mailCheckTaskCompletionPeriod": None,
        "mailHost": None,
        "mailPassword": None,
        "mailSendOnPolicyCompletion": None,
        "mailSendOnTaskCompletion": None,
        "mailSmtpAuth": None,
        "mailSmtpConnTimeout": None,
        "mailSmtpPort": None,
        "mailSmtpSslEnable": None,
        "mailSmtpStartTlsEnable": None,
        "mailSmtpTimeout": None,
        "mailSmtpWriteTimeout": None,
        "roleLdapObjectClasses": "sudoRole",
        "taskManagerCheckFutureTask": None,
        "taskManagerFutureTaskCheckPeriod": None,
        "userAuthorizationEnabled": True,
        "userGroupLdapBaseDn": "ou=User,ou=Groups,{0}".format(self.base_dn_parse()),
        "userLdapBaseDn": "ou=Users,{0}".format(self.base_dn_parse()),
        "userLdapObjectClasses": "pardusAccount,pardusLider",
        "userLdapPrivilegeAttribute": "liderPrivilege",
        "userLdapRolesDn": "ou=Role,ou=Groups,{0}".format(self.base_dn_parse()),
        "userLdapUidAttribute": "uid",
        "xmppAllowSelfSignedCert": False,
        "xmppHost": self.data['e_hosts'],
        "xmppMaxRetryConnectionCount": 5,
        "xmppPacketReplayTimeout": 10000,
        "xmppPassword": self.data['lider_user_pwd'],
        "xmppPingTimeout": 300,
        "xmppPort": 5222,
        "xmppPresencePriority": 1,
        "xmppResource": "Smack",
        "xmppServiceName": self.data['e_service_name'],
        "xmppUseCustomSsl": False,
        "xmppUseSsl": False,
        "xmppUsername": "lider_sunucu",
        "xmppBoshAddress": "http://" + self.data['e_hosts'] + ":5280/bosh",
        "selectedRegistrationType": "DEFAULT",
        "sudoRoleType": "LDAP"
    }
        try:
            # date = datetime.datetime.strptime('my date', "%b %d %Y %H:%M")
            liderdb = mysql.connector.connect(
                user='root', password=self.data["db_password"], host=self.data["db_server_addr"], database=self.data["db_name"]
            )
            cursor = liderdb.cursor()
            query = "INSERT INTO c_config (config_id, create_date, modify_date, name, value) VALUES (%s, %s, %s, %s, %s)"
            values = ("1", time.strftime('%Y-%m-%d %H:%M:%S'), None, "liderConfigParams", json.dumps(params))
            cursor.execute(query, values)
            liderdb.commit()
            self.logger.info("liderahenk konfigürasyonlar veritabanına eklendi")
        except Exception as e:
            self.logger.error("liderahenk konfigürasyonlar veritabanına eklenirken hata oluştu. HATA:{0}".format(str(e)))

    def base_dn_parse(self):
        ### split for get data['base_dn']: liderahenk.org #BASECN and #BASEDN
        parse_dn = self.data["l_base_dn"].split('.')
        dn_list = []
        for dn in parse_dn:
            message = 'dc=' + str(dn) + ','
            dn_list.append(message)
        base_dn = ''.join(str(x) for x in dn_list)
        base_dn = base_dn.strip(',')
        return base_dn
