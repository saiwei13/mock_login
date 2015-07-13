import re
from requests.utils import dict_from_cookiejar

__author__ = 'chenwei'

import configparser
from datetime import datetime,date

import random
import requests
from base_client import BaseClient
import utils



##err_no   0：登录成功　　，　　４：密码错误，　　６：验证码错误　　　527:请输入验证码　　　


class Baidu(BaseClient):
    '''
    https://passport.baidu.com/center?_t=1431325161
    可以去这个链接查询登录历史
    '''

    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.session = requests.session()

        # https://ss0.bdstatic.com/5LMZfyabBhJ3otebn9fN2DJv/passApi/js/login_tangram_f2e986d5.js


        # self.index_url = 'https://www.baidu.com/'

        # href="https://passport.baidu.com/v2/?login&tpl=mn&u=http%3A%2F%2Fwww.baidu.com%2F"
        # https://www.baidu.com/   主页
        # #https://passport.baidu.com/v2/?login　　　登录界面
        # get token
        # https://passport.baidu.com/v2/api/?getapi&tpl=pp&apiver=v3&tt=1431305718340&class=login&logintype=basicLogin&callback=bd__cbs__k7txq4

        ##
        ##要先访问主页，自动保存cookies ，再访问sign_url　才能显示页面内容
        self.sign_url = 'https://passport.baidu.com/v2/api/?login'
        # self.mission_url = 'http://v2ex.com/mission/daily'

        self.config_section = 'baidu'
        '''配置文件字段'''
        self.config_cookies = 'cookies'
        '''配置文件字段'''

        self.tt = utils.timestamp();


    def has_sign_in(self):
        '''检查是否已经登录'''

        rsp = self.session.get('http://www.baidu.com')
        ''':type : requests.Response'''

        # print(rsp.text)

        if '登录' in rsp.text:
            print("not login!")
            return False
        else :
            print("alread login!")
            return True

        # rsp = self.session.get("http://pan.baidu.com/api/account/thirdinfo")
        # ''':type : requests.Response'''
        # if rsp.json()['errno'] == 0:
        #     print("Login check success!")
        #     return True
        # else :
        #     print("not login!")
        #     return False

    def get_token(self,tt):
        '''获取token'''
        # ret = self.session.get("http://www.baidu.com/")
        url="https://passport.baidu.com/v2/api/?getapi&tpl=pp&apiver=v3&tt=%s&class=login&logintype=dialogLogin"  % str(tt);
        rsp = self.session.get(url)
        match = re.search(u'"token" : "(?P<tokenVal>.*?)"',rsp.text)
        token = match.group('tokenVal')
        return token

    def get_verifycode(self, code_string):
        '''
        获取验证码
        '''
        url = "https://passport.baidu.com/cgi-bin/genimage?" + code_string
        print(url)

        rsp = self.session.get(url)
        ''':type : requests.Response'''
        path = 'code.jpg'

        if rsp.status_code == 200:
                with open(path,'wb') as f:
                    for chunk in rsp.iter_content():
                        f.write(chunk)
                    f.flush();


        import time
        time.sleep(1)

        code = input("Please input verifycode >")
        return code

    #
    # def get_verifycode(self):
    #     '''获取验证码 , 有时候出现，有时候不出现'''
    #     # https://passport.baidu.com/v2/api/?logincheck&amp;token=15577c57bccc357490af640d58273808&amp;tpl=pp&amp;apiver=v3&amp;tt=1431325125972&amp;username=a6377508&amp;isphone=false&amp;callback=bd__cbs__qfgjng"></script>
    #     pass
    #     # params = dict(token=token,
    #     #               tpl="netdisk",
    #     #               apiver="v3",
    #     #               tt=utils.timestamp(),
    #     #               username=self.username,
    #     #               isphone="false")
    #     # check_login_url = "https://passport.baidu.com/v2/api/?logincheck&" + urllib.urlencode(params)
    #     # ret = self.api_request(check_login_url)
    #     # code_string =  ret["data"]["codeString"]
    #     #
    #     # if code_string:
    #     #     logger.debug("Login check require verifycode")
    #     #     verifycode = self.get_verifycode(code_string)
    #     # else:
    #     #     verifycode = ""
    #
    #
    #     check_login_url ='https://passport.baidu.com/v2/api/?logincheck&amp;token=%s&amp;tpl=pp&amp;apiver=v3&amp;tt=%s&amp;username=a6377508&amp;isphone=false&amp;callback=bd__cbs__qfgjng'


    def get_post_data(self,tt,token,codeString,verifycode):
        post_data={
            'apiver': 'v3',
            # 'callback': 'parent.bd__pcbs__gsd1lq',
            # 'charset': 'UTF-8',
            'codestring': codeString,
            # 'crypttype': '12',
            # 'idc':'',
            'isPhone':'',
            'logLoginType':' pc_loginDialog',
            'loginmerge': 'true',
            'logintype': 'dialogLogin',
            'mem_pass': 'on',
            # 'rsakey': 'hWyCfSdv6iAMWmv2xhdrOqtQNxr1W0Pp',
            'password': self.password,
            'ppui_logintime': '5452',
            'quick_user': '0',
            'safeflg': '0',
            'splogin': 'newuser',
            'staticpage': 'https://www.baidu.com/cache/user/html/v3Jump.html',
            # 'subpro':'',
            'token': token,
            'tpl': 'mn',
            'tt': str(utils.timestamp()),
            'u': 'https://www.baidu.com/',
            'username': self.username,
            'verifycode':verifycode,
        }

        return post_data

    def sign_in(self):

        if self.has_sign_in():
            print('return')
            return;

        self.tt = utils.timestamp();

        # rsp = self.session.get('https://passport.baidu.com/v2/?login&tpl=mn&u=http%3A%2F%2Fwww.baidu.com%2F')
        # rsp = self.session.get('https://passport.baidu.com/v2/?login')


        token = self.get_token(utils.timestamp());
        print('token=',token)

        #构造包的头部
        header = {
            "User-Agent":"Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:27.0) Gecko/20100101 Firefox/27.0",
            # 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            # 'Origin': 'https://www.baidu.com',
            # 'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/41.0.2272.76 Chrome/41.0.2272.76 Safari/537.36',
            # 'Content-Type': 'application/x-www-form-urlencoded',
            # 'Referer': 'https://www.baidu.com/',
            # 'Accept-Encoding': 'gzip, deflate',
            # 'Accept-Language': 'en-US,en;q=0.8,zh-CN;q=0.6,zh;q=0.4,zh-TW;q=0.2',
        }

        post_data = self.get_post_data(utils.timestamp(),token,'','')
        print(post_data)
        rsp = self.session.post(
            url=self.sign_url,
            data=post_data,
            headers=header,
        )
        ''':type : requests.Response'''
        print(rsp.status_code)
        # print(rsp.text)
        match  = re.findall('err_no=(\d+)&',rsp.text);
        print('match=',match)

        if not match:
            print(rsp.text)
            return;

        print('err_no=%s',match[0])

        if match[0] == '257' :
            codeString = re.findall(r'codeString=(.*?)&userName',rsp.text)[0]
            print(codeString)
            code = self.get_verifycode(codeString)
            print('code=',code)
            post_data = self.get_post_data(utils.timestamp(),token,codeString,code)

            print(post_data)

            rsp = self.session.post(
                url=self.sign_url,
                data=post_data,
                headers=header,
            )

            print(rsp.status_code)
            print(rsp.text)

        elif match[0] == '0':
            print('登录成功')
            print(rsp.text)

        if rsp.status_code == 200:
            pass
        return;

