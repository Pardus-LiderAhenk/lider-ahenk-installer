#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Author: İsmail BAŞARAN <ismail.basaran@tubitak.gov.tr> <basaran.ismaill@gmail.com>
# Author: Tuncay ÇOLAK <tuncay.colak@tubitak.gov.tr>

import os
from api.config.config_manager import ConfigManager
from api.logger.installer_logger import Logger
import time

class EjabberInstaller(object):

    def __init__(self, ssh_api, ssh_status):
        self.ssh_api = ssh_api
        self.ssh_status = ssh_status
        self.logger = Logger()
        self.config_manager = ConfigManager()
        self.jabberd_template_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../conf/ejabberd_temp.yml')
        self.jabberd_out_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../dist/ejabberd.yml')

    def install(self, data):
        config_manager = ConfigManager()
        # configuration ejabberd.yml
        base_dn = self.base_dn_parse(data)
        ldap_root_dn = "cn=admin,"+str(base_dn) #cn=admnin,dc=liderahenk,dc=org

        repo_key = data["repo_key"]
        repo_key = repo_key.rsplit("/")[-1]

        cfg_data = config_manager.read()
        conf_data = {
            "#HOST": data['e_hosts'],
            "#LDAP_SERVER": data['ldap_servers'],
            "#LDAP_ROOT_DN": ldap_root_dn,
            "#LDAP_ROOT_PWD": data['l_admin_pwd'],
            "#LDAP_BASE_DN": base_dn,
            "#SERVICE_NAME": data['e_service_name']
        }
        self.f_ejabberd_yml = open(self.jabberd_template_path, 'r+')
        jabber_data = self.f_ejabberd_yml.read()
        self.logger.info("Ejabberd sunucu kurulumu için veriler okundu")

        txt = self.config_manager.replace_all(jabber_data, conf_data)
        self.f_ejabberd_yml_out = open(self.jabberd_out_path, 'w+')
        self.f_ejabberd_yml_out.write(txt)
        self.f_ejabberd_yml.close()
        self.f_ejabberd_yml_out.close()
        self.logger.info("ejabberd.yml dosyası oluşturuldu")

        #run commands of ejabberd
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

            result_code = self.ssh_api.run_command(cfg_data["cmd_ejabberd_install"])
            if result_code == 0:
                self.logger.info("Ejabberd paketi kuruldu")
            else:
                self.logger.error("Ejabberd paketi kurulamadı, result_code: " + str(result_code))

            self.ssh_api.scp_file(self.jabberd_out_path, cfg_data["jabberd_des_path"])
            if result_code == 0:
                self.logger.info("Ejabberd konfigürasyon dosyası sunucuya kopyalandı")
            else:
                self.logger.error("Ejabberd konfigürasyon dosyası sunucuya kopyalandı")

            self.ssh_api.run_command(cfg_data["cmd_cp_conf"].format(cfg_data["jabberd_des_path"], cfg_data["jabberd_conf_path"]))

            result_code = self.ssh_api.run_command(cfg_data["cmd_jabberd_start"].format(cfg_data["cmd_bin_ejabberd_path"]))
            if result_code == 0:
                self.logger.info("Ejabberd servisi başlatıldı")
            else:
                self.logger.error("Ejabberd servisi başlatılamadı, result_code: "+str(result_code))

            print("---------->>>> Start : %s" % time.ctime())
            time.sleep(10)
            print("-------->>>>> End : %s" % time.ctime())

            result_code = self.ssh_api.run_command(cfg_data["cmd_register"].format(cfg_data["cmd_bin_ejabberd_path"], data["e_username"], data["e_service_name"], data["e_user_pwd"]))
            if result_code == 0:
                self.logger.info("{0} kullanıcısı kaydedildi".format(data["e_username"]))
            else:
                self.logger.error("{0} kullanıcısı kaydedilemedi, result_code: ".format(data["e_username"]) +str(result_code))

            result_code = self.ssh_api.run_command(cfg_data["cmd_register"].format(cfg_data["cmd_bin_ejabberd_path"], data["lider_username"], data["e_service_name"], data["lider_user_pwd"]))
            if result_code == 0:
                self.logger.info("{0} kullanıcısı kaydedildi".format(data["lider_username"]))
            else:
                self.logger.error("{0} kullanıcısı kaydedilemedi, result_code: ".format(data["lider_username"])+str(result_code))

            result_code = self.ssh_api.run_command(cfg_data["cmd_srg_create"].format(cfg_data["cmd_bin_ejabberd_path"], data["e_service_name"]))
            if result_code == 0:
                self.logger.info("shared roster grubu oluşturuldu.")
            else:
                self.logger.error("shared roster grubu oluşturulamadı, resuşt_code: "+str(result_code))

            result_code = self.ssh_api.run_command(cfg_data["cmd_srg_user_add"].format(cfg_data["cmd_bin_ejabberd_path"], data["e_service_name"]))
            if result_code == 0:
                self.logger.info("Kullanıcılar shared roster grubuna eklendi")
            else:
                self.logger.error("Kullanıcılar shared roster grubuna eklenemedi, result_code: "+str(result_code))

            result_code = self.ssh_api.run_command(cfg_data["cmd_jabberd_restart"].format(cfg_data["cmd_bin_ejabberd_path"]))
            if result_code == 0:
                self.logger.info("Ejabberd servisi başlatıldı")
            else:
                self.logger.error("Ejabberd servisi başlatılamadı, result_code: "+str(result_code))
            result_code = self.ssh_api.run_command(cfg_data["cmd_jabberd_status"].format(cfg_data["cmd_bin_ejabberd_path"]))
            if result_code == 0:
                self.logger.info("Ejabberd servisi çalışıyor")
            else:
                self.logger.error("Ejabberd servisi çalışmıyor")
            self.ssh_api.run_command(cfg_data["cmd_hold_ejabberd"])


            self.ssh_api.run_command(cfg_data["cmd_copy_ejabberd_service"].format(cfg_data["cmd_bin_ejabberd_path"]))
            self.logger.info("ejabberd.service dosyası /etc/systemd/system/ dizinine kopyalandı")
            result_code = self.ssh_api.run_command(cfg_data["cmd_system_reload"])
            result_code = self.ssh_api.run_command(cfg_data["cmd_enable_ejabberd_service"])
            if result_code == 0:
                self.logger.info("Ejabberd servis olarak ayarlandı.")
            else:
                self.logger.error("Ejabberd servis olarak ayarlanamadı.")
        else:
            # print("bağlantı sağlanamadığı için kurulum yapılamadı..")
            self.logger.error("XMPP sunucusuna bağlantı sağlanamadığı için kurulum yapılamadı. Lütfen bağlantı ayarlarını kotrol ediniz!")

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