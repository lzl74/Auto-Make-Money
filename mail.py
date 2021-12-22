# -*- coding: UTF-8 -*- 
from apscheduler.schedulers.blocking import BlockingScheduler
from email import encoders
from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr
import time
import smtplib
import sys
import os


def _format_addr(s):
    name, addr = parseaddr(s)
    return formataddr((Header(name, 'utf-8').encode(), addr))


def push_mail():
    from_addr = 'xxxxxxx'
    password = 'xxxxxxx'
    to_addr = 'xxxxxxx'
    smtp_server = 'smtpdm.xxxxx.com'
    with open(r'C:\Users\luozh\Desktop\kzz\log.txt', 'r') as f:
        msg = MIMEText(f.read(), 'plain')
    msg['From'] = _format_addr('pc <%s>' % from_addr)
    msg['To'] = _format_addr('mailbox <%s>' % to_addr)
    msg['Subject'] = Header('可转债通知 '+time.strftime("%Y-%m-%d", time.localtime()), 'utf-8').encode()

    server = smtplib.SMTP(smtp_server, 25)
    server.set_debuglevel(1)
    server.login(from_addr, password)
    server.sendmail(from_addr, [to_addr], msg.as_string())
    server.quit()
    with open(r'C:\Users\luozh\Desktop\kzz\log.txt', 'w') as f:
        f.write("")


if __name__ == '__main__':
        push_mail()
