#！/usr/bin/env python
#! -*-coding:utf-8 -*-
#!@Author : zhuxx
#!@time : 2020/04/20 11:01

import PIL
from PIL import Image
from flask import request,flash,render_template
from flask_login import current_user
from jinja2.exceptions import TemplateNotFound

from conf.config import Config
from app import utils
from dust.util.decrypt_encryption import decrypt,encryption,md5_dec
from dust.util.google_code import calGoogleCode
from dust.util.async_send import main
from dust.util.create_task import ControlExcel
from dust.util.word_could_ccoolection import analysis_word_could

import math
import os
import traceback
import json


def common_list(DynamicModel, view):
    action = request.args.get('action')
    id = request.args.get('id')
    page = int(request.args.get('page')) if request.args.get('page') else 1
    length = int(request.args.get('length')) if request.args.get('length') else Config.ITEMS_PER_PAGE

    if action == 'del' and id:
        try:
            DynamicModel.get(DynamicModel.id == id).delete_instance()
            flash('删除成功')
        except:
            flash('删除失败')

    if action == 'download' and id:
        pass

    if action == 'show_demo' and id:
        return render_template(view.format('report',id,DynamicModel.report_id))

    query = DynamicModel.select()
    total_count = query.count()

    if page: query = query.paginate(page,length)

    dict = {'content': utils.query_to_list(query), 'total_count': total_count,
            'total_page': math.ceil(total_count / length), 'page': page, 'length': length}
    return render_template(view, form=dict, current_user=current_user)


def common_edit(DynamicModel, form, view):
    id = request.args.get('id', '')
    if id:
        model = DynamicModel.get(DynamicModel.id == id)
        if request.method == 'GET':
            utils.model_to_form(model, form)

        if request.method == 'POST':
            if form.validate_on_submit():
                utils.form_to_model(form, model)
                model.save()
                flash('修改成功')
            else:
                utils.flash_errors(form)
    else:
        if form.validate_on_submit():
            model = DynamicModel()
            utils.form_to_model(form, model)
            model.save()
            flash('保存成功')
        else:
            utils.flash_errors(form)
    return render_template(view, form=form, current_user=current_user)

def edit_task(DynamicModel, form, view):
    id = request.args.get('id', '')
    if id:
        model = DynamicModel.get(DynamicModel.id == id)
        if request.method == 'GET':
            utils.model_to_form(model, form)
        if request.method == 'POST':
            if form.validate_on_submit():
                utils.form_to_model(form, model)
                model.save()
                flash('修改成功')
            else:
                utils.flash_errors(form)
    else:
        if form.validate_on_submit():
            model = DynamicModel()
            try:
                if model.get(DynamicModel.task_son_id == form.task_son_id.data).task_son_id:
                    utils.flash_errors(form,err='task_son_id 已经存在',file='task_son_id')
                else:
                    utils.form_to_model(form, model)
                    model.save()
                    flash('保存成功')
            except Exception as e:
                utils.form_to_model(form, model)
                model.save()
                flash('保存成功')
        else:
            utils.flash_errors(form)
    return render_template(view, form=form, current_user=current_user)

def showrepoer(DynamicModel,form,view):
    id = request.args.get('id', '')
    model = DynamicModel.get(DynamicModel.id == id)

    try:
        report_id = model.report_id
        report_name = model.task_name
        return render_template(view.format(report_name,report_id))
    except TemplateNotFound as e:
        flash("{} 报告不存在！！".format(e),"{} 报告不存在！！".format(e))
        return render_template('show_report.html')

def render_analysis(DynamicModel):
    id = request.args.get('id', '') or 1
    model = DynamicModel.get(DynamicModel.id == id)
    if request.method == 'GET':
        infos = utils.obj_to_dict(model)
        task_name = infos['task_name']
        value = {'success': int(infos['success_count']), 'fail': int(infos['fail_count']),
                 'error': int(infos['error_count'])}
        return task_name, value

def render_analysis_word_could(DynamicModel,task_name):
    task_id = request.args.get('id', '') or 1
    query = DynamicModel.select()
    infos = utils.query_to_list(query)
    direction, response = [],[]
    for info in infos:
        if task_id == info['task_id']:
            direction.append(info['describe'])
            response.append(info['response'])
    try:
        word_could_value = analysis_word_could(direction,response)
        if word_could_value == {}:
            value = {'success': 0, 'fail': 0, 'error': 0}
            return task_name,value
    except AttributeError as e:
        word_could_value = {'error':e}
    return task_name,word_could_value

