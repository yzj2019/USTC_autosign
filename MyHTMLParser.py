# !python3
# coding=UTF-8
from html.parser import HTMLParser

# 把HTMLParser向上封装一层，详见https://www.cnblogs.com/zhanghaohong/p/4562127.html
class Parser_loginurl(HTMLParser):
    '''分离出统一身份认证地址'''
    def __init__(self):
        HTMLParser.__init__(self)
        self.data = []  # 定义data数组用来存储html中的数据
        self.links = []

    def handle_starttag(self, tag, attrs):
        # print('<%s>' % tag)
        if tag == 'a':
            if len(attrs) == 0:
                pass
            else:
                tag = False
                for (Name, Value) in attrs:
                    if Name == 'id':
                        # 获取统一身份认证接口
                        if Value == 'login-unified-wrapper':
                            tag = True
                    if Name == 'href':
                        if tag == True:
                            self.links.append(Value)
    """
    def handle_endtag(self, tag):
        print('<%s>' % tag)

    def handle_startendtag(self, tag, attrs):
        print('<%s>' % tag)

    def handle_data(self, data):
        print('data===>', data)

    def handle_comment(self, data):
        print('<!--', data, '-->')

    def handle_entityref(self, name):
        print("&%s;" % name)

    def handle_charref(self, name):
        print('&#%s;' % name)


if __name__ == "__main__":
    html_code = '''<html>
        <head>这是头标签</head>
        <body>
            <!--test html parser-->
            <p>Some <a type="button" id="login-unified-wrapper" href="/ucas-sso/login">html</a> HTML&nbsp;&#1234; ...<br>END</p>
        </body ></html>'''
    parser = MyHTMLParser()
    parser.feed(html_code)
    parser.close()
    print(parser.data)
    print(parser.links)
"""

class Parser_lastdata(HTMLParser):
    '''分离出本次健康打卡所需的数据: _token, '''
    def __init__(self):
        HTMLParser.__init__(self)
        self.data = {}  # 定义data数组用来存储html中的数据
    
    def handle_starttag(self, tag, attrs):
        if tag == 'input':
            '''print('<%s>' % tag)
            print(attrs)'''
            if len(attrs) == 0:
                pass
            elif len(attrs) == 3:
                tag = False
                for (Name, Value) in attrs:
                    if Name == 'type' and Value == 'hidden':
                        tag = True
                if tag == True:
                    name = attrs[1][1]
                    value = attrs[2][1]
                    self.data[name] = value