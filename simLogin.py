# -*- coding: UTF-8 -*-

import  redis_util
import os
from logger import LOG
import  json
import  uuid
import sys
import  urllib
import requests
import time

__localparam = ''' -H "authority: accounts.taptap.com" -H "origin: https://accounts.taptap.com" -H "user-agent: Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.87 Safari/537.36 SE 2.X MetaSr 1.0" -H "content-type: application/x-www-form-urlencoded" -H "accept: application/json, text/plain, */*" -H "sec-fetch-dest: empty" -H "x-requested-with: XMLHttpRequest" -H "x-ua: V=1&PN=Accounts&LANG=zh_CN&VN_CODE=2&UID=1d037636-7d87-4083-89d3-fbb89be68e2a&PLT=PC" -H "sec-fetch-site: same-origin" -H "sec-fetch-mode: cors" -H "referer: https://accounts.taptap.com/login?type=email" -H "accept-language: zh-CN,zh;q=0.9" -H "cookie: '''

def  getparam(index):
    filename = f"./datajson/codecookies_{index}.json"
    f = open(filename, "r", encoding='UTF-8-sig')
    filestr = f.read()
    f.close()

    data = json.loads(filestr)
    cookiestr = ""
    for v in data:
        cookiestr = cookiestr + v['name'] + "=" + v['value'] + ";"

    localparam = __localparam + cookiestr + '''"'''

    return localparam

#生成设置cookies
def createsetcookie(index):
    pass

    cookies = []

    filename = f"./datajson/codecookies_{index}.json"
    f = open(filename, "r", encoding='UTF-8-sig')
    filestr = f.read()
    f.close()

    data = json.loads(filestr)
    for v in data:
        cookies.append(v)

    filename = "./datajson/cookie_c.txt"
    f = open(filename, "r", encoding='UTF-8-sig')
    filestr = f.read()
    f.close()

    start = filestr.find("ACCOUNTS_SESS")
    acccount = {}
    if start > 0:
        sztoken = filestr[start + 13: -1]
        sztoken = sztoken.lstrip("\t")

        acccount['name'] = "ACCOUNTS_SESS"
        acccount['value'] = sztoken
        acccount['domain'] = "accounts.taptap.com"
        acccount['path'] = "/"
        acccount['expires'] = time.time() + 24 * 60 * 60
        acccount['size'] = len("ACCOUNTS_SESS") + len(sztoken)
        acccount['httpOnly'] = True
        acccount['secure'] = False
        acccount['session'] = False
        acccount['sameParty'] = False
        acccount['sourceScheme'] = "Secure"
        acccount['sourcePort'] = 443

    cookies.append(acccount)

    json_str = json.dumps(cookies)

    filename = f"./datajson/set_cookies_{index}.json"
    f = open(filename, "w", encoding='utf-8')
    f.write(json_str)
    f.close()

def runcookies(index):
    pass

    email = getemail(index)
    encode_url = urllib.request.quote(email)
    email_code = getcodeemail(index)

    #email_code = "246060"
    datasend = ''' --data "email_code=''' + str(email_code) +'''&email_address=''' + encode_url + '''" '''
    cmd =  '''curl -s --cookie-jar ./datajson/cookie_c.txt "https://accounts.taptap.com/api/email/login"''' + getparam(index) + datasend

    try:
        print("cmd")
        print(cmd)
        data = json.loads(os.popen(cmd).read())

        if 'OK' == data['code']:
            print("登陆成功" + str(data),flush = True)

            createsetcookie(index)
        else:
            LOG.warn("[TOKEN_LOST]回复失败，token失效:" + str(data))
            print("登陆失败" + str(data),flush = True)

    except:
        print("runcookies:" + str(sys.exc_info()),flush = True)

def getemail(index):
    filename = f"./initdata/user_info_json/userinfo_{index}.json"
    f = open(filename, "r", encoding='UTF-8-sig')
    filestr = f.read()
    f.close()

    data = json.loads(filestr)

    return data['email']

def getcodeemail(index):
    filename = f"./datajson/emailcode_{index}.json"
    f = open(filename, "r", encoding='UTF-8-sig')
    filestr = f.read()
    f.close()

    data = json.loads(filestr)

    return data['emailcode']


def runcardverify(index):
    try:
        cmd = f"node taplogin.js --index_num {index}"
        status = os.system(cmd)

        if 0 != status:
            LOG.error("执行node get_cookies.js失败")
        else:
            pass

            #result = os.popen('tail -1 ./errlog/errlog.txt')
            #context = result.read()
            #print(context, flush=True)
    except:
        LOG.error("执行node get_cookies.js出现异常")

if __name__ == '__main__':
    pass

    #runcookies()
    #runcardverify()

    createsetcookie()
