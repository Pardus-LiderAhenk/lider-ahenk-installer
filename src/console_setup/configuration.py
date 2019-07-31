#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Author: Agah Hulusi OZ <enghulusi@gmail.com>

import json
import os
import random
import string
import time
from getpass import getpass

from install_manager import InstallManager


class Configuration():
    def __init__(self):
        super(Configuration, self).__init__()
        self.liderldap_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../dist/lider_ldap.json')
        self.liderejabberd_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../dist/lider_ejabberd.json')
        self.liderdb_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../dist/liderdb.json')
        self.lider_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../dist/lider.json')
        self.server_list_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../dist/server_list_file.json')
        self.lider_ahenk = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'dist/lider_ahenk.json')
        self.log_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../dist/installer.log')
        if not os.path.exists(os.path.join(os.path.dirname(os.path.abspath(__file__)), '../dist')):
            os.makedirs(os.path.join(os.path.dirname(os.path.abspath(__file__)), '../dist'))

        self.im = InstallManager()
        self.l_base_dn = None
        self.ladmin_user = None
        self.l_admin_pwd = None
        self.ladmin_pwd = None
        self.e_user_pwd = None
        self.ldap_status = "new"

    def lider_ahenk_install(self):

            print("****************************************")
            print("*****Sunucu Konfigürasyon Bilgileri*****")
            print("****************************************")

            while (True):
                self.l_base_dn = input("LDAP Base DN (liderahenk.org) : ")

                if self.l_base_dn == "q" or self.l_base_dn == "Q":
                    exit()
                elif self.l_base_dn != "":
                    break

            while (True):
                self.l_admin_pwd = getpass("Sistem Admin Parolası (****) : ")
                if self.l_admin_pwd == "q" or self.l_admin_pwd == "Q":
                    exit()
                elif self.l_admin_pwd != "":
                    break
            while (True):
                self.ladmin_user = input("Lider Arayüz Kullanıcı Adı (lider_console) : ")
                if self.ladmin_user == "q" or self.ladmin_user == "Q":
                    exit()
                elif self.ladmin_user != "":
                    break
            while (True):
                self.ladmin_pwd = getpass("Lider Arayüz Kullanıcı Parolası (****) : ")
                if  self.ladmin_pwd == "q" or self.ladmin_pwd == "Q":
                    exit()
                elif self.ladmin_pwd != "":
                    break
            self.e_user_pwd = self.l_admin_pwd

            while (True):
                print(" ")
                while (True):
                    self.Islem = input("Var olan LDAP'ı güncellemek için 'G', yeni bir LDAP kurmak için 'K' seçiniz : ")
                    if self.Islem == "q" or self.Islem == "Q" :
                        exit()
                    elif self.Islem != "":
                        break
                if self.Islem == 'K' or self.Islem == 'k':
                    self.ldap_status = 'new'
                    break
                elif self.Islem == 'G' or self.Islem == 'g':
                    # if ldap_status is 'Güncelle'
                    self.ldap_status = 'update'
                    break
                else:
                    print("Yanlış seçtiniz !!!")

            while(True):
                print("Lider Ahenk Sunucu Konfigürasyon tamamlanmıştır. Kuruluma devam edilsin mi ? : ")
                secim = input("Evet(E) veya Hayır(H) : ")
                if secim == 'e' or secim == 'E':

                    print("Lider Ahenk sunucu konfigürasyon bilgileri kaydedildi. Kurulum başlayacaktır...")
                    time.sleep(6)
                    # subprocess.Popen(["xterm", "-e", "tail", "-f",
                    #                   self.log_path])

                    ## get connect and repo settings data
                    with open(self.server_list_path) as f:
                        server_data = json.load(f)

                        self.database_install(server_data)
                        time.sleep(5)
                        self.ldap_install(server_data)
                        time.sleep(5)
                        self.ejabberd_install(server_data)
                        time.sleep(5)
                        self.lider_install(server_data)
                    break
                elif secim == 'h' or secim == 'H':
                    exit()
    def database_install(self, server_data):

        print("*****VERİTABANI*****\n")

        if server_data["selection"] == "advanced":
            ip = server_data["Veritabanı"][0]["ip"]
            username = server_data["Veritabanı"][0]["username"]
            password = server_data["Veritabanı"][0]["password"]
            location = server_data["Veritabanı"][0]["location"]

        else:
            # selection is standart
            ip = server_data["ip"]
            username = server_data["username"]
            password = server_data["password"]
            location = server_data["location"]

        ## Random Password Generator for "databases user's password"
        chars = string.ascii_letters + string.digits
        rnd = random.SystemRandom()
        self.db_password = ''.join(rnd.choice(chars) for i in range(10))

        self.data = {
            'location': location,
            # Server Configuration
            'ip': ip,
            'username': username,
            'password': password,
            # Database Configuration
            'db_name': "liderdb",
            'db_username': "root",
            'db_password': self.db_password,
            # Repo Configuration
            'repo_addr': server_data["repo_addr"],
            'repo_key': server_data["repo_key"]
        }

        with open(self.liderdb_path, 'w') as f:
            json.dump(self.data, f, ensure_ascii=False)

        if self.data['location'] == 'remote':
            self.im.ssh_connect(self.data)
            self.im.install_mariadb(self.data)
            self.im.ssh_disconnect()
        else:
            self.im.install_mariadb(self.data)

    def ldap_install(self, server_data):
        print("*****OPENLDAP*****\n")

        if server_data["selection"] == "advanced":
            ip = server_data["OpenLDAP"][0]["ip"]
            username = server_data["OpenLDAP"][0]["username"]
            password = server_data["OpenLDAP"][0]["password"]
            location = server_data["OpenLDAP"][0]["location"]
            lider_server_addr = server_data["Lider"][0]["ip"]
        else:
            # selection is standart
            ip = server_data["ip"]
            username = server_data["username"]
            password = server_data["password"]
            location = server_data["location"]
            lider_server_addr = server_data["ip"]

        l_org_name = self.l_base_dn.split('.')
        l_org_name = l_org_name[0]

        self.data = {

            'location': location,
            # Server Configuration
            'ip': ip,
            'username': username,
            'password': password,

            # OpenLDAP Configuration
            'l_base_dn': self.l_base_dn,
            'l_config_pwd': self.l_admin_pwd,
            'l_org_name': l_org_name,
            'l_config_admin_dn': "cn=admin,cn=config",
            'l_admin_cn': 'admin',
            'ladmin_user': self.ladmin_user,
            'l_admin_pwd': self.l_admin_pwd,
            'ladmin_pwd': self.ladmin_pwd,
            'ldap_status': self.ldap_status,
            'repo_addr': server_data["repo_addr"],
            'repo_key': server_data["repo_key"],
            'lider_server_addr': lider_server_addr,
            'simple_ldap_user': "test_ldap_user",
            'simple_ldap_user_pwd': "secret"

            # yeni ldap kur ya da varolan ldapı konfigüre et 'new' ya da 'update' parametreleri alıyor
        }

        with open(self.liderldap_path, 'w') as f:
            json.dump(self.data, f, ensure_ascii=False)

        if self.data['location'] == 'remote':
            self.im.ssh_connect(self.data)
            self.im.install_ldap(self.data)
            self.im.ssh_disconnect()
        else:
            self.im.install_ldap(self.data)

    def ejabberd_install(self, server_data):

        print("*****XMPP*****\n")

        if server_data["selection"] == "advanced":
            ip = server_data["XMPP"][0]["ip"]
            username = server_data["XMPP"][0]["username"]
            password = server_data["XMPP"][0]["password"]
            location = server_data["XMPP"][0]["location"]
            self.ldap_server = server_data["OpenLDAP"][0]["ip"]
        else:
            # selection is standart
            ip = server_data["ip"]
            username = server_data["username"]
            password = server_data["password"]
            location = server_data["location"]
            self.ldap_server = server_data["ip"]

        ## Random Password Generator for "lider_sunucu"
        chars = string.ascii_letters + string.digits
        rnd = random.SystemRandom()
        self.lider_sunucu_pwd = ''.join(rnd.choice(chars) for i in range(10))

        self.data = {

            'location': location,
            # Server Configuration
            'ip': ip,
            'username': username,
            'password': password,
            # Ejabberd Configuration
            'e_service_name': "im.liderahenk.org",
            # 'e_service_name': self.e_service_name.text(),
            'e_username': 'admin',
            # 'e_user_pwd': self.ejabberd_layout.e_user_pwd.text(),
            'e_user_pwd': self.e_user_pwd,
            'e_hosts': ip,
            'ldap_servers': self.ldap_server,
            'l_base_dn': self.l_base_dn,

            # Lider Configuration
            'lider_username': 'lider_sunucu',
            'lider_user_pwd': self.lider_sunucu_pwd,
            'l_admin_pwd': self.l_admin_pwd,
            'repo_key': server_data["repo_key"],
            'repo_addr': server_data["repo_addr"]
        }

        with open(self.liderejabberd_path, 'w') as f:
            json.dump(self.data, f, ensure_ascii=False)

        if self.data['location'] == 'remote':
            self.im.ssh_connect(self.data)
            self.im.install_ejabberd(self.data)
            self.im.ssh_disconnect()
        else:
            self.im.install_ejabberd(self.data)

    def lider_install(self, server_data):

        print("*****LİDER*****\n")

        if server_data["selection"] == "advanced":
            ip = server_data["Lider"][0]["ip"]
            username = server_data["Lider"][0]["username"]
            password = server_data["Lider"][0]["password"]
            location = server_data["Lider"][0]["location"]
            self.ldap_server = server_data["OpenLDAP"][0]["ip"]
            self.db_server = server_data["Veritabanı"][0]["ip"]
            self.ejabberd_server = server_data["XMPP"][0]["ip"]
            if server_data["Veritabanı"][0]["ip"] == ip:
                self.db_server = "127.0.0.1"
            else:
                self.db_server = server_data["Veritabanı"][0]["ip"]

        else:
            # selection is standart
            ip = server_data["ip"]
            username = server_data["username"]
            password = server_data["password"]
            location = server_data["location"]
            self.ldap_server = server_data["ip"]
            self.db_server = server_data["ip"]
            self.ejabberd_server = server_data["ip"]
            self.db_server = "127.0.0.1"

        self.data = {
            'location': location,

            # Server Configuration
            'ip': ip,
            'username': username,
            'password': password,
            # Database Configuration
            'db_server': self.db_server,
            'db_name': "liderdb",
            'db_username': "root",
            'db_password': self.db_password,

            # Ejabberd Configuration
            'e_service_name': "im.liderahenk.org",
            'e_hosts': self.ejabberd_server,
            'lider_username': 'lider_sunucu',
            'lider_user_pwd': self.lider_sunucu_pwd,

            # OpenLDAP Configuration
            'l_base_dn':  self.l_base_dn ,
            'l_admin_cn': "admin",
            'l_admin_pwd': self.l_admin_pwd,
            'ldap_servers': self.ldap_server,

            # File Server Configuration
            'file_server': ip,
            'fs_username': username,
            'fs_username_pwd': password,
            'fs_plugin_path': '/home/{username}'.format(username=username),
            'fs_agreement_path': '/home/{username}'.format(username=username),
            'fs_agent_file_path': '/home/{username}'.format(username=username),

            # repository parameters
            'repo_key': server_data["repo_key"],
            'repo_addr': server_data["repo_addr"]
        }

        with open(self.lider_path, 'w') as f:
            json.dump(self.data, f, ensure_ascii=False)

        if self.data['location'] == 'remote':
            self.im.ssh_connect(self.data)
            self.im.install_lider(self.data)
            self.im.ssh_disconnect()
        else:
            self.im.install_lider(self.data)


        print(" Kurulum Tamamlandı ")