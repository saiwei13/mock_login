# -*- coding: utf-8 -*-

import requests


__author__ = 'chenwei'

# 分段加密
CHUNK_SIZE = 30

# RSA加密
def enctypt(e, m, c):
        return pow(c, e, m)

# 加密一段
def enctyptChunk(e, m, chunk):

    chunk = list(chunk)
    for i in range(len(chunk)):
        chunk[i] = ord(chunk[i])

    # 补成偶数长度
    if not len(chunk) % 2 == 0:
        chunk.append(0)

    nums = [ chunk[i] + (chunk[i+1] << 8) for i in range(0, len(chunk), 2) ]

    c = sum([n << i*16 for i, n in enumerate(nums)])

    encypted = enctypt(e, m, c)

    # 转成16进制并且去掉开头的0x
    return hex(encypted)[2:]

# 加密字符串，如果比较长，则分段加密
def encryptString(e, m, s):

    print("encryptString()","e=%s   m=%s   pwd=%s" %(e,m,s))

    e, m = int(e, 16), int(m, 16)

    chunks = [ s[:CHUNK_SIZE], s[CHUNK_SIZE:] ] if len(s) > CHUNK_SIZE else [s]

    # print('chunks=',chunks)

    result = [enctyptChunk(e, m, chunk) for chunk in chunks]

    print('加密pwd=',result)

    # return ' '.join(result)[:-1] # 去掉最后的'L'
    return result[0]

def getEncryptKey():

        r = requests.get('http://login.renren.com/ajax/getEncryptKey')
        ''':type r : requests.Response'''
        print (r.status_code)
        # return r.json()


if __name__ == '__main__':

    key = getEncryptKey()
    str = encryptString('10001', '80f83b96aa216c08db78e5842e2fef33ede970ac2dc2ab7a341b18efd52eab79', '111111')
    print(str)