if __name__ == '__main__':
    pass

    baidu = Baidu('a6377508','6377508')
    baidu.sign_in()
    # baidu.session.get('http://www.baidu.com')
    # t = baidu.get_token(utils.timestamp())

    # print(t)

    # baidu.has_sign_in()



    # timeSpan:"ppui_logintime",
    # data.timeSpan=new Date().getTime()-me.initTime
    # 	this.initTime=new Date().getTime()

    # prefix="bd__cbs__",
    # callbackName=prefix+Math.floor(Math.random()*2147483648).toString(36);



   # 字段：　userName  password

# /static/passpc-account/js/boot_login_bca42bb7.js  是否不变

    # https://passport.baidu.com/v2/?login&tpl=mn&u=http%3A%2F%2Fwww.baidu.com%2F


    # "https://passport.baidu.com/v2/getpublickey?token=417500d70938f4a19a55addbb0f33936&amp;tpl=mn&amp;apiver=v3&amp;tt=1431173100610&amp;callback=bd__cbs__bwul7p"

    # https://passport.baidu.com/v2/getpublickey
    # token: f43c7ba82314886001dc4eff61517e2b
    # tpl: mn
    # apiver: v3
    # tt: 1431168771681
    # callback: bd__cbs__z10aey


    # https://passport.baidu.com/v2/api/?login

    # apiver: v3
    # callback: parent.bd__pcbs__gsd1lq
    # charset: UTF-8
    # codestring:
    # crypttype: 12
    # idc:
    # isPhone:
    # logLoginType: pc_loginDialog
    # loginmerge: true
    # logintype: dialogLogin
    # mem_pass: on
    # password: GqhcHh4ilNurrONN9QEtynURyEYewjEAKcSqfBHkNGwEI7b8SpfXYcUPUNKEVUPajEHQ0w6RxAhJqDfPPPVbLHyGbBP1dXQFxaZf3uPYcVhtTUATQ3/yElYzEJo5QRGWHhQFWc+Rfxj6PW8sOHKW4iGzPlTbznVa6N/zunUDIwQ=
    # ppui_logintime: 5452
    # quick_user: 0
    # rsakey: bOQ4UoJxm55h0NLzG1x5V8H0VlYiELy6
    # safeflg: 0
    # splogin: newuser
    # staticpage: https://www.baidu.com/cache/user/html/v3Jump.html
    # subpro:
    # token: f43c7ba82314886001dc4eff61517e2b
    # tpl: mn
    # tt: 1431168772733
    # u: https://www.baidu.com/?tn=SE_hldp04290_mt35whgs
    # username: a6377508
    # verifycode:


    # callback: parent.bd__pcbs__qcpytr
    # password: jEv45wKefVJkz65YoaUa9enSViVY7Oml4JsjuHjd2pAU2Kx5lHwma7/Vmy33tCew6h7pAkA3afEhe/T9k6NGkVG2oikFAJNkF+IjYGF3RqCYelaXA6YXX9B5iSRJjlnoXDj9ZXFE+9/J+eKdGTWmJpFXauvw+a6wtYe5WbJ6ivo=
    # ppui_logintime: 1154
    # rsakey: cxE6Gzl8AVlEZu9jmWWHDMTJSlrMWNAd

    # token: f43c7ba82314886001dc4eff61517e2b
    # tt: 1431169086781
    # u: https://www.baidu.com/
    # username: a6377508
    # verifycode: