'''自动打卡的webdriver实现'''
# !python3
# coding=UTF-8
import sys      # 系统调用
import os       # 用于获取脚本的绝对路径
import yaml     # python处理yaml文件
from selenium import webdriver                          # 浏览器驱动程序
from selenium.webdriver.chrome.options import Options   # 选项


def getYmlConfig(yaml_file):
    '''获取配置数据'''
    file = open(yaml_file, 'r', encoding="utf-8")
    file_data = file.read()
    file.close()
    config = yaml.load(file_data, Loader=yaml.SafeLoader)
    return config


class USTC_autosign(object):
    '''USTC自动打卡的webdriver类'''
    def __init__(self):
        self.users = []
        abs_file = os.path.abspath(sys.argv[0])
        abs_dir = abs_file[:abs_file.rfind("/")]    # 父文件夹绝对路径
        config = getYmlConfig(abs_dir + '/config.yml')
        users = config['users']
        for user in users:
            # 通过yaml文件构建用户的用户名密码list(dict)
            self.users.append(list(user.values())[0])
    
    def get_driver(self):
        '''获取浏览器对象'''
        chrome_options = Options()
        chrome_options.add_argument('lang=zh_CN.UTF-8')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('blink-settings=imagesEnabled=false')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('user-agent="Mozilla/5.0 (iPod; U; CPU iPhone OS 2_1 like Mac OS X; ja-jp) AppleWebKit/525.18.1 (KHTML, like Gecko) Version/3.1.1 Mobile/5F137 Safari/525.20"')
        driver = webdriver.Chrome(options=chrome_options)       #创建浏览器对象
        return driver


    def conn_USTC(self, user):
        '''通过单用户的统一身份认证，并返回浏览器对象'''
        login_url = 'https://jw.ustc.edu.cn/login'
        print('connecting to %s ...' % login_url)
        driver = self.get_driver()
        driver.get(login_url)
        driver.find_element_by_id('login-unified-wrapper').click()
        driver.
        driver.find_element_by_id('login').click()

        return driver


    def test(self):
        '''测试用'''
        for user in self.users:
            self.conn_USTC(user)



if __name__ == "__main__":
    my = USTC_autosign()
    my.test()