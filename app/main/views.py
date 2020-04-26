#！/usr/bin/env python
#! -*-coding:utf-8 -*-
#!@Author : zhuxx
#!@time : 2020/04/20 11:01

import random
import os
import simplejson

from flask import render_template, redirect, url_for,jsonify,request,send_from_directory
from werkzeug.utils import secure_filename
from flask_login import login_required, current_user
from app.models import CfgNotify,Task,Report,User,TaskResult
from app.main.forms import TaskFrom,ReportFrom,PostManFrom,SecretFrom,GoogleFrom,AsynchronousForm,SearchForm,UserForm,ChangePassword
from . import main
from .func import common_edit,common_list,edit_task,showrepoer,render_analysis,edit_postman,tools_func,run_tasks,\
    create_thumbnail,gen_file_name,allowed_file,input_task,select_num,render_analysis_line,render_analysis_word_could,\
    changepassword
from dust.util.echarts_every_pic import line_base,word_could,pie_base
from dust.util.upload_file import uploadfile
from conf.config import Config


info = {}
line_info = {}
wordCould_info = {}

@main.route('/', methods=['GET'])
@login_required
def root():
    return redirect(url_for('main.index'))


@main.route('/index', methods=['GET'])
@login_required
def index():
    num1, num2, num3, num4 = select_num(Task,Report,User)
    global line_info
    line_info = render_analysis_line(Report)
    return render_template('index.html', current_user=current_user, num1=num1,num2=num2,num3=num3,num4=num4)


@main.route('/notifylist', methods=['GET', 'POST'])
@login_required
def notifylist():
    return common_list(User, 'notifylist.html')


@main.route('/task',methods=['GET','POST'])
@login_required
def show_tasks():
    return common_list(Task, 'show_tasks.html')


@main.route('/edit_task',methods=['GET','POST'])
@login_required
def edit_tasks():
    return edit_task(Task, TaskFrom(), 'edit_tasks.html')


@main.route('/run_task',methods=['GET','POST'])
@login_required
def run_task():
    return run_tasks(Task,SearchForm(), 'run_task.html')


@main.route('/postman',methods=['GET','POST'])
@login_required
def post_man():
    return edit_postman(Task,PostManFrom(),'post_man_test.html')


@main.route('/analysis_report',methods=["GET"])
@login_required
def analysis_report():
    global info,wordCould_info
    info = render_analysis(Report)
    wordCould_info = render_analysis_word_could(TaskResult,info[0])
    return render_template('analysis_report_test.html',current_user=current_user)


@main.route('/report',methods=["GET"])
@login_required
def show_report():
    return common_list(Report,'show_report.html')


@main.route('/report_demo',methods=["GET"])
@login_required
def show_report_demo():
    view = "report/{}_{}.html"
    return showrepoer(Report,ReportFrom,view)


@main.route('/authority',methods=['GET',"POST"])
@login_required
def auth_limit():
    pass


@main.route("/lineChart")
@login_required
def get_line_chart():
    time_point,success,fail,error = line_info
    c = line_base(time_point,success,fail,error)
    return c.dump_options_with_quotes()


@main.route("/lineDynamicData")
@login_required
def update_line_data():
    time_point, success, fail, error = line_info
    now_point = time_point[-1] + 1
    return jsonify({'name1':now_point,'value1':success[-1],
                    'name2':now_point,'value2':fail[-1],
                    'name3':now_point,'value3':error[-1]})

@main.route("/analysis_report/pieChart")
@login_required
def get_pie_data():
    task_name, value = info
    c = pie_base(task_name,value)
    return c.dump_options_with_quotes()


@main.route("/analysis_report/wordCouldChart")
@login_required
def get_word_could_data():
    task_name, value = wordCould_info
    c = word_could(task_name,value)
    return c.dump_options_with_quotes()


@main.route("/method_index",methods=['GET',"POST"])
@login_required
def method_index():
    return render_template('method_index.html')


@main.route("/json")
@login_required
def method_json():
    return render_template('json.html')


@main.route("/secret",methods=['GET',"POST"])
@login_required
def method_secret():
    return tools_func('secret.html',SecretFrom())


@main.route("/google_code",methods=['GET',"POST"])
@login_required
def method_google_code():
    return tools_func('google_code.html',GoogleFrom())


@main.route("/send_async",methods=['GET',"POST"])
@login_required
def method_async():
    return tools_func('async_send.html',AsynchronousForm())


@main.route('/uploade',methods=['GET',"POST"])
@login_required
def upload_index():
    size = Config.MAX_CONTENT_LENGTH / 1024 ** 2
    info = ", ".join(sorted(Config.ALLOWED_EXTENSIONS))
    return render_template('upload.html',size=size,info=info)

@main.route("/upload", methods=['GET', 'POST'])
@login_required
def upload():
    if request.method == 'POST':
        files = request.files['file']

        if files:
            filename = secure_filename(files.filename)
            filename = gen_file_name(filename)
            mime_type = files.content_type

            if not allowed_file(files.filename):
                result = uploadfile(name=filename, type=mime_type, size=0, not_allowed_msg="上传的格式不在允许上传的范围内")

            else:
                # save file to disk
                uploaded_file_path = os.path.join(Config.UPLOAD_FOLDER, filename)
                files.save(uploaded_file_path)

                # create thumbnail after saving
                if mime_type.startswith('image'):
                    create_thumbnail(filename)

                # get file size after saving
                size = os.path.getsize(uploaded_file_path)

                # return json for js call back
                result = uploadfile(name=filename, type=mime_type, size=size)

                # # create tasks
                input_result = input_task(filename)
                print(input_result)

            return simplejson.dumps({"files": [result.get_file()]})

    if request.method == 'GET':
        # get all file in ./data directory
        files = [f for f in os.listdir(Config.UPLOAD_FOLDER) if
                 os.path.isfile(os.path.join(Config.UPLOAD_FOLDER, f))]

        file_display = []

        for f in files:
            size = os.path.getsize(os.path.join(Config.UPLOAD_FOLDER, f))
            file_saved = uploadfile(name=f, size=size)
            file_display.append(file_saved.get_file())

        return simplejson.dumps({"files": file_display})

    return redirect(url_for('index'))


@main.route("/delete/<string:filename>", methods=['DELETE'])
def delete(filename):
    file_path = os.path.join(Config.UPLOAD_FOLDER, filename)
    file_thumb_path = os.path.join(Config.THUMBNAIL_FOLDER, filename)

    if os.path.exists(file_path):
        try:
            os.remove(file_path)

            if os.path.exists(file_thumb_path):
                os.remove(file_thumb_path)

            return simplejson.dumps({filename: 'True'})
        except:
            return simplejson.dumps({filename: 'False'})



@main.route("/thumbnail/<string:filename>", methods=['GET'])
def get_thumbnail(filename):
    return send_from_directory(Config.THUMBNAIL_FOLDER, filename=filename)


@main.route("/data/<string:filename>", methods=['GET'])
def get_file(filename):
    return send_from_directory(os.path.join(Config.UPLOAD_FOLDER), filename=filename)


@main.route("/changepassword",methods=['GET',"POST"])
@login_required
def change_password():
    changepassword(User,'changepassword.html',ChangePassword())


@main.route("/notifyedit",methods=['GET',"POST"])
@login_required
def edit_user():
    return common_edit(User,UserForm(),'notifyedit.html')


@main.route("/adduser",methods=['GET',"POST"])
@login_required
def add_user():
    return common_edit(User,UserForm(),'add_user.html')