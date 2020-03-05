# encoding=utf-8

from autoSubmit import autoSubmit
from autoEmail import sendEmail

# 填用户名和密码
username = 'XXXXXXXXXX'
password = 'XXXXXXXXXX'


# 开启邮件服务的参数列表
smtp_host = 'smtp.163.com'         # 所选的第三方smtp服务的域名
smtp_user = 'XXXXXXXXXXX@163.com'  # 开启了smtp的邮箱账号
smtp_pass = 'XXXXXXXXX'            # 对应的密码

sender_email = smtp_user           # 发送者邮箱必须是开启了smtp的邮箱
recver_email = 'XXXXXXXXX@qq.com'  # 接受者邮箱


if __name__ == "__main__":
    try:
        res = autoSubmit(username, password)
        body = res
    except Exception as e:
        body = 'HTTP请求异常\n\n' + str(e)
    subject = 'i am ok自动上报反馈'
    sendEmail(smtp_host, smtp_user, smtp_pass, recver_email, subject, body)
