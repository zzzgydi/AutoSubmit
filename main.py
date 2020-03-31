# encoding=utf-8

import time
import configparser
from autopy.autoSubmit import autoSubmit
from autopy.autoEmail import sendEmail
from os import getcwd, path, listdir


# 获取config目录下所有配置文件
def getAllConf():
    cwd = getcwd()
    configPath = path.join(cwd, 'config')
    return [path.join(configPath, f)
            for f in listdir(configPath) if f.endswith('.conf') and
            path.isfile(path.join(configPath, f))]


def runTask(conf):
    config = configparser.ConfigParser()
    config.read(conf)
    label = config['scut']['label']
    username = config['scut']['username']
    password = config['scut']['password']
    smtp_host = config['email']['host']   # 所选的第三方smtp服务的域名
    smtp_user = config['email']['user']   # 开启了smtp的邮箱账号
    smtp_pass = config['email']['pass']   # 对应的密码
    sender_email = smtp_user                    # 发送者邮箱必须是开启了smtp的邮箱
    recver_email = config['email']['recver']    # 接受者邮箱

    print(time.strftime(r"%Y-%m-%d %H:%M:%S"))
    errors = []
    for i in range(10):
        status, msg = autoSubmit(username, password)
        result = '成功' if status == 0 else '失败'
        errors.append("# 第{}次上报\t[{}]\n{}".format(i + 1, result, msg))
        if status == 0:
            break
        else:
            time.sleep(5)
    # 构造邮件信息
    body = "Label - {}\n{}".format(label, "\n\n".join(errors))
    subject = 'i am ok自动上报反馈'
    sendEmail(smtp_host, smtp_user, smtp_pass, recver_email, subject, body)


if __name__ == "__main__":
    for conf in getAllConf():
        runTask(conf)
