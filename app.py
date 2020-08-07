#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time : 2020/8/7 上午11:17
# @Author : 尹新
# @Site : 
# @File : app.py
# @Software: PyCharm
import argparse
import smtplib
from email.mime.text import MIMEText

from common import config, hlog


def send(title, text):
    message = MIMEText(text, 'plain', 'utf-8')
    message['Subject'] = title
    message['From'] = config.sender

    smtpObj = smtplib.SMTP()

    try:
        hlog.info('connect to %s:%s' % (config.mail_host, config.mail_port1))
        smtpObj.connect(config.mail_host, config.mail_port1)
    except smtplib.SMTPServerDisconnected as e:
        hlog.info(e)
        hlog.info('try another port')
        hlog.info('connect to %s:%s' % (config.mail_host, config.mail_port2))
        smtpObj.connect(config.mail_host, config.mail_port2)

    hlog.info('login with %s:%s' % (config.mail_user, config.mail_pass))
    smtpObj.login(config.mail_user, config.mail_pass)

    for receiver in config.receivers:
        message['To'] = receiver

        try:
            smtpObj.sendmail(
                config.sender, receiver, message.as_string())
            hlog.info('send success')
        except smtplib.SMTPException as e:
            hlog.error(e)

    smtpObj.quit()


def main():
    parser = argparse.ArgumentParser(prog='stupid-mail-client',
                                     description='简单的邮件发送客户端',
                                     usage='%(prog)s -m [message]')

    parser.add_argument('-t',
                        '--title',
                        help='邮件标题',
                        required=False,
                        dest='title')

    group = parser.add_mutually_exclusive_group()
    group.add_argument('-m',
                       '--message',
                       help='要发送的消息',
                       dest='message')

    group.add_argument('-f',
                       '--filename',
                       help='发送文件内容',
                       dest='filename')

    parser.add_argument('-v',
                        '--version',
                        help='显示版本信息',
                        action='version',
                        version='%(prog)s v1.0.0')

    args = parser.parse_args()

    text = None
    if args.message:
        text = args.message
    elif args.filename:
        with open(args.filename, 'r', encoding='utf8') as file:
            file_text = file.read()
        text = args.filename + '\n\n' + file_text

    if args.title:
        title = args.title
    else:
        title = '默认标题'

    send(title, text)


if __name__ == '__main__':
    main()
