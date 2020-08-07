#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time : 2020/8/7 上午11:17
# @Author : 尹新
# @Site : 
# @File : common
# @Software: PyCharm
from pathlib import PurePath

from happy_python import HappyConfigParser, HappyLog

from config import Config

CONFIG_DIR = PurePath(__file__).parent / 'resource'
CONFIG_FILENAME = str(CONFIG_DIR / 'default.ini')
LOG_CONFIG_FILENAME = str(CONFIG_DIR / 'log.ini')

config = Config()
HappyConfigParser.load(CONFIG_FILENAME, config)

hlog = HappyLog.get_instance(LOG_CONFIG_FILENAME)