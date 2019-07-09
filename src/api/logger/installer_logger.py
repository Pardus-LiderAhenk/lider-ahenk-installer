#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Author: Tuncay ÇOLAK <tuncay.colak@tubitak.gov.tr>

import logging
import logging.config
import os
from inspect import getframeinfo, stack

class Logger(object):

    def __init__(self):
        super(Logger, self).__init__()
        if not os.path.exists(os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../dist')):
            os.makedirs(os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../dist'))

        self.log_out_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../dist/installer.log')
        self.log_conf_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../conf/log.conf')

    def info(self, message):
        caller = getframeinfo(stack()[1][0])
        filename = self.get_log_header(caller.filename)
        # logging.basicConfig(filename=self.log_out_path, filemode='a',  level=logging.INFO, datefmt='%m/%d/%Y %I:%M:%S %p', format='%(asctime)s %(levelname)s [Lider Ahenk Installer] [' + str(filename)+': ' + str(caller.lineno)+'] %(message)s ')
        logging.basicConfig(filename=self.log_out_path, filemode='a',  level=logging.INFO, datefmt='%m/%d/%Y %I:%M:%S %p', format='%(asctime)s %(levelname)s [Lider Ahenk Installer] %(message)s ')
        logging.info(message)

    def debug(self, message):
        caller = getframeinfo(stack()[1][0])
        filename = self.get_log_header( caller.filename )
        logging.basicConfig(filename=self.log_out_path, filemode='a', level=logging.DEBUG, datefmt='%m/%d/%Y %I:%M:%S %p', format='%(asctime)s %(levelname)s [Lider Ahenk Installer] %(message)s ')
        logging.debug(message)

    def warning(self, message):
        caller = getframeinfo(stack()[1][0])
        filename = self.get_log_header(caller.filename)
        logging.basicConfig(filename=self.log_out_path, filemode='a', level=logging.WARNING, datefmt='%m/%d/%Y %I:%M:%S %p', format='%(asctime)s %(levelname)s [Lider Ahenk Installer] %(message)s ')
        logging.warning(message)

    def error(self, message):
        caller = getframeinfo(stack()[1][0])
        filename = self.get_log_header(caller.filename)
        lider_error_no = caller.lineno
        # print(caller.filename, lider_error_no)
        logging.basicConfig(filename=self.log_out_path, filemode='a', level=logging.ERROR, datefmt='%m/%d/%Y %I:%M:%S %p', format='%(asctime)s %(levelname)s [Lider Ahenk Installer] %(message)s ')
        logging.error(message)

    def get_log_header(self, file_path):

        if file_path is not None:
            name_list = file_path.split('/')
            result = ''
            if len(name_list) > 1:
                result = str(name_list[len(name_list) - 2]).upper() + ' >> ' + name_list[len(name_list) - 1]
            return result

        else:
            return None
