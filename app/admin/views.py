#！/usr/bin/env python
#! -*-coding:utf-8 -*-
#!@Author : zhuxx
#!@time : 2020/05/08 09:56

from flask import Blueprint, render_template, request, session, redirect, url_for, jsonify, send_from_directory
from flask_sqlalchemy import get_debug_queries
from werkzeug.utils import secure_filename

from app.models import User,Role,AdminLog,TaskReport,Tasks,Env,TaskResult,Auth,TaskRun
from app.admin.util import get_welcome_info,line_base,add_example,common_del,edit_example,search_info,task_run,\
    upload_task,cpu_line,memory_liquid,net_io_line,disk_line,add_common,word_could,add_running
from app.admin.forms import AddTask,AuthForm,RoleForm,UserForm,TaskRunning
from setting import BasicConfig
from exts import db

from datetime import datetime
from functools import wraps
from itertools import product
import os
import logging

admin = Blueprint('admin',__name__)
line_info = []

# 有无访问权限装饰器： 判断用户权限控制
def admin_auth(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        user_id = session['user_id']
        admin = User.query.join(Role).filter(Role.id == User.role_id,
                                             User.user_id == user_id).first()
        auths = admin.role.auths
        auth_list = [int(i) for i in auths.split(',')]
        auth_all = Auth.query.all()
        real_auth = []
        for auth,val in product(auth_all,auth_list):
            if auth.id == val:
                real_auth.append(auth.url)
        rule = str(request.url_rule)
        if rule not in real_auth:
            return render_template('error/404.html',info='您无权访问/操作此内容，请联系管理员开启此权限')
        return func(*args, **kwargs)
    return wrapper

#首页
@admin.route('/index')
def index():
    session_id = session['user_id']
    users = User.query.filter_by(user_id=session_id).first()
    username = users.username
    return render_template('index.html',username=username)

#个人信息
@admin.route('/profile')
def profile():
    session_id = session['user_id']
    users = User.query.filter_by(user_id=session_id).first()
    return render_template('profile.html',user=users)

#修改密码
@admin.route('/editpwd',methods=['GET','POST'])
def editpwd():
    user_id = session['user_id']
    user = User.query.filter_by(user_id=user_id).first()
    if request.method == 'GET':
        return render_template('edit_pwd.html',user=user)
    else:
        oldpwd = request.form.get('oldpwd')
        newpwd1 = request.form.get('newpwd1')
        newpwd2 = request.form.get('newpwd2')
        print(oldpwd)
        user.password = newpwd1
        db.session.commit()
        return render_template('edit_pwd.html', user=user,message="密码修改成功！")

#校验密码
@admin.route('/checkpwd')
def checkpwd():
    oldpwd = request.args.get('oldpwd', '')
    user_id = session['user_id']
    user = User.query.filter_by(user_id=user_id).first()
    if user.check_password(oldpwd):
        data = {
            "name": user.email,
            "status": 11
        }
    else:
        data = {
            "name": None,
            "status": 00
        }
    return jsonify(data)

#欢迎页面
@admin.route('/welcome')
def welcome():
    global line_info
    session_id = session['user_id']
    users = User.query.filter_by(user_id=session_id).first()
    username = users.username
    admin_logs = AdminLog.query.filter_by(admin_id=session_id).order_by(AdminLog.time.desc())
    login_count = admin_logs.count() // 2 + 1
    if admin_logs.first():
        login_ip_now = admin_logs.first().ip
        login_ip_time = admin_logs.first().time
    else:
        login_ip_now = '127.0.0.1'
        login_ip_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    infos,line_info = get_welcome_info(User,Tasks,TaskReport)
    return render_template('welcome.html',username=username,login_count=login_count,login_ip_now=login_ip_now,
                           login_ip_time=login_ip_time,infos=infos)

#通过Ajax获取line数据
@admin.route('/line')
def get_line_chart():
    c = line_base(*line_info)
    line_info.clear()
    return c.dump_options_with_quotes()

###################
#    用例展示     #
##################

#用例展示
@admin.route('/list_show')
@admin_auth
def list_show():
    pages = int(request.args.get('page',1))
    paginate = Tasks.query.paginate(pages,10)
    tasks = paginate.items
    return render_template('list_show.html',tasks=tasks,paginate=paginate)

#添加用例
@admin.route('/list_add',methods=['GET','POST'])
@admin_auth
def list_add():
    if request.method == "GET":
        return render_template('list_add.html')
    else:
        forms = AddTask(request.form)
        if forms.validate():
            datas = forms.data
            data = add_example(Tasks, datas, db)
        else:
            data = {
                "msg": "表单验证失败",
                "status": "202"
            }
        return jsonify(data)

#编辑用例
@admin.route('/list_edit/',methods=['GET','POST'])
@admin_auth
def list_edit():
    if request.method == "GET":
        ids = request.args.get('id','')
        print(ids)
        if ids or ids != "":
            tasks = Tasks.query.filter(Tasks.id==int(ids)).first()
            return render_template('list_edit.html',data=tasks)
        else:
            tasks = Tasks.query.filter(Tasks.id == 1).first()
            return render_template('list_edit.html', data=tasks)
    else:
        forms = AddTask(request.form)
        if forms.validate():
            datas = forms.data
            data = edit_example(Tasks,datas,db)
        else:
            data = {
                "msg": "表单验证失败",
                "status": "202"
            }
        return jsonify(data)

#删除单个用例
@admin.route('/list_single_del',methods=['POST'])
@admin_auth
def list_single_del():
    if request.method == "POST":
        ids = request.values.get('id')
        data = common_del(Tasks,ids,db)
        return jsonify(data)


#批量删除用例
@admin.route('/list_all_del',methods=['POST'])
@admin_auth
def list_all_del():
    if request.method == "POST":
        ids = request.values.get('id')
        data = common_del(Tasks, ids, db)
        return jsonify(data)

#用例执行
@admin.route('/running_tasks',methods=['POST'])
@admin_auth
def running_task():
    if request.method == "POST":
        ids = request.values.get('id')
        data = task_run(Tasks,TaskResult,TaskReport,Env,ids,db)
        return jsonify(data)
    else:
        return {'msg':'出现问题了！','status':1002}


#用例搜索
@admin.route('/list_search',methods=['GET','POST'])
def list_search():
    if request.method == "GET":
        key = request.args.get('key')
        pages = int(request.args.get('page', 1))
        sql = Tasks.task_id.like(f'%{key}%') | Tasks.task_name.like(f'%{key}%')
        # sql = (Tasks.task_id == key)
        paginate = search_info(Tasks,sql,pages,db)
        tasks = paginate.items
        return render_template('list_show.html',paginate=paginate,tasks=tasks)

#报告展示首页
@admin.route('/list_show_report_index')
@admin_auth
def list_show_report_index():
    pages = int(request.args.get('page', 1))
    paginate = TaskReport.query.paginate(pages, 10)
    report = paginate.items
    return render_template('list_show_report.html', reports=report, paginate=paginate)

#报告展示
@admin.route('/list_show_report',methods=['GET'])
@admin_auth
def list_show_report():
    name = request.args.get('name',"")
    print(name)
    return render_template('report/{}.html'.format(name))


#报告搜索
@admin.route('/list_search_report',methods=['GET','POST'])
def list_search_report():
    if request.method == "GET":
        key = request.args.get('key')
        pages = int(request.args.get('page', 1))
        sql = TaskReport.report_name.like(f'%{key}%')
        paginate = search_info(TaskReport,sql,pages,db)
        reports = paginate.items
        return render_template('list_show_report.html',paginate=paginate,reports=reports)

#下载
@admin.route('/download/<filename>')
def download(filename):
    if filename == 'demo.xlsx':
        real_path = BasicConfig.BASIC_PATH + "/uploade_data/"
        real_filename = filename
    else:
        real_path = BasicConfig.BASIC_PATH + "/app/templates/report"
        real_filename = "{filename}.html".format(filename=filename)
        print(real_path,real_filename)
    return send_from_directory(real_path,real_filename,mimetype='application/octet-stream')

#上传
@admin.route('/upload',methods=['GET','POST'])
def upload():
    size = BasicConfig.MAX_CONTENT_LENGTH / 1024 ** 3
    allow = BasicConfig.ALLOWED_EXTENSIONS
    if request.method == 'GET':
        return render_template('upload.html',msg='请选择上传文件',size=size,info=allow)
    else:
        f = request.files['file']
        suffix = f.filename.split('.')[-1]
        if suffix in BasicConfig.ALLOWED_EXTENSIONS:
            filename = secure_filename(f.filename)
            file_path = os.path.join(BasicConfig.UPLOAD_FOLDER,filename)
            print(file_path)
            f.save(file_path)
            upload_task(db,Tasks,file_path)
            return redirect(url_for('admin.list_show'))
        else:
            return render_template('upload.html',msg='上传出现问题',size=size,info=allow)

#测试结果展示
@admin.route('/list_show_result')
@admin_auth
def list_show_result():
    pages = int(request.args.get('page', 1))
    paginate = TaskResult.query.paginate(pages, 10)
    tasks = paginate.items
    return render_template('list_show_result.html', tasks=tasks, paginate=paginate)

#测试结果搜索
@admin.route('/list_result_search',methods=['GET'])
def list_result_search():
    if request.method == "GET":
        key = request.args.get('key')
        pages = int(request.args.get('page', 1))
        sql = TaskResult.task_id.like(f'%{key}%') | TaskResult.task_son_id.like(f'%{key}%')
        paginate = search_info(TaskResult, sql, pages, db)
        tasks = paginate.items
        return render_template('list_show_result.html', paginate=paginate, tasks=tasks)

#用例模板展示
@admin.route('/list_task_model')
def list_task_model():
    pages = int(request.args.get('page', 1))
    paginate = Tasks.query.paginate(pages, 1)
    tasks = paginate.items
    return render_template('list_task_model.html', tasks=tasks, paginate=paginate)

#测试用例执行页面
@admin.route('/list_running')
# @admin_auth
def list_running():
    pages = int(request.args.get('page', 1))
    paginate = TaskRun.query.paginate(pages, 10)
    running = paginate.items
    return render_template('list_tasks_running.html', running=running, paginate=paginate)

#测试用例执行添加
@admin.route('/list_running_add',methods=['GET',"POST"])
# @admin_auth
def list_running_add():
    if request.method == "GET":
        return render_template('list_running_add.html')
    else:
        forms = TaskRunning(request.form)
        if forms.validate():
            datas = forms.data
            running_infos = Tasks.query.filter(Tasks.task_id.in_(datas['running_info'].replace('，',',').split(','))).all()
            running_info = ",".join([str(info.id) for info in running_infos])
            datas['running_info'] = running_info
            data = add_running(TaskRun, datas, db)
        else:
            data = {
                "msg": "表单验证失败",
                "status": "202"
            }
        return jsonify(data)

#执行任务搜索
@admin.route('/list_result_search',methods=['GET'])
def list_running_search():
    if request.method == "GET":
        key = request.args.get('key')
        pages = int(request.args.get('page', 1))
        sql = TaskRun.id = key
        paginate = search_info(TaskRun, sql, pages, db)
        tasks = paginate.items
        return render_template('list_tasks_running.html', paginate=paginate, running=tasks)

##############################
#    压力测试统计图表展示     #
#############################

#展示页面
@admin.route('/control_index')
@admin_auth
def control_index():
    return render_template('control/control.html')

#cpu
@admin.route('/cpu')
def get_cpu_chart():
    c = cpu_line()
    return c.dump_options_with_quotes()

#内存
@admin.route("/memory")
def get_memory_chart():
    mtotal, mused, mfree, stotal, sused, sfree, c = memory_liquid()
    return jsonify({'mtotal': mtotal, 'mused': mused, 'mfree': mfree, 'stotal': stotal, 'sused': sused, 'sfree': sfree, 'liquid': c.dump_options_with_quotes()})

#流量
@admin.route("/netio")
def get_net_io_chart():
    c = net_io_line()
    return c.dump_options_with_quotes()

#磁盘
@admin.route("/disk")
def get_disk_chart():
    total, used, free, c = disk_line()
    return jsonify({'total': total, 'used': used, 'free': free, 'line': c.dump_options_with_quotes()})


##############################
#          权限系统          #
#############################

#权限列表
@admin.route('/admin_permission')
@admin_auth
def admin_permission():
    page = int(request.args.get('page',1))
    paginate = Role.query.paginate(page,50)
    arts = paginate.items
    return render_template('role_index.html',paginate=paginate,roles=arts)

#添加权限
@admin.route('/admin_add_permission',methods=['GET','POST'])
def admin_add_permission():
    if request.method == "GET":
        return render_template('role_add.html')
    else:
        forms = RoleForm(request.form)
        if forms.validate():
            datas = forms.data
            add_common(db,Role,**datas)
            data = {
                "msg": "添加成功",
                "status": "200"
            }
        else:
            data = {
                "msg": "表单验证失败",
                "status": "202"
            }
        return jsonify(data)

#编辑权限
@admin.route('/admin_edit_permission',methods=['GET','POST'])
def admin_edit_permission():
    if request.method == "GET":
        ids = request.args.get('id', '')
        print(ids)
        if ids or ids != "":
            tasks = Role.query.filter(Role.id == int(ids)).first()
            return render_template('role_edit.html', data=tasks)
        else:
            tasks = Role.query.filter(Role.id == 1).first()
            return render_template('role_edit.html', data=tasks)
    else:
        forms = RoleForm(request.form)
        if forms.validate():
            datas = forms.data
            add_common(db,Role,**datas)
            data = {
                "msg": "添加成功",
                "status": "200"
            }
        else:
            data = {
                "msg": "表单验证失败",
                "status": "202"
            }
        return jsonify(data)

#删除单个权限
@admin.route('/admin_del_permission',methods=['POST'])
def admin_del_permission():
    if request.method == "POST":
        ids = request.values.get('id')
        data = common_del(Role, ids, db)
        return jsonify(data)

#角色列表
@admin.route('/admin_role')
@admin_auth
def admin_role():
    page = int(request.args.get('page',1))
    paginate = Auth.query.paginate(page,50)
    arts = paginate.items
    return render_template('admin_permission.html',paginate=paginate,auths=arts)

#添加角色
@admin.route('/admin_add_role',methods=['GET','POST'])
def admin_add_role():
    if request.method == "GET":
        return render_template('admin_add_permission.html')
    else:
        forms = AuthForm(request.form)
        if forms.validate():
            datas = forms.data
            add_common(db, Auth, **datas)
            data = {
                "msg": "添加成功",
                "status": "200"
            }
        else:
            data = {
                "msg": "表单验证失败",
                "status": "202"
            }
        return jsonify(data)

#编辑角色
@admin.route('/admin_edit_role',methods=['GET','POST'])
def admin_edit_role():
    if request.method == "GET":
        ids = request.args.get('id', '')
        print(ids)
        if ids or ids != "":
            tasks = Auth.query.filter(Auth.id == int(ids)).first()
            return render_template('admin_edit_permission.html', data=tasks)
        else:
            tasks = Auth.query.filter(Auth.id == 1).first()
            return render_template('admin_edit_permission.html', data=tasks)
    else:
        forms = AuthForm(request.form)
        if forms.validate():
            datas = forms.data
            add_common(db, Auth, **datas)
            data = {
                "msg": "添加成功",
                "status": "200"
            }
        else:
            data = {
                "msg": "表单验证失败",
                "status": "202"
            }
        return jsonify(data)

#删除单个角色
@admin.route('/admin_del_role',methods=['POST'])
def admin_del_role():
    if request.method == "POST":
        ids = request.values.get('id')
        data = common_del(Auth, ids, db)
        return jsonify(data)

#平台人员展示
@admin.route('/admin_show_user')
@admin_auth
def admin_show_user():
    page = int(request.args.get('page', 1))
    paginate = User.query.paginate(page, 10)
    arts = paginate.items
    return render_template('admin_show_user.html', paginate=paginate, users=arts)

#平台人员添加
@admin.route('/admin_user_add',methods=['GET',"POST"])
def admin_user_add():
    if request.method == "GET":
        return render_template('admin_user_add.html')
    else:
        forms = UserForm(request.form)
        if forms.validate():
            datas = forms.data
            datas['reg_time'] = datetime.strptime(datas['reg_time'],'%Y-%m-%d %H:%M:%S.%f')
            datas = {**datas,'is_super':0}
            add_common(db, User, **datas)
            data = {
                "msg": "添加成功",
                "status": "200"
            }
        else:
            data = {
                "msg": "表单验证失败",
                "status": "202"
            }
        return jsonify(data)

##############################
#          日志系统          #
#############################
#登录日志
@admin.route('/logs_login')
@admin_auth
def logs_login():
    page = int(request.args.get('page', 1))
    user_id = session['user_id']
    paginate = AdminLog.query.paginate(page, 10)
    all_info = AdminLog.query.all()
    arts = paginate.items
    new = []
    if user_id == 1:
        new = arts
    else:
        for art in all_info:
            if art.admin_id == user_id:
                new.append(art)
    return render_template('logs_login.html', paginate=paginate, logs=new)

#登录日志查询
@admin.route('/logs_login_search')
@admin_auth
def logs_login_search():
    if request.method == "GET":
        key = request.args.get('key')
        pages = int(request.args.get('page', 1))
        sql = AdminLog.operate.like(f'%{key}%')
        paginate = search_info(AdminLog, sql, pages, db)
        infos = paginate.items
        return render_template('logs_login.html', paginate=paginate, logs=infos)

#慢sql查询
@admin.after_app_request
def after_request(response):
    for query in get_debug_queries():
        logging.basicConfig(level=logging.DEBUG,
                            filename=os.path.join(BasicConfig.BASIC_PATH,'logs','query_logs_{}.log'.format(datetime.now().strftime('%Y_%m_%d'))),
                            filemode='a+',
                            format='"[%(asctime)s] {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s" end_logs')
        if query.duration > BasicConfig.FLASK_DB_QUERY_TIMEOUT:
            logging.info("{" + '"Context":"{}","SLOW_QUERY": "{}","Parameters": "{}","START_TIME": "{}","Duration": "{}"'.format(
                query.context,query.statement,query.parameters,query.start_time,query.duration
            ) + "}")
    return response

#日志分析
@admin.route('/logs_analysis')
def logs_analysis():
    return render_template('logs_analysis.html')

#获取词云信息
@admin.route('/get_logs_info')
def get_logs_info():
    c = word_could()
    return c.dump_options_with_quotes()