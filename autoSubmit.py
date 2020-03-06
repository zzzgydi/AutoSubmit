# encoding=utf-8

import requests
from bs4 import BeautifulSoup as bf
import json
import subprocess


common_header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36',
}


class _Http:
    def __init__(self):
        self.request = requests.Session()

    def get(self, url, headers={}, cookies={}):
        for h in common_header:
            headers[h] = common_header[h]
        return self.request.get(url, headers=headers, cookies=cookies, allow_redirects=False)
        # return request.get(url, headers=headers, cookies=cookies, verify=False, allow_redirects=False)

    def post(self, url, headers={}, cookies={}, data={}):
        for h in common_header:
            headers[h] = common_header[h]
        return self.request.post(url, data=data, headers=headers, cookies=cookies, allow_redirects=False)
        # return request.post(url, data=data, headers=headers, cookies=cookies, verify=False, allow_redirects=False)


# 自动上报
def autoSubmit(username, password):
    http = _Http()
    # 第一次登录 - 获取官网页面
    url_1 = 'https://sso.scut.edu.cn/cas/login?service=https%3A%2F%2Fiamok.scut.edu.cn%2Fcas%2Flogin'
    response = http.get(url_1)
    cookies_1 = response.cookies
    html = response.text

    # 解析页面 - 获取参数加密
    bs = bf(html, "html.parser")
    lt = bs.select('#lt')[0]['value']
    execution = bs.select('input[name="execution"]')[0]['value']
    _eventId = bs.select('input[name="_eventId"]')[0]['value']
    rsa = username + password + lt
    cmds = ['node', './script/main.js', rsa]
    p = subprocess.run(cmds, stdout=subprocess.PIPE)

    # 构造登录请求参数
    form_data = {
        'rsa': p.stdout.decode('utf-8').strip(),
        'ul': len(username),
        'pl': len(password),
        'lt': lt,
        'execution': execution,
        '_eventId': _eventId,
    }

    if len(form_data['rsa']) < 1:
        print('Node模块调用出现问题')
        return 'Node模块调用出现问题'

    # 第二次登录
    post_header = {'Content-Type': 'application/x-www-form-urlencoded'}
    response = http.post(url_1, data=form_data,
                         headers=post_header, cookies=cookies_1)
    cookies_2 = response.cookies
    location = response.headers.get('Location')  # 第三次登录地址

    if not location:
        print('登录失败，账号或密码有误')
        return '登录失败，账号或密码有误'

    # 第三次登录
    response = http.get(location, cookies=cookies_1)
    cookies_3 = response.cookies
    jsessionid = cookies_3.get('JSESSIONID')

    # 第四次登录
    login_url = 'https://iamok.scut.edu.cn/cas/login'
    response = http.get(login_url, cookies=cookies_3)
    cookies_4 = response.cookies
    code = cookies_4.get('code')

    # 构造有用的cookies
    cookies = {
        'JSESSIONID': jsessionid,
        'code': code
    }

    # 请求用户数据
    get_data_url = 'https://iamok.scut.edu.cn/mobile/recordPerDay/getRecordPerDay'
    response = http.get(get_data_url, cookies=cookies)
    data = response.json()['data']  # 用户以往的数据

    '''
    这里可以在data中修改数据
    '''

    # 一键上报
    post_data_url = 'https://iamok.scut.edu.cn/mobile/recordPerDay/submitRecordPerDay'
    post_header = {
        'Content-Type': 'application/json;charset=UTF-8'
    }
    response = http.post(post_data_url, data=json.dumps(data),
                         headers=post_header, cookies=cookies)

    status_code = response.json()['code']
    if status_code != '200' and status_code != 200:
        print('上报失败')
        # print(response.json())
        return '上报失败'
    else:
        print('上报成功')
        return '上报成功'
