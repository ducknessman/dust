#！/usr/bin/env python
#! -*-coding:utf-8 -*-
#!@Author : zhuxx
#!@time : 2020/05/08 19:19

import datetime
import time

from dust.send import Request
from dust.compare import Compare
from dust.create_report import CreateReport
from dust.task_upload import UploadExcel
from dust.LogAnalysis.analysis import collection_words
from dust.control import cpu,cpu_percent_dict,memory,net_io,net_io_dict,disk,disk_dict

from pyecharts import options as opts
from pyecharts.charts import Line,Gauge,WordCloud
from pyecharts.globals import SymbolType

#折线图
def line_base(title,user,task,report,success,fail) -> Line:
    line = (
        Line()
        .add_xaxis([i for i in range(5)])
        .add_yaxis(
            series_name="用户人数",
            y_axis=[i for i in user],
            is_smooth=True,
            label_opts=opts.LabelOpts(is_show=False),
            color="black"
        )
        .add_yaxis(
            series_name="测试用例",
            y_axis=[i for i in task],
            is_smooth=True,
            label_opts=opts.LabelOpts(is_show=False),
            color="red"
        )
        .add_yaxis(
            series_name="报告数量",
            y_axis=[i for i in report],
            is_smooth=True,
            label_opts=opts.LabelOpts(is_show=False),
            color="blue"
        )
            .add_yaxis(
            series_name="成功数量",
            y_axis=[i for i in success],
            is_smooth=True,
            label_opts=opts.LabelOpts(is_show=False),
            color="orange"
        )
            .add_yaxis(
            series_name="失败数量",
            y_axis=[i for i in fail],
            is_smooth=True,
            label_opts=opts.LabelOpts(is_show=False),
            color="green"
        )
        .set_global_opts(
            title_opts=opts.TitleOpts(title="平台统计图"),
            xaxis_opts=opts.AxisOpts(type_="value",name='统计'),
            yaxis_opts=opts.AxisOpts(type_="value",name='数量'),
        )
    )
    return line

def cpu_line() -> Line:
    now = time.strftime('%Y{y}%m{m}%d{d} ').format(y='年', m='月', d='日的')
    cpu()
    c = (
        Line()
            .add_xaxis(list(cpu_percent_dict.keys()))
            .add_yaxis('', list(cpu_percent_dict.values()), areastyle_opts=opts.AreaStyleOpts(opacity=0.5))
            .set_global_opts(title_opts=opts.TitleOpts(title = now + "CPU负载",pos_left = "center"),
                             yaxis_opts=opts.AxisOpts(min_=0,max_=100,split_number=10,type_="value", name='%'))
    )
    return c

def memory_liquid() -> Gauge:
    mtotal, mused, mfree, stotal, sused, sfree, mpercent = memory()
    c = (
        Gauge()
            .add("", [("", mpercent)])
            .set_global_opts(title_opts=opts.TitleOpts(title="内存负载", pos_left = "right"))
    )
    return mtotal, mused, mfree, stotal, sused, sfree, c

def net_io_line() -> Line:
    net_io()

    c = (
    Line()
    .add_xaxis(net_io_dict['net_io_time'])
    .add_yaxis("发送字节数", net_io_dict['net_io_sent'], is_smooth=True)
    .add_yaxis("接收字节数", net_io_dict['net_io_recv'], is_smooth=True)
    .set_series_opts(
        areastyle_opts=opts.AreaStyleOpts(opacity=0.5),
        label_opts=opts.LabelOpts(is_show=False),
    )
    .set_global_opts(
        title_opts=opts.TitleOpts(title="网卡IO", pos_left = "center"),
        xaxis_opts=opts.AxisOpts(
            axistick_opts=opts.AxisTickOpts(is_align_with_label=True),
            is_scale=False,
            boundary_gap=False,
        ),
        yaxis_opts=opts.AxisOpts(type_="value", name='B/2S'),
        legend_opts=opts.LegendOpts(pos_left="left"),
    ))
    return c

def disk_line() -> Line:
    total, used, free = disk()

    c = (
        Line(init_opts=opts.InitOpts(width="1680px", height="800px"))
        .add_xaxis(xaxis_data=disk_dict['disk_time'])
        .add_yaxis(
            series_name="写入数据",
            y_axis=disk_dict['write_bytes'],
            areastyle_opts=opts.AreaStyleOpts(opacity=0.5),
            linestyle_opts=opts.LineStyleOpts(),
            label_opts=opts.LabelOpts(is_show=False),
        )
        .add_yaxis(
            series_name="读取数据",
            y_axis=disk_dict['read_bytes'],
            yaxis_index=1,
            areastyle_opts=opts.AreaStyleOpts(opacity=0.5),
            linestyle_opts=opts.LineStyleOpts(),
            label_opts=opts.LabelOpts(is_show=False),
        )
        .extend_axis(
            yaxis=opts.AxisOpts(
                name_location="start",
                type_="value",
                is_inverse=True,
                axistick_opts=opts.AxisTickOpts(is_show=True),
                splitline_opts=opts.SplitLineOpts(is_show=True),
                name='KB/2S'
            )
        )
        .set_global_opts(
            title_opts=opts.TitleOpts(
                title="磁盘IO",
                pos_left="center",
                pos_top="top",
            ),
            tooltip_opts=opts.TooltipOpts(trigger="axis", axis_pointer_type="cross"),
            legend_opts=opts.LegendOpts(pos_left="left"),
            xaxis_opts=opts.AxisOpts(type_="category", boundary_gap=False),
            yaxis_opts=opts.AxisOpts(type_="value", name='KB/2S'),
        )
        .set_series_opts(
            axisline_opts=opts.AxisLineOpts(),
        )
    )

    return total, used, free, c

