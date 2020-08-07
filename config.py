#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time : 2020/8/7 上午11:18
# @Author : 尹新
# @Site : 
# @File : config
# @Software: PyCharm
from happy_python import HappyConfigBase


class Config(HappyConfigBase):
    """
    配置文件模板
    """

    def __init__(self):
        super().__init__()

        self.section = 'main'

        self.mail_host = ''
        self.mail_port1 = 465
        self.mail_port2 = 587
        self.mail_user = ''
        self.mail_pass = ''
        self.sender = ''
        self.receivers = []