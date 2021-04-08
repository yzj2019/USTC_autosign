'''每日健康上报的连接模块'''
# !python3
# coding=UTF-8
import requests  # HTTP/HTTPS方便接口
# import sys  # 系统调用
# from urllib.parse import urlparse  # URL解析
# import json  # 用于处理json类型的返回数据
# 从单一文件ConnectToUSTC.py中引入依赖地方式
# from ConnectToUSTC import getYmlConfig, conn_USTC   # 连接USTC统一身份认证
from MyHTMLParser import Parser_lastdata    # 自定义HTML解析器

# https://weixine.ustc.edu.cn/2020/home

def USTC_dailysign(session, user):
    '''进行一次每日上报'''
    user = user['user']
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7,ja-JP;q=0.6,ja;q=0.5',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36',
        'referer': 'https://weixine.ustc.edu.cn/2020/login',
        'sec-ch-ua': '"Google Chrome";v="89", "Chromium";v="89", ";Not A Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
    }
    # 首次连接：相当于点击了“统一身份认证登录”，然后通过session内存的cookies自动通过统一身份认证，然后自动跳转到https://weixine.ustc.edu.cn/2020/home，返回的是首页的html信息
    login_url = 'https://weixine.ustc.edu.cn/2020/caslogin'
    print('connecting to %s ...' % login_url)
    res = session.get(url=login_url, headers=headers)
    # 解析html信息，获取上一次上报的地址、本次上报所需的token；故变更地址后只需要手动打卡一次，即可自动打卡
    parser = Parser_lastdata()
    parser.feed(res.text)
    parser.close()
    last_sign = parser.data
    # print(parser.data)
    # 二次连接：打卡
    sign_url = 'https://weixine.ustc.edu.cn/2020/daliy_report'
    headers['referer'] = 'https://weixine.ustc.edu.cn/2020/home'
    headers['origin'] = 'https://weixine.ustc.edu.cn'
    headers['cache-control'] = 'max-age=0'
    headers['content-length'] = '335'
    headers['content-type'] = 'application/x-www-form-urlencoded'
    params = {
        '_token': last_sign['_token'],
        'now_address': '1',
        'gps_now_address': '',
        'now_province': last_sign['now_province_hidden'],
        'gps_province': '',
        'now_city': last_sign['now_city_hidden'],
        'gps_city': '',
        'now_detail': '',
        'is_inschool': '',
        'body_condition': '1',
        'body_condition_detail': '',
        'now_status': '',
        'now_status_detail': '',
        'has_fever': '0',
        'last_touch_sars': '0',
        'last_touch_sars_date': '',
        'last_touch_sars_detail': '',
        'other_detail': '无'
    }
    # 如果在合肥，则'是否在校'=中区，'当前状态'=正常在校园内
    # 否则(校外，正常在家)
    # 具体接口可通过chrome开发者工具抓包获得
    if last_sign['now_province_hidden'] == '340000':
        params['is_inschool'] = '4'
        params['now_status'] = '1'
    else:
        params['is_inschool'] = '0'
        params['now_status'] = '2'
    res = session.post(url=sign_url, data=params, headers=headers)
    if (res.status_code == 200):
        print('Daily Sign OK')
    else:
        print('Daily Sign Failed')

'''if __name__ == "__main__":
    config = getYmlConfig('config.yml')
    users = config['users']
    for user in users:
        session = conn_USTC(user)
        USTC_dailysign(session, user)'''