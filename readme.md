0x00 项目功能

    功能描述：逐行遍历pre_review_post.csv并且发评论

0x01 项目基本信息
    
    运行环境：47.93.86.224，阿里云：内网地址：10.116.150.141，外网地址：39.97.184.99

0x02 关键方法与入口函数
    
    ~~[user_info_json_gen.py]~~
    运行环境：本地办公机
    路径：initdata/user_info_json_gen.py
    输入：pre_review_post.csv
    输出：路径initdata/user_info_json下的user_info的json文件

    ~~[main_autologin.py]~~
    输入：
        参数：index_count（user_info的个数）
    功能：
        发布全部的评论
    
    ~~[interface_boost.py]~~
    用于启动接口
    每次更换ip地址或者换地址启动改接口，需要换templates/upload.html 中第6行的ip地址

0x03 其他关键信息
    
    用于xftp按钮shell语句，由于不能通过git同步代码，所以通过一下两个sh按钮获得项目
    
    ~~[getproject.sh]~~
    这是一个xftp按钮 用于获取项目
    
    ~~[rmproject.sh]~~
    这是一个xftp按钮 删除项目，并上传办公机打包好的项目.zip文件
    
    每次更换ip地址或者换地址启动改接口，需要换templates/upload.html 中第6行的ip地址

    有些游戏是测试服的，可能会导致评论发布失败，因为页面本身的跳转有问题
