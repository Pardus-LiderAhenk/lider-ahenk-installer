#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Author: Agah Hulusi OZ <enghulusi@gmail.com>

import os
import json
from getpass import getpass
from install_manager import InstallManager


class Settings():

    def __init__(self):
        super(Settings, self).__init__()
        self.im = InstallManager()
        self.liderahenk_data_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'dist/liderahenk.json')
        self.liderldap_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../dist/lider_ldap.json')
        self.server_list_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../dist/server_list_file.json')
        self.lider_ahenk = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../dist/lider_ahenk.json')
        if not os.path.exists(os.path.join(os.path.dirname(os.path.abspath(__file__)), '../dist')):
            os.makedirs(os.path.join(os.path.dirname(os.path.abspath(__file__)), '../dist'))

        self.ip = None
        self.username = None
        self.password = None
        self.repoaddress = None
        self.repo = None

    def settings(self):

        self.big_data = {}

        while(True):

            platform_options = input("Lider ahenk sunucu platform bilgileri Standart(S) veya Gelişmiş(G) :")

            if platform_options == "q" or platform_options == "Q":
                exit()


            if platform_options == "S" or platform_options == "s":
                print("****************************************")
                print("********Sunucu Erişim Bilgileri*********")
                print("****************************************")
                print("                  ")
                print("Kurulum 2 adımda gerçekleşir : ")
                print("-Birinci Adım : Bileşenlerin kurulacağı sunucu erişim bilgileri (Sunucu ip, Sunucu kullanıcı-adı, Sunucu parolası) girilir")
                print("-İkinci Adım : Lider Ahenk sunucu konfigürasyon bilgilerinin girilmesi")
                print("                  ")
                while (True):
                    while(True):
                        self.ip = input("Sunucu IP giriniz (192.168.*.*) : ")
                        if self.ip == "Q"  or self.ip == "q" :
                            exit()
                        elif self.ip != "" :
                            break
                    while (True):
                        self.username = input("Sunucu KULLANICI-ADI giriniz (lider) : ")
                        if self.username == "q" or self.username == "Q" :
                            exit()
                        elif self.username != "":
                            break
                    while (True):
                        self.password = getpass("Sunucu PAROLASI giriniz (****) : ")
                        if self.password =="q" or self.password == "Q" :
                            exit()
                        elif self.password != "":
                            break
                    while (True):
                        self.repo = input("Lütfen REPO tipi seçiniz Test(T) veya Stable(S) : ")
                        if self.repo == "t" or self.repo == "T":
                            self.repoaddress = "deb [arch=amd64] https://repo.liderahenk.org/liderahenk-test testing main"
                            break
                        elif self.repo == "S" or self.repo == "s":
                            self.repoaddress = "deb [arch=amd64] https://repo.liderahenk.org/liderahenk stable main"
                            break
                        elif self.repo == "Q" or self.repo == "q":
                            exit()
                    server_data = {
                        "selection" : "standart",
                        "ip" : self.ip,
                        "username" : self.username,
                        "password" : self.password,
                        "location" : "remote",
                        "repo_key": "https://repo.liderahenk.org/liderahenk-archive-keyring.asc",
                        "repo_addr": self.repoaddress,
                        "server_name": "all",
                    }

                    print("Bağlantı ayarları kontrol ediliyor Lütfen bekleyiniz...")

                    ssh_status = self.im.ssh_connect(server_data)
                    if ssh_status is True:
                        print("Bağlantı Başarılı. Kuruluma Devam Edebilirsiniz.")
                        self.big_data.update(server_data)
                        break
                    else:
                        print("Bağlantı Sağlanamadı. Bağlantı Ayarlarını Kontrol Ederek Daha Sonra Tekrar Deneyiniz!\n")
                        continue
                break


            elif platform_options == "G" or platform_options == "g":
                flag = ["Veritabanı", "OpenLDAP", "XMPP", "Lider"]
                print("****************************************")
                print("********Sunucu Erişim Bilgileri*********")
                print("****************************************")
                print("                  ")
                print("Kurulum 2 adımda gerçekleşir : ")
                print("-Birinci Adım : Bileşenlerin kurulacağı sunucu erişim bilgileri girilir")
                print("-İkinci Adım : Lider Ahenk sunucu konfigürasyon bilgilerinin girilmesi")
                print("                  ")


                print("====>>>>VERİTABANI Bilgilerini giriniz : ")
                while(True):
                    while(True):
                        self.ip = input("Sunucu IP giriniz (192.168.*.*) : ")
                        if self.ip == "q" or self.ip == " Q":
                            exit()
                        elif self.ip != "":
                            break
                    while(True):
                        self.username = input("KULLANICI-ADI giriniz (lider) : ")
                        if self.username == "Q" or self.username == " q" :
                            exit()
                        elif self.username != "":
                            break
                    while(True):
                        self.password = getpass("KULLANICI PAROLASI giriniz (****) : ")
                        if self.password == " q" or self.password == "Q":
                            exit()
                        elif self.password != "":
                            break

                    if self.username != "" and self.password != "" and self.ip != "" :
                        self.server_data = {
                            "Veritabanı":
                                [{  "username": self.username,
                                    "password": self.password,
                                    "ip": self.ip,
                                    "server_name": "Veritabanı",
                                    "location": "remote"
                                }]
                        }
                        self.big_data.update(self.server_data)
                        print("****************************************************")
                        print("")
                        data = {
                            'location': "remote",
                            # Server Configuration
                            'ip': self.ip,
                            'username': self.username,
                            'password': self.password,
                        }
                        ssh_status = self.im.ssh_connect(data)
                        if ssh_status is True:
                            print("Bağlantı Başarılı. Kuruluma Devam Edebilirsiniz.")
                            self.big_data.update(self.server_data)
                            break
                        else:
                            print(
                                "Bağlantı Sağlanamadı. Bağlantı Ayarlarını Kontrol Ederek Daha Sonra Tekrar Deneyiniz!\n")
                            continue


                    break
                        # else:
                        #     print("Veritabanı Bilgilerini Yanlış veya Eksik girdiniz !!! ")

                print("====>>>>OPENLDAP Bilgilerini giriniz : ")
                while (True):
                    while (True):
                        self.ip = input("Sunucu IP giriniz (192.168.*.*) : ")
                        if self.ip == "q" or self.ip == " Q":
                            exit()
                        elif self.ip != "":
                            break
                    while (True):
                        self.username = input("KULLANICI-ADI giriniz (lider) : ")
                        if self.username == "Q" or self.username == " q" :
                            exit()
                        elif self.username != "":
                            break
                    while (True):
                        self.password = getpass("KULLANICI PAROLASI giriniz (****) : ")
                        if self.password == " q" or self.password == "Q":
                            exit()
                        elif self.password != "":
                            break

                    if self.username != "" and self.password != "" and self.ip != "":
                        self.server_data = {
                            "OpenLDAP":
                                [{"username": self.username,
                                  "password": self.password,
                                  "ip": self.ip,
                                  "server_name": "Veritabanı",
                                  "location": "remote"
                                  }]
                        }
                        self.big_data.update(self.server_data)

                        print("****************************************************")
                        print(" ")
                        data = {
                            'location': "remote",
                            # Server Configuration
                            'ip': self.ip,
                            'username': self.username,
                            'password': self.password,
                        }
                        ssh_status = self.im.ssh_connect(data)
                        if ssh_status is True:
                            print("Bağlantı Başarılı. Kuruluma Devam Edebilirsiniz.")
                            self.big_data.update(self.server_data)
                            break
                        else:
                            print(
                                "Bağlantı Sağlanamadı. Bağlantı Ayarlarını Kontrol Ederek Daha Sonra Tekrar Deneyiniz!\n")
                            continue
                    break
                    # else:
                    #     print("OpenLDAP Bilgilerini Yanlış veya Eksik girdiniz !!! ")

                print("====>>>>XMPP Bilgilerini giriniz : ")
                while (True):
                    while (True):
                        self.ip = input("Sunucu IP giriniz (192.168.*.*) : ")
                        if self.ip == "q" or self.ip == " Q":
                            exit()
                        elif self.ip != "":
                            break
                    while (True):
                        self.username = input("KULLANICI-ADI giriniz (lider) : ")
                        if self.username == "Q" or self.username == " q" :
                            exit()
                        elif self.username != "":
                            break
                    while (True):
                        self.password = getpass("KULLANICI PAROLASI giriniz (****) : ")
                        if self.password == " q" or self.password == "Q":
                            exit()
                        elif self.password != "":
                            break

                    if self.username != "" and self.password != "" and self.ip != "":
                        self.server_data = {
                            "XMPP":
                                [{"username": self.username,
                                  "password": self.password,
                                  "ip": self.ip,
                                  "server_name": "Veritabanı",
                                  "location": "remote"
                                  }]
                        }
                        self.big_data.update(self.server_data)
                        print("****************************************************")
                        print("")
                        data = {
                            'location': "remote",
                            # Server Configuration
                            'ip': self.ip,
                            'username': self.username,
                            'password': self.password,
                        }
                        ssh_status = self.im.ssh_connect(data)
                        if ssh_status is True:
                            print("Bağlantı Başarılı. Kuruluma Devam Edebilirsiniz.")
                            self.big_data.update(self.server_data)
                            break
                        else:
                            print(
                                "Bağlantı Sağlanamadı. Bağlantı Ayarlarını Kontrol Ederek Daha Sonra Tekrar Deneyiniz!\n")
                            continue
                    break
                    # else:
                    #     print("XMPP Bilgilerini Yanlış veya Eksik girdiniz !!! ")

                print("====>>>>LİDER Bilgilerini giriniz : ")
                while (True):
                    while (True):
                        self.ip = input("Sunucu IP giriniz (192.168.*.*) : ")
                        if self.ip == "q" or self.ip == " Q":
                            exit()
                        elif self.ip != "":
                            break
                    while (True):
                        self.username = input("KULLANICI-ADI giriniz (lider) : ")
                        if self.username == "Q" or self.username == " q" :
                            exit()
                        elif self.username != "":
                            break
                    while (True):
                        self.password = getpass("KULLANICI PAROLASI giriniz (****) : ")
                        if self.password == " q" or self.password == "Q":
                            exit()
                        elif self.password != "":
                            break

                    if self.username != "" and self.password != "" and self.ip != "":
                        self.server_data = {
                            "Lider":
                                [{"username": self.username,
                                  "password": self.password,
                                  "ip": self.ip,
                                  "server_name": "Veritabanı",
                                  "location": "remote"
                                  }]
                        }
                        self.big_data.update(self.server_data)
                        print("****************************************************")
                        print("")
                        data = {
                            'location': "remote",
                            # Server Configuration
                            'ip': self.ip,
                            'username': self.username,
                            'password': self.password,
                        }
                        ssh_status = self.im.ssh_connect(data)
                        if ssh_status is True:
                            print("Bağlantı Başarılı. Kuruluma Devam Edebilirsiniz.")
                            self.big_data.update(self.server_data)
                            break
                        else:
                            print(
                                "Bağlantı Sağlanamadı. Bağlantı Ayarlarını Kontrol Ederek Daha Sonra Tekrar Deneyiniz!\n")
                            continue
                    break
                    # else:
                    #     print("Lider Bilgilerini Yanlış veya Eksik girdiniz !!! ")

                while (True):
                    self.repo = input("Lütfen REPO tipi seçiniz Test(T) veya Stable(S) : ")
                    if self.repo == "t" or self.repo == "T":
                        self.repoaddress = "deb [arch=amd64] http://repo.liderahenk.org/liderahenk-test testing main"
                        break
                    elif self.repo == "S" or self.repo == "s":
                        self.repoaddress = "deb [arch=amd64] http://repo.liderahenk.org/liderahenk stable main"
                        break
                    elif self.repo == "Q" or self.repo == "q":
                        exit()

                self.repo_data = {
                    "selection": "advanced",
                    "repo_key": "http://repo.liderahenk.org/liderahenk-archive-keyring.asc",
                    "repo_addr": self.repoaddress
                }
                self.big_data.update(self.repo_data)

                break

            else:
                print("Lütfen tekrar seçim yapınız !!! ")

        with open(self.server_list_file, 'w') as json_file:
            json.dump(self.big_data, json_file)
