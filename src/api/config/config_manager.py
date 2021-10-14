#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Author: Tuncay ÇOLAK <tuncay.colak@tubitak.gov.tr>

import configparser
import os
from datetime import datetime
from api.logger.installer_logger import Logger

class ConfigManager(object):

    """
    method reading and writing from the configuration file
    """
    def __init__(self):
        self.logger = Logger()
        self.config = configparser.ConfigParser()
        self.installer_config_path2 = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../conf/installer.conf' )
        if not os.path.exists(os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../dist')):
            os.makedirs(os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../dist'))

    def read(self):
        try:
            self.config.read(self.installer_config_path2, encoding="utf-8")
            config = self.config["COMMANDS"]
            return config
        except Exception as e:
            self.logger.error("Veriler okunurken hata oluştu: " + str(e))
            return None

    def replace_all(self, text, dic):
        try:
            for i, j in dic.items():
                text = text.replace(i, j)
            self.logger.info("Dosya güncellenmesi başarıyla tamamlandı")
            return text
        except Exception as e:
            self.logger.error("Dosya güncellenmesi sırasında beklenmedik bir hata ile karşılaşıldı\n" + str(e))

    def date_format(self):
        date_now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        date_parse = date_now.split(" ")
        date_list = []
        for line in date_parse:
            date_line = line + "-"
            date_list.append(date_line)
        date = ''.join(str(x) for x in date_list)
        date = date.strip('-')
        return date