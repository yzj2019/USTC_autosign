'''读入yaml配置文件，连接并通过USTC统一身份认证'''
# !python3
# coding=UTF-8
import requests  # HTTP/HTTPS方便接口
import sys  # 系统调用
from urllib.parse import urlparse  # URL解析
import yaml  # python处理yaml文件
import json  # 用于处理json类型的返回数据
from MyHTMLParser import Parser_loginurl  # HTMLParser自定义解析器

debug = False


def getYmlConfig(yaml_file):
    '''获取配置数据'''
    file = open(yaml_file, 'r', encoding="utf-8")
    file_data = file.read()
    file.close()
    config = yaml.load(file_data, Loader=yaml.SafeLoader)
    return config




def conn_USTC(user):
    '''通过统一身份认证连接综合教务系统，并保持连接'''
    # 使用requests方法实现，https://blog.csdn.net/xc_zhou/article/details/81021496?utm_medium=distribute.pc_relevant_t0.none-task-blog-2%7Edefault%7EBlogCommendFromMachineLearnPai2%7Edefault-1.control&dist_request_id=&depth_1-utm_source=distribute.pc_relevant_t0.none-task-blog-2%7Edefault%7EBlogCommendFromMachineLearnPai2%7Edefault-1.control，https://blog.csdn.net/qq_37616069/article/details/80376776
    # https://www.jianshu.com/p/8cd6e9bc2680，先chrome开发者工具分析登录过程，再进行模仿
    # 也可考虑使用webdriver实现，见https://blog.csdn.net/Haven200/article/details/103208795
    user = user['user']
    # 首次访问，获取统一身份认证地址
    login_url = 'https://jw.ustc.edu.cn/login'
    print('connecting to %s ...' % login_url)
    res = requests.get(url=login_url)
    parser = Parser_loginurl()
    parser.feed(res.text)
    parser.close()
    print(parser.links[0])
    # 解析并生成下一个url
    urlparser = urlparse(login_url)
    host = urlparser.netloc
    ucaslogin_url = urlparser.scheme + '://' + host + parser.links[0]
    # print(ucaslogin_url)

    # 访问教务处与统一身份认证的接口，会自动重定向到统一身份认证地址
    session = requests.session()
    print('connecting to %s ...' % ucaslogin_url)
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7,ja-JP;q=0.6,ja;q=0.5',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36'
    }
    res = session.get(url=ucaslogin_url, headers=headers)
    print(res.cookies)

    # 建立统一身份认证连接，并保持连接
    # 登陆时提交表格用到这里的参数，是通过chrome开发者工具查看请求的模式并模仿
    headers['Referer'] = res.url
    headers['Cookie'] = 'JSESSIONID=' + res.cookies['JSESSIONID']
    params = {
        'model': 'uplogin.jsp',
        'service': '',
        'warn': '',
        'showCode': '',
        'username': user['username'],
        'password': user['password'],
        'button': ''
    }
    print('connecting to {0},{1},{2} ...'.format(res.url, user['username'], user['password']))
    res = session.post(url=res.url, data=params, headers=headers)
    # print(res.headers)
    # print(res.url) 
    # 验证登陆成功
    return session



def Query_grades(session):
    # 登陆成功，此时可以通过session来访问需要登录才能访问到的内容，因为cookies保持一致了
    # 此处以获取“我的成绩”为例，测试上面的连接是否成功
    headers = {
        'accept': 'application/json, text/plain, */*',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7,ja-JP;q=0.6,ja;q=0.5',
        'referer': 'https://jw.ustc.edu.cn/for-std/grade/sheet',
        'sec-ch-ua': '"Google Chrome";v="89", "Chromium";v="89", ";Not A Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36'
    }
    # 获取学期号
    res = session.get(url='https://jw.ustc.edu.cn/for-std/grade/sheet/getSemesters', headers=headers)
    # json转换：https://blog.csdn.net/qq_33232071/article/details/51026157
    semesters = json.loads(res.text)  # 进行json转换str到list类型，元素是dict类型
    print(semesters)
    # 获取学生受教育类型（此处是本科）
    res = session.get(url='https://jw.ustc.edu.cn/for-std/grade/sheet/getGradeSheetTypes', headers=headers)
    sheettypes = json.loads(res.text)
    # print(type(sheettypes))
    trainTypeId = str(sheettypes[0]['id'])
    semesterIds = []
    for semester in semesters:
        semesterIds.append(str(semester['id']))
    semesterIds.reverse()   # 逆序，依照上面开发者工具的结果
    print(trainTypeId)
    print(semesterIds)
    # 获取成绩：这里为什么不能显式地传参数，而必须将参数合并进url中？因为是get
    newurl = 'https://jw.ustc.edu.cn/for-std/grade/sheet/getGradeList' + '?' + 'trainTypeId=' + trainTypeId +'&semesterIds='
    for semesterId in semesterIds:
        newurl = newurl + semesterId + ','
    newurl = newurl[0:len(newurl)-1]
    print(newurl)
    res = session.get(url=newurl, headers=headers)   
    print(res.json())



if __name__ == "__main__":
    config = getYmlConfig('config.yml')
    users = config['users']
    for user in users:
        session = conn_USTC(user)
        Query_grades(session)
        

# https://jw.ustc.edu.cn/for-std/exam-arrange/info/24312
