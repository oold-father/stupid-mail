#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time : 2020/8/7 上午11:17
# @Author : 尹新
# @Site : 
# @File : app.py
# @Software: PyCharm
import argparse
import smtplib
from email.header import Header
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pathlib import Path

from common import config, hlog


def send(title, text, att_map=None, receivers=None, name=None):

    name = name if name else config.sender
    message = MIMEMultipart()
    message['Subject'] = Header(title, 'utf-8')
    message['From'] = Header(name, 'utf-8')
    message.attach(MIMEText(text, 'plain', 'utf-8'))

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

    receivers = receivers if receivers else config.receivers

    for receiver in receivers:
        message['To'] = Header(receiver, 'utf-8')

        for filename, file in att_map.items():
            att = MIMEText(file, 'base64', 'utf-8')
            att["Content-Type"] = 'application/octet-stream'
            att["Content-Disposition"] = 'attachment; filename="%s"' % filename
            message.attach(att)

        try:
            smtpObj.sendmail(
                config.sender, receiver, message.as_string())
            hlog.info('send success')
        except smtplib.SMTPException as e:
            hlog.error(e)

    smtpObj.quit()


def read_file(filename):
    file = Path(filename)
    if not (file.exists() and file.is_file()):
        file.exists() and file.is_file()
        hlog.error('文件 %s 不存在' % filename)
        return None

    with file.open(mode='r', encoding='utf8') as file:
        file_text = file.read()

    return file_text


def handler(parser_args):

    text = None
    if parser_args.message:
        text = parser_args.message
    elif parser_args.filename:
        text = read_file(parser_args.filename)

    if parser_args.title:
        title = parser_args.title
    else:
        title = '默认标题'

    att_map = {}
    if parser_args.attachment:
        for att in parser_args.attachment:
            att_file = read_file(att)
            if att_file:
                att_map.update({att: att_file})

    send(title, text, att_map, parser_args.receivers, parser_args.name)


def main():
    parser = argparse.ArgumentParser(prog='stupid-mail-client',
                                     description='简单的邮件发送客户端',
                                     usage='%(prog)s -m [message]')

    parser.add_argument('-t',
                        '--title',
                        help='邮件标题',
                        required=False,
                        dest='title')

    parser.add_argument('-n',
                        '--name',
                        help='发件人姓名',
                        required=False,
                        dest='name')

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-m',
                       '--message',
                       help='要发送的消息',
                       dest='message')

    group.add_argument('-f',
                       '--filename',
                       help='发送文件内容',
                       dest='filename')

    parser.add_argument('-a',
                        '--attachment',
                        help='邮件附件',
                        nargs='+',
                        required=False,
                        dest='attachment')

    parser.add_argument('-r',
                        '--receivers',
                        help='邮件接收者',
                        nargs='+',
                        required=False,
                        dest='receivers')

    parser.add_argument('-v',
                        '--version',
                        help='显示版本信息',
                        action='version',
                        version='%(prog)s v1.0.0')

    args = parser.parse_args()

    handler(args)


if __name__ == '__main__':
    main()
