# encoding=utf-8

import smtplib
from email.mime.text import MIMEText
from email.header import Header

'''
用于触发邮件发送
'''


def sendEmail(smtp_host, smtp_user, smtp_pass, recver_email, subject, body):
    message = MIMEText(body, 'plain', 'utf-8')
    message['From'] = smtp_user     # 发送者
    message['To'] = recver_email         # 接收者
    message['Subject'] = Header(subject, 'utf-8')
    try:
        smtpObj = smtplib.SMTP_SSL(smtp_host, 465)
        smtpObj.login(smtp_user, smtp_pass)
        smtpObj.sendmail(smtp_user, [recver_email], message.as_string())
        print("邮件发送成功")
    except smtplib.SMTPException as e:
        print("Error: 无法发送邮件", e)