#词云
def word_could() -> WordCloud:
    name,value = collection_words()
    data = [z for z in value.items()]
    wordcould = (
        WordCloud()
        .add(series_name=name,
             data_pair=data,
             word_size_range=[20,80],
             shape=SymbolType.DIAMOND)
        .set_global_opts(
            title_opts=opts.TitleOpts(title="{} 当日平台sql日志".format(name)),
        )
    )
    return wordcould

#列表转置
def rotate(infos):
    return list(zip(*infos))

#获取首页数据信息
def get_welcome_info(*models):
    now_time = datetime.datetime.now()
    now = datetime.datetime(now_time.year,now_time.month,now_time.day).strftime('%Y-%m-%d 00:00:00')
    tom_time = (datetime.date(now_time.year,now_time.month,now_time.day) + datetime.timedelta(days=-1)).strftime('%Y-%m-%d 00:00:00')
    week_time = (datetime.date(now_time.year,now_time.month,now_time.day) + datetime.timedelta(weeks=-1)).strftime('%Y-%m-%d 00:00:00')
    month_time = datetime.date(now_time.year,now_time.month - 1,now_time.day).strftime('%Y-%m-%d 00:00:00')
    user_model,task_model,report_model = models
    user_info = collection_db_info(user_model,now_time,now,tom_time,week_time,month_time)
    task_info = collection_db_info(task_model,now_time,now,tom_time,week_time,month_time)
    report_innfo = collection_db_info(report_model, now_time, now, tom_time, week_time, month_time)
    success_info,fail_info = get_collection_suc_fail(report_model,now_time,now,tom_time,week_time,month_time)
    infos = rotate([['总量','今日','昨日','本周','本月'],user_info,task_info,report_innfo,success_info,fail_info])
    return infos,[['sum','today','yesterday','week','month'],user_info,task_info,report_innfo,success_info,fail_info]

#获取首页数量
def collection_db_info(model,now_time,now,tom,week,month):
    counts = model.query.count()
    now_time = now_time.strftime('%Y-%m-%d %H:%M:%S')
    if model.__tablename__ == 'user':
        sql = 'model.reg_time.between("{}","{}")'
    elif model.__tablename__ == "tasks":
        sql = 'model.task_time.between("{}","{}")'
    else:
        sql = 'model.finished_time.between("{}","{}")'
    now_account = model.query.filter(eval(sql.format(now,now_time))).count()
    tom_account = model.query.filter(eval(sql.format(tom,now))).count()
    week_account = model.query.filter(eval(sql.format(week,now_time))).count()
    month_account = model.query.filter(eval(sql.format(month,now_time))).count()
    return [counts,now_account,tom_account,week_account,month_account]

#获取首页成功失败数量
def get_collection_suc_fail(model,now_time,now,tom,week,month):
    now_time = now_time.strftime('%Y-%m-%d %H:%M:%S')
    sqls = ['',
            'model.finished_time.between("{}","{}")'.format(now,now_time),
            'model.finished_time.between("{}","{}")'.format(tom,now),
            'model.finished_time.between("{}","{}")'.format(week,now_time),
            'model.finished_time.between("{}","{}")'.format(month,now_time)]
    suc_count,fail_count = [],[]
    for sql in sqls:
        success,fail = [],[]
        if sql == "":
            infos = model.query.all()
        else:
            infos = model.query.filter(eval(sql.format(tom,now))).all()
        for info in infos:
            success.append(info.success_count)
            fail.append(info.fail_count)
        suc_count.append(sum(success))
        fail_count.append(sum(fail))
    return suc_count,fail_count

#添加用例
def add_example(model,datas,db):
    if model.query.filter(model.task_son_id == datas['task_son_id']).first():
        data = {
            'msg': '用例子id重复',
            'status': '1002'
        }
    else:
        add_list = model(
            task_id=datas['task_id'],
            task_son_id=datas['task_son_id'],
            task_name=datas['task_name'],
            task_description=datas['task_description'],
            task_url=datas['task_url'],
            task_method=datas['task_method'].upper(),
            task_data=datas['task_data'],
            task_result=datas['task_result'],
            task_session=datas['task_session'],
            task_auth=datas['task_auth'],
            task_env=datas['task_env'],
            task_time=datas['task_time']
        )
        db.session.add(add_list)
        db.session.commit()
        data = {
            'msg': '修改成功',
            'status': '200'
        }
    return data

