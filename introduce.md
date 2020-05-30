### DUST 测试平台简介

#### 简介

**版本** v1.1
本平台主要为练手产物，其中存在一些bug，请及时联系管理员。

#### 平台结构
```text
├─app                                  #flask的程序
│  ├─admin                             #后台程序
│  ├─login                             #登录程序
│  ├─static                            #全部静态文件
│  │  ├─css                     
│  │  └─js
│  ├─templates                         #全部页面
│  │  ├─control
│  │  └─report
├─dust                                 #后台处理逻辑
├─migrations                           #数据库备份文件
├─sql                                  #需要插入的数据
├─app.py                               #程序入口
├─data.sqlite                          #数据库文件
├─exts.py                              #数据库连接
├─introduce.md                         #介绍文档
├─manager.py                           #添加数据库入口
├─setting.py                           #相关配置文件
```

#### 1. 数据库初始化
将代码clone之后，需要初始化数据库。步骤如下
1.数据库初始化
>python manager.py db init

2.数据库生成备份文件
>python manager.py db migrate

3.数据库更新
>python manager.py db upgrade

4.生成登录管理员
>python manager.py create_user -u admin -p admin -e 123@qq.com -ph 13355885566

#### 2.导入数据
打开sql文件夹，将里面的sql文件导入数据库。避免出现一些不必要的问题。数据文件在sql文件夹中，执行sql语句就可以实现导入。

#### 3.运行程序
运行程序可以直接run apps.py 程序就可以实现，简易更改端口，避免造成端口占用的问题。

#### 4.功能简介
此版本为开发的V1.0版本，主要目的是优化上一个版本的数据库响应时间长，和页面冲突以及一些其他优化。
1. 在此版本实现了压力测试突变展示系统，可以每2秒进行一次推送，数据进行实时显示。
2. 本版本实现了权限系统，通过控制url来实现访问
3. 增加操作日志查询展示页面，同时增加慢日志的查询方法，通过词频展示的方式查看慢sql的方式。
4. 重写测试报告模板。
5. 对上传和下载功能进行了优化
6. 实现checkbox的勾选执行，批量删除功能。
7. 实现登录时密码加密功能
8. 实现修改密码功能
9. 增加用例统计展示板和对应图形展示
