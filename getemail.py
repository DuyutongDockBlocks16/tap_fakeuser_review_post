import poplib
from email.parser import Parser
import os
import sys
import json
import urllib
import requests
import time

__localparam = ''' -H "authority: mail.163.com" -H "accept: text/javascript" -H "origin: https://mail.163.com" -H "sec-fetch-dest: empty" -H "user-agent: Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.87 Safari/537.36 SE 2.X MetaSr 1.0" -H "content-type: application/x-www-form-urlencoded" -H "sec-fetch-site: same-origin" -H "sec-fetch-mode: cors" -H "referer: https://mail.163.com/js6/main.jsp?sid='''
__localparam2 = '''&df=email163" -H "accept-language: zh-CN,zh;q=0.9" -H "cookie: '''


def getemail():
    filename = "./initdata/userinfo.json"
    f = open(filename, "r", encoding='UTF-8-sig')
    filestr = f.read()
    f.close()

    data = json.loads(filestr)

    return data['email']


def getepassword():
    filename = "./initdata/userinfo.json"
    f = open(filename, "r", encoding='UTF-8-sig')
    filestr = f.read()
    f.close()

    data = json.loads(filestr)

    return data['password']


def loginemail(index):
    try:
        cmd = f"node loginemail.js --index_num {index}"
        status = os.system(cmd)
        if 0 != status:
            print("执行node loginemail.js失败", flush=True)
    except:
        print("执行node loginemail.js出现异常", flush=True)


def getparam(index):
    filename = f"./datajson/cookies_email_{index}.json"
    f = open(filename, "r", encoding='UTF-8-sig')
    filestr = f.read()
    f.close()

    data = json.loads(filestr)
    cookiestr = ""
    sid = ""
    for v in data:
        if v['name'] == "Coremail.sid":
            sid = v['value']
        cookiestr = cookiestr + v['name'] + "=" + v['value'] + ";"

    localparam = __localparam + sid + __localparam2 + cookiestr + '''"'''

    return localparam, sid


def analydata(emaildata, index):
    if not 'var' in emaildata:
        print(emaildata)
        return False

    vardata = emaildata['var']

    emailcode = ""
    sendtime = 0
    recievetime = 0
    for v in vardata:
        emailfrom = v['from']
        if emailfrom.find("noreply@dm.taptap.com") < 0:
            continue

        subject = v['subject']
        senddata = v['sentDate']
        sendtime = "%d-%d-%d %d:%d:%d" % (
        senddata[0], senddata[1] + 1, senddata[2], senddata[3], senddata[4], senddata[5])
        sendtime = int(time.mktime(time.strptime(sendtime, "%Y-%m-%d %H:%M:%S")))

        receivedDate = v['receivedDate']
        recievetime = "%d-%d-%d %d:%d:%d" % (
        receivedDate[0], receivedDate[1] + 1, receivedDate[2], receivedDate[3], receivedDate[4], receivedDate[5])
        recievetime = int(time.mktime(time.strptime(recievetime, "%Y-%m-%d %H:%M:%S")))

        start = subject.find('is your TapTap verification code')
        if start > 0:
            emailcode = subject[0:start - 1]

        break

    # emailcode不为空
    if emailcode != "":
        return writeemailjson(emailcode, sendtime, recievetime, index)

    return False


def writeemailjson(emailcode, sendtime, receivetime, index):
    cookies = []

    filename = "./datajson/emailcode.json"
    f = open(filename, "r", encoding='UTF-8-sig')
    filestr = f.read()
    f.close()

    data = json.loads(filestr)

    print(emailcode, sendtime, receivetime, data['starttime'])
    if receivetime < data['starttime']:
        return False

    data['emailcode'] = emailcode
    data['sendtime'] = sendtime
    data['receivetime'] = receivetime

    json_str = json.dumps(data)

    filename = f"./datajson/emailcode_{index}.json"
    f = open(filename, "w", encoding='utf-8')
    f.write(json_str)
    f.close()

    print("获取邮箱验证码成功:" + emailcode, flush=True)

    return True


def get_email_content(index):
    datasend = ''' --data "var=%3C%3Fxml%20version%3D%221.0%22%3F%3E%3Cobject%3E%3Cint%20name%3D%22fid%22%3E1%3C%2Fint%3E%3Cstring%20name%3D%22order%22%3Edate%3C%2Fstring%3E%3Cboolean%20name%3D%22desc%22%3Etrue%3C%2Fboolean%3E%3Cint%20name%3D%22limit%22%3E20%3C%2Fint%3E%3Cint%20name%3D%22start%22%3E0%3C%2Fint%3E%3Cboolean%20name%3D%22skipLockedFolders%22%3Efalse%3C%2Fboolean%3E%3Cstring%20name%3D%22topFlag%22%3Etop%3C%2Fstring%3E%3Cboolean%20name%3D%22returnTag%22%3Etrue%3C%2Fboolean%3E%3Cboolean%20name%3D%22returnTotal%22%3Etrue%3C%2Fboolean%3E%3Cstring%20name%3D%22mrcid%22%3E19a9bd3ea617411a76e4cdc2aad5ac83_v1%3C%2Fstring%3E%3C%2Fobject%3E"'''

    param, sid = getparam(index)
    if "" == sid:
        print("sid为空")
        return

    cmd = '''curl -s "https://mail.163.com/js6/s?sid=''' + sid + '''&func=mbox:listMessages"''' + param + datasend

    try:
        data = os.popen(cmd).read()

        data = data.replace('new Date', "")
        data = data.replace('true', 'True').replace('false', 'False')
        data = eval(data)

        return data

    except:
        print("get_email_content:" + str(sys.exc_info()), flush=True)

    return


def loginemailandreceviemail(index):
    # 登陆邮箱
    loginemail(index)

    cnt = 0
    # 获取邮件
    while (True):
        emailstr = get_email_content(index)
        if "" == emailstr:
            return 2

        flag = analydata(emailstr, index)
        if flag:
            break
        else:
            time.sleep(60)
            cnt = cnt + 1

            if cnt > 3:
                return 1

    return 0


if __name__ == '__main__':
    pass

    # analydata("")
    loginemailandreceviemail()

    # createuserinfojson()