#添加执行用例
def add_running(model,datas,db):
    add_list = model(
        running_name=datas['running_name'],
        running_info=datas['running_info'],
        create_time = datas['create_time']
    )
    db.session.add(add_list)
    db.session.commit()
    data = {
        'msg': '修改成功',
        'status': '200'
    }
    return data

#通用删除
def common_del(model,ids,db):
    ids = ids.split(',')
    if ids:
        tasks = model.query.filter(model.id.in_(ids)).all()
        for task in tasks:
            db.session.delete(task)
            db.session.commit()
        data = {
            'msg':'删除成功',
            'status':'200'
        }
    else:
        data = {
            'msg':"删除失败，请联系管理员",
            'status':'1000'
        }
    return data

#用例执行
def task_run(model,model_result,model_report,model_env,ids,db):
    ids = ids.split(',')
    start_time = datetime.datetime.now()
    datas = {
        "testPass":0,
        "testResult": [],
        "testName":'',
        "testAll":0,
        "testFail": 0,
        "beginTime": start_time.strftime('%Y-%m-%d %H:%M:%S.%f'),
        "totalTime": "",
        "testSkip": 0,

    }
    result_model = {'success':"成功",'fail':"失败",'error':'跳过'}
    if ids:
        temp_status = []
        tasks = model.query.filter(model.id.in_(ids)).all()
        for task in tasks:
            print(task)
            if task.task_env == 0 or task.task_env == "":
                url = task.task_url
            elif task.task_env == 1:
                basic = model_env.query.filter(model_env.env_single==1).first()
                url = "{}/{}".format(basic, task.url)
            elif task.task_env == 2:
                basic = model_env.query.filter(model_env.env_single==2).first()
                url = "{}/{}".format(basic, task.url)
            else:
                basic = model_env.query.filter(model_env.env_single==3).first()
                url = "{}/{}".format(basic, task.url)

            task_id = task.task_id
            task_son_id = task.task_son_id
            data = task.task_data
            method = task.task_method
            cookies = task.task_session
            task_result = task.task_result
            running_start_time = time.time()
            response = Request().request(method,url,data,cookies)
            status = Compare().judge_type(task_result,response)
            add_common(db,model_result,task_id=task_id,task_son_id=task_son_id,task_url=url,
                       task_data=data,task_result=task_result,task_response=str(response),task_status=status,
                       finished_time=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f'))
            running_end_time = time.time()
            datas['testResult'].append({
                "className": "{}-{}-{}".format(task.task_name,task_id,task_son_id),
                "methodName": method,
                "description": task.task_description,
                "spendTime": running_end_time - running_start_time,
                "status": result_model[status],
                "log": ["this is result {}, this is response {}".format(task_result,response)]
            })
            temp_status.append(status)
            datas['testName'] = "{}_{}".format(task.task_id,start_time.strftime("%Y%m%d%H%M%S%f"))
        success,fail,error = collection_result(temp_status)
        datas['testPass'] = success
        datas['testAll'] = len(datas['testResult'])
        datas['testFail'] = fail
        datas['testSkip'] = error
        end_time = datetime.datetime.now()
        datas['totalTime'] = '{}s'.format((end_time - start_time).total_seconds())
        CreateReport().create(datas,datas['testName'])
        add_common(db,model_report,report_name=datas['testName'],success_count=success,
                   fail_count=fail,error_account=error,finished_time=end_time.strftime('%Y-%m-%d %H:%M:%S.%f'))
        info = {'msg':'用例执行已结束，测试报告请进行查收！','status':200}
        return info
    else:
        info = {'msg':'出现问题了！','status':1002}
        return info

#统计结果
def collection_result(statuses):
    success,fail,error = 0,0,0
    for status in statuses:
        if status == "success":
            success += 1
        elif status == "fail":
            fail += 1
        elif status == 'error':
            error += 1
    return success,fail,error

#添加测试结果
def add_common(db, model, **kwargs):
    info = model(**kwargs)
    db.session.add(info)
    db.session.commit()

#添加用户
def add_user(db, model, **kwargs):
    info = model(**kwargs)
    db.session.add(info)
    db.session.commit()

#修改用例
def edit_example(model,datas,db):
    update_info = datas
    db.session.query(model).filter_by(task_son_id=datas['task_son_id']).update(update_info)
    db.session.commit()
    data = {
        "msg": "已经提交成功",
        'status': 200
    }
    return data

#公共搜索方法
def search_info(model,sql,pages,db):
    info = db.session.query(model).filter(sql).paginate(pages,10)
    return info

#用力上传
def upload_task(db,model,filename):
    db.session.execute(
        model.__table__.insert(),
        list(UploadExcel(filename).read_excel())
    )
    db.session.commit()