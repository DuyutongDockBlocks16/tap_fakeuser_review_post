import json
import csv
import os
import mysql_operate


def createuserjosnelse(email, password, appid, strnote, score, index):
    data = {}
    data['email'] = email
    data['password'] = password
    data['appid'] = appid
    data['note'] = strnote
    data['score'] = score
    data['index'] = index

    json_str = json.dumps(data)

    filename = f"./user_info_json/userinfo_{index}.json"

    f = open(filename, "w", encoding='utf-8')
    f.write(json_str)
    f.close()

def del_file(path):
    ls = os.listdir(path)
    for i in ls:
        c_path = os.path.join(path, i)
        if os.path.isdir(c_path):
            del_file(c_path)
        else:
            os.remove(c_path)



def user_info_gen(file_path):
    print(os.path.join("user_info_json/"))

    del_file(os.path.join("user_info_json/"))

    with open(file_path,encoding='gbk') as f:
        f_csv = csv.reader(f)
        for row in f_csv:
            email_info = str(row[0])
            submit_sql = f"""SELECT AES_DECRYPT(password, 'hongxuanzhuan_key') as pwd from virtual_user_info vui where email='{email_info}' limit 1"""
            data = mysql_operate.db.select_db(submit_sql)
            pwd_info = bytes.decode(data[0].get("pwd"))
            gameid_info = row[2]
            review_text_info = row[3]
            score_info = row[4]
            index_info = row[5]
            print(email_info, pwd_info, gameid_info, review_text_info, score_info)
            createuserjosnelse(email_info, pwd_info, gameid_info, review_text_info, score_info, index_info)


if __name__ == '__main__':
    file_path = "D:/pythonProject/simuLogin/upload/pre_review_post.csv"
    user_info_gen(file_path)




