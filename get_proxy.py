# coding:utf-8


import json
import telnetlib
import requests
import random

proxy_url = 'https://raw.githubusercontent.com/fate0/proxylist/master/proxy.list'
# proxyList = []

#定义函数,验证代理ip是否有效
def verify(ip,port,type):
    proxies = {}
    try:
        telnet = telnetlib.Telnet(ip,port=port,timeout=3)  #用这个ip请访问，3s自动断开，返回tiemout
    except:
        print('unconnected')
    else:
        #print('connected successfully')
        # proxyList.append((ip + ':' + str(port),type))
        proxies['type'] = type
        proxies['host'] = ip
        proxies['port'] = port
        proxiesJson = json.dumps(proxies)
        #保存到本地的proxies_ip.json文件
        with open('./proxies_ip.json','a+') as f:
            f.write(proxiesJson + '\n')
        print("已写入：%s" % proxies)

#定义函数，带着url地址去获取数据
def getProxy(proxy_url):
    response = requests.get(proxy_url)
    #print(type(response))
    # 用split('\n') 将每一行分割之后组成的列表，消除换行影响
    proxies_list = response.text.split('\n')
    for proxy_str in proxies_list:
        # 用json.loads()方法，将每一行的字符串转换为json对象，最后取值
        proxy_json = json.loads(proxy_str)
        host = proxy_json['host']
        port = proxy_json['port']
        type = proxy_json['type']
        verify(host,port,type)


#主函数，入口
if __name__ == '__main__':
    getProxy(proxy_url)