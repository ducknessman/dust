#！/usr/bin/env python
#! -*-coding:utf-8 -*-
#!@Author : zhuxx
#!@time : 2020/04/24 11:10

from pyecharts import options as opts
from pyecharts.charts import Line,Pie,WordCloud
from pyecharts.globals import SymbolType


def line_base(time_point:list,success:list,fail:list,error:list) -> Line:
    line = (
        Line()
        .add_xaxis(["{}".format(i) for i in time_point])
        .add_yaxis(
            series_name="success",
            y_axis=[i for i in success],
            is_smooth=True,
            label_opts=opts.LabelOpts(is_show=False),
            color="yellow"
        )
        .add_yaxis(
            series_name="fail",
            y_axis=[i for i in fail],
            is_smooth=True,
            label_opts=opts.LabelOpts(is_show=False),
            color="red"
        )
        .add_yaxis(
            series_name="error",
            y_axis=[i for i in error],
            is_smooth=True,
            label_opts=opts.LabelOpts(is_show=False),
            color="green"
        )
        .set_global_opts(
            title_opts=opts.TitleOpts(title="测试用例执行统计"),
            xaxis_opts=opts.AxisOpts(type_="value",name='report_id'),
            yaxis_opts=opts.AxisOpts(type_="value",name='数量'),
        )
    )
    return line


def pie_base(task_name,value:dict) -> Pie:
    amount = sum(value.values())
    value_percent = {'success':round(value['success']/amount,2) * 100,
                     'fail':round(value['fail']/amount,2) * 100,
                     'error':round(value['error']/amount,2) * 100}
    pie = (
        Pie()
        .add(series_name=task_name,
             data_pair=[list(z) for z in value.items()],
             radius=["30%", "65%"],
             center=["35%", "50%"],
             label_opts=opts.LabelOpts(formatter="{b}: {c}"))
        .add(series_name="",
             data_pair=[list(z) for z in value_percent.items()],
             radius=["30%", "65%"],
             center=["75%", "50%"],
             label_opts=opts.LabelOpts(formatter="{b}: {c}%")
             )
        .set_colors(["blue", "red", "pink"])
        .set_global_opts(title_opts=opts.TitleOpts(title="{} 饼状图统计展示".format(task_name))
                                                   )
    )
    return pie


def word_could(task_name,value:dict) -> WordCloud:
    data = [z for z in value.items()]
    wordcould = (
        WordCloud()
        .add(series_name=task_name,
        data_pair=data,
        word_size_range=[20, 80],
        shape=SymbolType.DIAMOND,
        )
        .set_global_opts(
            title_opts=opts.TitleOpts(title="{} 测试报告-词频展示".format(task_name)),
            )
    )
    return wordcould