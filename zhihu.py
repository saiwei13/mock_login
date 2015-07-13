import re
import requests
from mock_login.base_client import BaseClient

__author__ = 'chenwei'


class ZHIHU(BaseClient):
    '''
    模拟知乎登录
    '''
    def __init__(self,email,password):
        self.email = email
        self.password = password
        self.session = requests.session()
        self.index_url = 'http://www.zhihu.com/'
        self.sign_url = 'http://www.zhihu.com/login'

        self.config_section = 'zhihu'
        '''配置文件字段'''
        self.config_cookies = 'cookies'
        '''配置文件字段'''



    def sign_in(self):
        rsp = self.session.get(self.index_url)
        '''
        这里url如果写http://www.zhihu.com/login，后面请求post登录，后出现403错误
        b'<html><title>403: Forbidden</title><body>403: Forbidden</body></html>'
        '''
        # ''':type : requests.Response'''
        if rsp.status_code != 200:
            print('return =',rsp.status_code)
            return

        if '/logout' in rsp.text:
            print('sign_in()  亲,你已登录知乎')
            return;

        _xsrf = re.search(r'name="_xsrf" value="(.*)"',rsp.text).group(1)

        header = {
            'Accept': '*/*',
            'Origin': 'http://www.zhihu.com',
            'X-Requested-With': "XMLHttpRequest",
            'User-Agent': "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/41.0.2272.76 Chrome/41.0.2272.76 Safari/537.36",
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Referer': "http://www.zhihu.com/",
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'en-US,en;q=0.8,zh-CN;q=0.6,zh;q=0.4'
        }

        post_data={
                '_xsrf':_xsrf,
                'email': self.email,
                'password': self.password,
                'rememberme': 'y',
        }

        rsp = self.session.post(
            url=self.sign_url,
            data=post_data,
            headers=header,
        )
        ''':type : requests.Response'''

        print(rsp.status_code)
        if rsp.status_code != 200:
            print(rsp.content)
        else:
            ##{'r': 1, 'errcode': 269, 'msg': {'captcha': '请填写验证码'}}
            ## 我在chrome翻墙登知乎， 再用脚本模拟登录， ip发生变化， 很容易出现验证码问题
            print(rsp.json())

            if(rsp.json()['r']==1):
                print('登录失败',rsp.json())
                msg=rsp.json()['msg']
            else:
                print('登录成功')
                # dict_from_cookiejar
                # print(rsp.cookies)
                #
                # print(type(rsp.cookies))
                # print(type(self.session.cookies))
                #
                # d = dict_from_cookiejar(self.session.cookies)
                # print(d)

                self.save_cookies()

    def has_sign_in(self):
        rsp = self.session.get(self.index_url)
        return '/logout' in rsp.text

if __name__ == '__main__':

    from mock_login.utils import config_file
    import configparser
    cf = configparser.ConfigParser()
    cf.read(config_file)

    zhihu = ZHIHU(
        email=cf.get('zhihu','email'),
        password=cf.get('zhihu','password')
    )
    zhihu.load_cookies()

    zhihu.sign_in()