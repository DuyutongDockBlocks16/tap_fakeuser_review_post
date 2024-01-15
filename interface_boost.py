# -*- coding: UTF-8 -*-
import threading
from main_autologin import autologin
from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
import os
from initdata.user_info_json_gen import user_info_gen

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'upload/'


def del_file(path):
    ls = os.listdir(path)
    for i in ls:
        c_path = os.path.join(path, i)
        if os.path.isdir(c_path):
            del_file(c_path)
        else:
            os.remove(c_path)

def review_post():
    # 读取全部的json文件名
    user_json_path = os.path.join("user_info_json/")
    file_names = os.listdir(user_json_path)

    # 获取所有文件名中的编号
    file_index_list = []
    for element in file_names:
        json_index = element[element.find('_') + 1:element.find('.json')]
        file_index_list.append(int(json_index))

    for element_index in file_index_list:
        autologin(element_index)

    # 测试用的逻辑
    # for element_index in range(3, 4):
    #     try:
    #         autologin(element_index)
    #     except Exception as e:
    #         print(e)

@app.route('/upload')
def upload_file():
    return render_template('upload.html')

@app.route('/uploader',methods=['GET','POST'])
def uploader():
    if request.method == 'POST':

        f = request.files['file']
        print(request.files)
        f.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(f.filename)))

        # 生成user_info的json文件，用于后续发评论用
        user_info_gen(os.path.join(app.config['UPLOAD_FOLDER'])+f.filename)

        print('file uploaded successfully')
        # 单独启动一个进程来执行发评论的操作
        review_post_thread = threading.Thread(target=review_post,
                                             args=(),
                                             name='review_post_thread')
        review_post_thread.start()
        print('review_post_thread has started')

        return 'file uploaded successfully'

    else:

        return render_template('upload.html')

if __name__ == '__main__':
   app.run(
      host = '0.0.0.0',
      port = 5000,
      debug = True
   )
