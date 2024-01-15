import os
from logger import LOG
import  json
import  time

def createemailcode(index):
    pass

    emailcode = {}
    emailcode['starttime'] = int(time.time())
    emailcode['emailcode'] = ""
    emailcode['sendtime'] = 0
    emailcode['receivetime'] = 0

    json_str = json.dumps(emailcode)

    filename = f"./datajson/emailcode_{index}.json"
    f = open(filename, "w", encoding='utf-8')
    f.write(json_str)
    f.close()

def runloginjs(index):
    #生成初始emailcode文件
    createemailcode(index)

    try:
        cmd = f"node getcode.js --index_num {index}"
        status = os.system(cmd)
        if 0 != status:
            print("执行node runloginjs失败",flush = True)
        else:
            print("执行node runloginjs成功",flush = True)
    except:
        print("执行runloginjs出现异常",flush = True)


if __name__ == '__main__':
    pass
    createemailcode()
    runloginjs()