def render_analysis_line(DynamicModel):
    query = DynamicModel.select()
    infos = utils.query_to_list(query)
    success,fail,error = [],[],[]
    # start_time = datetime.datetime.strptime(infos[0]['finish_time'],"%Y-%m-%d %H:%M:%S")
    # end_time = datetime.datetime.strptime(infos[-1]['finish_time'],"%Y-%m-%d %H:%M:%S")
    # totao_during = int((end_time - start_time).total_seconds())
    # during = int((end_time - start_time).total_seconds() / len(infos))
    # time_point = [(start_time + datetime.timedelta(seconds=i)).strftime("%Y-%m-%d %H:%M:%S") for i in range(0,totao_during,during)]
    time_point = [i for i in range(len(infos))]
    for info in infos:
        success.append(int(info['success_count']))
        fail.append(int(info['fail_count']))
        error.append(int(info['error_count']))
    return time_point,success,fail,error

def edit_postman(DynamicModel,form,view):
    if form.validate_on_submit():
        model = DynamicModel()
        result,model1 = utils.form_to_model_special(form, model)
        if model1 != 0:
            model.save()
            flash('保存成功')
        flash("{}".format(result))
    return render_template(view,form=form,current_user=current_user)

def tools_func(view,form):
    if form.validate_on_submit():
        infos = {}
        for wtf in form:
            infos[wtf.name] = wtf.data
        if form.__formname__ == "Secret":
            if infos['secret_name'] == "ras":
                if infos['private_key'] != "":
                    decrypt_secret = decrypt(infos['private_key'],infos['secret'])
                    if isinstance(decrypt_secret,dict):
                        flash("{}".format(decrypt_secret[0]))
                    message_info = decrypt_secret
                    return render_template(view,form=form,current_user=current_user,secret=message_info)

                elif infos['public_key'] != "":
                    encryption_secret = encryption(infos['public_key'],infos['secret'])
                    if isinstance(encryption_secret,dict):
                        flash("{}".format(encryption_secret[0]))
                    message_info = encryption_secret
                    return render_template(view, form=form, current_user=current_user, secret=message_info)
            else:
                md5_secret = md5_dec(infos['secret'])
                if isinstance(md5_secret,dict):
                    flash("{}".format(md5_secret[0]))
                message_info = md5_secret
                return render_template(view, form=form, current_user=current_user, secret=message_info)
        elif form.__formname__ == "googleform":
            google_code = calGoogleCode(infos['google_number'])
            if isinstance(google_code,dict):
                flash("{}".format(google_code[0]))
            message_info = google_code
            return render_template(view, form=form, current_user=current_user, secret=message_info)

        elif form.__formname__ == 'asyncform':
            token = [eval(infos['token']) for _ in range(infos['number'])]
            method = infos['method'].upper()
            data = eval(infos['data'])
            result = main(infos['url'],data,token,method)
            if isinstance(result,dict):
                flash("{}".format(result[0]))
            message_info = result
            return render_template(view, form=form, current_user=current_user, secret=message_info)

    return render_template(view, form=form, current_user=current_user)

def run_tasks(DynamicModel,form,view):
    if form.validate_on_submit():
        infos = {}
        for wtf in form:
            infos[wtf.name] = wtf.data
        value = "DynamicModel.{}".format(infos['search_name'])
        model = DynamicModel.select().where(eval(value) == infos['search'])
        model_infos = utils.running_task(infos['choice_env'],model)
        flash('{}'.format(model_infos))
    return render_template(view,form=form,current_user=current_user)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in Config.ALLOWED_EXTENSIONS

def gen_file_name(filename):
    """
    If file was exist already, rename it and return a new name
    """

    i = 1
    while os.path.exists(os.path.join(Config.UPLOAD_FOLDER, filename)):
        name, extension = os.path.splitext(filename)
        filename = '%s_%s%s' % (name, str(i), extension)
        i += 1

    return filename

def create_thumbnail(image):
    try:
        base_width = 80
        img = Image.open(os.path.join(Config.UPLOAD_FOLDER, image))
        w_percent = (base_width / float(img.size[0]))
        h_size = int((float(img.size[1]) * float(w_percent)))
        img = img.resize((base_width, h_size), PIL.Image.ANTIALIAS)
        img.save(os.path.join(Config.THUMBNAIL_FOLDER, image))

        return True

    except:
        print(traceback.format_exc())
        return False

def input_task(filename):
    try:
        excel = ControlExcel(filename).read_excel()
        utils.excel_to_model(excel)
        return "{}用例上传成功！！".format(filename)
    except Exception as e:
        print(e)
        return "{}用例上传失败！！".format(filename)

def select_num(*DynamicModel):
    nums = []
    success, total = 0, 0
    for model in DynamicModel:
        query = model.select()
        total_count = query.count()
        nums.append(total_count)
        if model.__name__ == "Report":
            query = model.select()
            infos = utils.query_to_list(query)
            for info in infos:
                success = success + int(info['success_count'])
                total = total + int(info['success_count']) + int(info['fail_count']) + int(info['error_count'])
    else:
        nums.append(round(success/total,3) * 100)

    return nums


def changepassword(DynamicModel,view,form):
    model = DynamicModel()
    return render_template(view, form=form, current_user=current_user)