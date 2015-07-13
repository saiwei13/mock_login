import configparser
from datetime import datetime,date
import random
import requests
from base_client import BaseClient

__author__ = 'chenwei'


##判断是否登陆

class Renren(BaseClient):
    def __init__(self,email,password):

        self.email = email
        self.password = password
        self.session = requests.session()

        self.index_url = 'http://www.renren.com/'
        self.sign_url = 'http://www.zhihu.com/login'
        self.encryptkey_url = 'http://login.renren.com/ajax/getEncryptKey'

        self.config_section = 'renren'
        '''配置文件字段'''
        self.config_cookies = 'cookies'
        '''配置文件字段'''

        print('email = %s , pwd=%s' %(email,password))

    def sign_in(self):
        pass

        self.load_cookies()

        # rsp = self.session.get(self.index_url)
        # # if '".*/login.js"' in rsp.text:
        # # if 'login.js' in rsp.text:      ##注意
        # # if '"login.js"' in rsp.text:
        #     print("未登陆")
        # else:
        #     print("已登陆")
        #
        # print(rsp.text)
        # print("跳转url=",rsp.url)

        # return
        import rsa

        key = self.getEncryptKey()
        print(key)

        header = {
            'Accept': '*/*',
            'Origin': 'http://www.renren.com',
            'X-Requested-With': "XMLHttpRequest",
            'User-Agent': "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/41.0.2272.76 Chrome/41.0.2272.76 Safari/537.36",
            'Content-Type': 'application/x-www-form-urlencoded',
            'Referer': "http://www.renren.com/",
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'en-US,en;q=0.8,zh-CN;q=0.6,zh;q=0.4'
        }

        post_data={
                'captcha_type': 'web_login',
                'domain': 'renren.com',
                'email': self.email,
                'key_id': '1',
                'origURL': 'http://www.renren.com/home',
                'password':rsa.encryptString(key['e'],key['n'],self.password),
                'rkey':key['rkey'],
        }

        #
        url = 'http://www.renren.com/ajaxLogin/login?1=1&uniqueTimestamp=%f' % random.random()

        rsp = self.session.post(
            url=url,
            data=post_data,
            headers=header,
        )
        ''':type : requests.Response'''
        print(rsp.status_code)
        print(rsp.json())
        if rsp.status_code == 200:
            if rsp.json()['code']:
                self.save_cookies();
        else:
            print(rsp.status_code)

    def getEncryptKey(self):
        print('getEncryptKey()')
        r = requests.get(self.encryptkey_url)
        ''':type r : requests.Response'''
        print (r.status_code)
        return r.json()

    def get_url(self):
        # http://www.renren.com/ajaxLogin/login?1=1&uniqueTimestamp=2015452252190
        now = datetime.now()
        year = now.year
        month = now.month-1
        day = now.weekday()+1
        if day == 7:
            day = 0;
        hour = now.hour
        second = now.second
        millsecond = round(now.microsecond/1000)

        url = "http://www.renren.com/ajaxLogin/login?1=1&uniqueTimestamp=%d%d%d%d%d%d" % (year,month,day,hour,second,millsecond);
        return url

if __name__ == '__main__':

    from utils import config_file

    cf = configparser.ConfigParser()
    cf.read(config_file)

    renren = Renren(
        email=cf.get('renren','email'),
        password=cf.get('renren','password')
    )
    renren.sign_in();