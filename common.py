import time
import hashlib
import requests
import json
import sys

#去重
def diffsamedata(userdata):
    tmpnosameid = []
    arytmp = {}
    for v in userdata:
        strid = "%d" % v
        arytmp[ strid ] = 1

    typeData = list(arytmp.items())
    for data in typeData:
        tmpnosameid.append(int(data[0]))

    return tmpnosameid

def writeLog(szText):
    filename = time.strftime("log/Log-%Y-%m-%d.txt", time.localtime())
    f = open(filename, "a+", encoding='UTF-8')

    szHead = time.strftime("%H:%M:%S  ", time.localtime())
    szText = szHead + str(szText) + "\r"
    f.write(szText)
    f.close()


def postEarlyWarnOneNote(szText, iphone):
    iphone = str(iphone)

    datajson = {}
    tick = time.time()
    timestamp = int(tick * 1000)
    datajson['reqID'] = timestamp
    datajson['mobileNo'] = iphone
    datajson['smsContent'] = szText

    iphoneHeader = {}
    iphoneHeader['SERVICEID'] = "45"
    iphoneHeader['APIUSER'] = "vanand_psc"
    iphoneHeader['APIKEY'] = 'dfe380d771c5b30864d4fa73eae8c078'
    # iphoneHeader['Content-Type'] = "application/json"

    try:
        # 内网测试用
        # strtmp = "vanand" + "tangyong" + "%d" % timestamp + "GWUlHss9sfpjCAeV"
        strtmp = "vanand" + "tangyong" + "%d" % timestamp + "2x1nSexaNOodPF4a"
        md5str = hashlib.md5(strtmp.encode(encoding='utf-8')).hexdigest()
        # url = "http://192.168.9.16:80/tkweb/api/sme/custom/send?accessType=vanand&uid=tangyong&" \
        # "timestamp=%d&sign=%s" % (timestamp, md5str )
        url = "https://secgateway.srv.jj.cn/pms-sme/custom/send?accessType=vanand&uid=tangyong&" \
              "timestamp=%d&sign=%s" % (timestamp, md5str)
        req = requests.post(url, headers=iphoneHeader, json=datajson, timeout=10)
        data = json.loads(req.text)

        if -1 == data['errcode']:
            print("发送给=%s短信失败=%s" % (iphone, szText))
            writeLog("发送给=%s短信失败=%s" % (iphone, szText))
        elif 0 == data['errcode']:
            # print("发送短信成功：", req.text)
            pass
    except:
        print("网页%s短信发送失败=%s" % (iphone, szText))
        writeLog("网页%s短信发送失败=%s,%s" % (iphone, szText, str(sys.exc_info()[0])))
