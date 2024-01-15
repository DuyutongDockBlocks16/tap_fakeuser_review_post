# -*- coding: UTF-8 -*-

import rungetcode
import time
import getemail
import simLogin
import shutil
import os
import common
import setcard
import json


def autologin(index):
    print("开始执行自动登录相关操作", flush=True)
    tick0 = int(time.time())

    # 用puppteer输入账号，准备获取邮箱验证码
    rungetcode.runloginjs(index)

    tickemail = int(time.time())
    print("邮箱输入操作时间:" + str(tickemail - tick0), flush=True)

    # 停顿3秒，以便一遍就能接收到验证码
    time.sleep(3)

    print("开始获取验证码:" + time.strftime("%Y-%m-%d %H:%M:%S"), flush=True)

    # 登录邮箱，获取验证码
    flag = getemail.loginemailandreceviemail(index)
    if flag > 0:
        return flag

    print("获取邮箱验证码时间:" + str(int(time.time()) - tickemail), flush=True)

    # 登录taptap
    simLogin.runcookies(index)

    # 用puppteer注入cookies，并进行身份验证
    simLogin.runcardverify(index)

    # 进行发帖等动作
    email, password, appid, note, score = getappidandnote(index)
    setcard.postapnote(email, password, appid, note, score, index)

    tick1 = int(time.time())
    print("执行完成，共花费=%d秒" % (tick1 - tick0), flush=True)

    return 0


def getappidandnote(index):
    filename = f"./initdata/user_info_json/userinfo_{index}.json"
    f = open(filename, "r", encoding='UTF-8-sig')
    filestr = f.read()
    f.close()

    data = json.loads(filestr)

    return data['email'], data['password'], data['appid'], data['note'], data['score']


# 拷贝
def copyscrfiletoinitfile(index):
    srcfilename = "./srcdata/userinfo_%d.json" % index
    if not os.path.isfile(srcfilename):
        print("该文件不存在:" + srcfilename, flush=True)
        return False

    initfilename = "./initdata/userinfo.json"

    shutil.copyfile(srcfilename, initfilename)

    filename = "./initdata/lognote.txt"
    f = open(filename, "w", encoding='utf-8')
    f.write(str(index))
    f.close()

    return True


def getstartnum():
    filename = "./initdata/lognote.txt"
    f = open(filename, "r", encoding='UTF-8-sig')
    filestr = f.read()
    f.close()

    if filestr.isdigit():
        return int(filestr)

    return -1


def writeerrmsg(index):
    strerr = "获取邮箱验证码失败，请查看程序:" + str(index) + "," + time.strftime("%Y-%m-%d %H:%M:%S")
    common.postEarlyWarnOneNote(strerr, 13693229150)
    print(strerr, flush=True)

    filename = "./initdata/sndemailfailed.txt"
    f = open(filename, "a+", encoding='utf-8')
    f.write(str(index))
    f.write("\n")
    f.close()


def mainloop():
    index = getstartnum()

    if index < 0:
        print("读取参数错误，程序中止", flush=True)
        return

    while True:
        print("===========开始第%d个操作:" % index + time.strftime("%Y-%m-%d %H:%M:%S"), flush=True)

        flag = copyscrfiletoinitfile(index)
        if not flag:
            break

        rcode = autologin()
        if 1 == rcode:
            #
            print("获取邮箱验证码重复失败，继续重新进行登录操作", flush=True)
            time.sleep(300)
            if autologin() > 0:
                writeerrmsg(index)
        elif 2 == rcode:
            writeerrmsg(index)

        time.sleep(300)

        index = index + 1

    print("流程中止，end", flush=True)


# 自动登录
if __name__ == '__main__':
    index_count = 1
    for element_index in range(3, 4):
        autologin(element_index)
