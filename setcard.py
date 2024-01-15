import  redis_util
import os
from logger import LOG
import  json
import  uuid
import sys
import  urllib
import requests
import uuid
import mysql_operate

__tailparampre = "X-UA=V%3D1%26PN%3DWebApp%26LANG%3Dzh_CN%26VN_CODE%3D71%26VN%3D0.1.0%26LOC%3DCN%26PLT%3DPC%26DS%3DAndroid%26UID%3D"
__tailparam = '''-H "authority: www.taptap.com" -H "origin: https://www.taptap.com" -H "x-xsrf-token:'''
__tailparam2 = '''" -H "user-agent: Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.87 Safari/537.36 SE 2.X MetaSr 1.0" -H "content-type: application/x-www-form-urlencoded; charset=UTF-8" -H "accept: application/json, text/javascript, */*; q=0.01" -H "sec-fetch-dest: empty" -H "x-requested-with: XMLHttpRequest" -H "sec-fetch-site: same-origin" -H "sec-fetch-mode: cors" -H "referer: https://www.taptap.com/user-certification/idcard" -H "accept-language: zh-CN,zh;q=0.9" -H "cookie: '''

def __gettailparam():

    uuidstr = str(uuid.uuid4())

    return   __tailparampre + uuidstr + "%26DT%3DPC%26OS%3DWindows%26OSV%3D10"

def  getcookieparam(index):
    filename = f"./datajson/cookies_taplogin_{index}.json"
    f = open(filename, "r", encoding='UTF-8-sig')
    filestr = f.read()
    f.close()

    data = json.loads(filestr)
    cookiestr =""
    xsrftoken = ""
    for v in data:
        if v['name'] == 'XSRF-TOKEN':
            xsrftoken = v['value']
        cookiestr = cookiestr + v['name'] + "=" + v['value'] + ";"

    xsrftoken = urllib.request.unquote(xsrftoken)
    localparam = __tailparam + xsrftoken + __tailparam2 + cookiestr + '''"'''

    return localparam


def postcardid():
    pass

    realname = ""
    realname = urllib.request.quote(realname)

    idcard = ""
    datasend = ''' --data "real_name=''' + str(realname) +'''&idcard=''' + idcard + '''" '''

    cmd =  '''curl -s "https://www.taptap.com/ajax/profile/idcard"''' + getcookieparam() + datasend

    print(cmd)

    try:
        data = json.loads(os.popen(cmd).read())

        if data['success']:
            print("设置成功")
        else:
            print("设置失败:" + str(data))
    except:
        print(str(sys.exc_info()))

def getscoreandid(appid, index, score):
    appid_str = int(appid)
    try:

        url = "https://www.taptap.com/webapiv2/review-draft/v1/detail?app_id=%d&" % appid_str + __gettailparam()
        cmd = 'curl -s –connect-timeout 10 -m 20 "%s"' % url + getcookieparam(index)

        # print("cmd")
        # print(cmd)

        data = json.loads(os.popen(cmd).read())


    except:
        strerror = str(sys.exc_info())
        print('getscoreandid失败=' + strerror)
        return 0

    if not data['success']:
        print('getscoreandid失败=' + str(data))
        return 0

    print("data")
    print(data)
    id = 0
    noteinfo = data['data']
    if None == noteinfo:
        print("没有数据，需要重新获取")
        id = postcreatenote(appid, index, score)
    else:
        id = noteinfo['id']

    return id


def  postcreatenote(appid, index, score):
    pass
    data = {}
    try:

        datasnd = ''' --data "app_id=''' + appid + '''&score='''+ score +'''&contents=&ratings=%7B%7D&images=%5B%5D"'''
        url = "https://www.taptap.com/webapiv2/review-draft/v1/create?" + __gettailparam()
        cmd = 'curl -s –connect-timeout 10 -m 20 "%s"' % url + getcookieparam(index) + datasnd
        print("cmd")
        print(cmd)

        data = json.loads(os.popen(cmd).read())

    except:
        strerror = str(sys.exc_info())
        print("postcreatenote失败:" + strerror)
        return 0

    if not data['success']:
        print('postcreatenote失败=' + str(data))
        return 0

    noteinfo = data['data']
    id = noteinfo['id']

    return  id

def postapnote(email, password, appid, note, score, index):
    # print("appid: ",appid)
    id = getscoreandid(appid,index,score)
    if 0 == id:
        print("没有获取到评论id,不能进行评论")
        return

    print("评论ID=%d" % id)

    data = {}
    try:

        strnote = urllib.request.quote(note)

        datasnd = ''' --data "score='''+ score +'''&contents=''' + strnote + '''&ratings=%7B%7D&images=%5B%5D&device=Web&hidden_device=1&id=''' + str(id) +'''"'''
        url = "https://www.taptap.com/webapiv2/review-draft/v1/publish?" + __gettailparam()
        cmd = 'curl -s –connect-timeout 10 -m 20 "%s"' % url + getcookieparam(index) + datasnd

        data = json.loads(os.popen(cmd).read())
    except:
        strerror = str(sys.exc_info()[0])
        print("postapnote失败:" + strerror)
        return

    if not data['success']:
        print('postapnote失败=' + str(data))
        return

    print("评论成功")
    submit_sql = "INSERT INTO post_review_record(" \
                 "email, " \
                 "game_id, " \
                 "review_text, " \
                 "score) " \
                 "VALUES('{}', '{}', '{}', '{}')". \
        format(str(email),
               str(appid),
               str(note),
               str(index)
               )
    print(submit_sql)
    mysql_operate.db.execute_db(submit_sql)

if __name__ == '__main__':
    pass

    appid = 196332
    postapnote(appid,"画面精美，值得期待！")
