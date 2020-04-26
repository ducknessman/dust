#！/usr/bin/env python
#! -*-coding:utf-8 -*-
#!@Author : zhuxx
#!@time : 2020/04/20 11:01

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField, PasswordField, SelectField, IntegerField
from wtforms.validators import DataRequired, Length, InputRequired

class MyStringField(StringField):
    def __init__(self,label=None, validators=None, **kwargs):
        super(MyStringField, self).__init__(label, validators, **kwargs)
        self.false_values = (' ',"",None,False)

    def process_formdata(self, valuelist):
        print(valuelist)
        if not valuelist or valuelist[0] == "" or valuelist[0] is None:
            self.data = self.default
        elif valuelist[0] in self.false_values:
            self.data = ''
        else:
            self.data = valuelist[0].strip(" ")


class UserForm(FlaskForm):
    username = StringField('用户名', validators=[DataRequired(message='不能为空'), Length(0, 64, message='长度不正确')])
    password = StringField('密码', validators=[DataRequired(message='不能为空'), Length(0, 64, message='长度不正确')])
    fullname = StringField('全称', validators=[DataRequired(message='不能为空'), Length(0, 64, message='长度不正确')])
    email = StringField('邮箱', validators=[DataRequired(message='不能为空'), Length(0, 64, message='长度不正确')])
    phone = StringField('电话', validators=[DataRequired(message='不能为空'), Length(0, 64, message='长度不正确')])
    status = BooleanField('生效标识', default=True)
    submit = SubmitField('提交')


class TaskFrom(FlaskForm):
    task_id = StringField('用例编号',validators=[DataRequired(message='不能为空')])
    task_son_id = StringField('用例子编号', validators=[DataRequired(message='不能为空'),])
    task_url = StringField('url', validators=[DataRequired(message='不能为空')])
    task_method = SelectField('method', choices=[('POST', 'POST'), ('GET', 'GET'),('PUT', 'PUT'),('DEL', 'DELETE')],
                              validators=[DataRequired(message='不能为空')])
    task_name = StringField('用例名称', validators=[DataRequired(message='不能为空')])
    task_data = StringField('请求数据', validators=[DataRequired()])
    auth_name = StringField('执行人',validators=[DataRequired()])
    task_future_result = StringField('预期结果', validators=[DataRequired(message='不能为空')])
    status = BooleanField('生效标识', default=True)
    submit = SubmitField('提交')


class SearchForm(FlaskForm):
    search_name = SelectField('查询字段', choices=[('id', 'id'), ('task_id', 'task_id'), ('task_name', 'task_name')],
                              validators=[DataRequired(message='不能为空')])
    choice_env = SelectField('选择环境变量', choices=[('common',"common"),('stage', 'http://bkex.co'),
                                                ('dev', 'http://bkex.co'),
                                                ('alpha', 'http://bkex.co'),
                                                ('real', 'http://www.bkex.co')],
                              validators=[DataRequired(message='不能为空')])
    search = StringField('查询内容', default="",validators=[DataRequired(message='不能为空')])
    run = SubmitField('运行')


class ReportFrom(FlaskForm):
    task_name = StringField('用例名称', validators=[DataRequired(message='不能为空')])
    report_id = IntegerField('报告编号', validators=[DataRequired(message='不能为空')])
    success_count = IntegerField('成功次数', validators=[DataRequired(message='不能为空')])
    fail_count = IntegerField('失败次数', validators=[DataRequired(message='不能为空')])
    error_count = IntegerField('错误次数', validators=[DataRequired(message='不能为空')])
    finish_time = StringField('完成时间', validators=[DataRequired(message='不能为空')])

class PostManFrom(FlaskForm):
    task_url = StringField('url', validators=[DataRequired(message='不能为空')])
    task_method = SelectField('method', choices=[ ('GET', 'GET'),('POST', 'POST'),('PUT', 'PUT'),('DEL', 'DELETE')],
                              validators=[DataRequired(message='不能为空')])
    task_name = StringField('用例名称', validators=[DataRequired(message='不能为空')])
    header = MyStringField('请求数据', default=" ",validators=[InputRequired()])
    data = MyStringField('请求数据', default=" ",validators=[InputRequired()])
    cookies = MyStringField('请求数据', default=" ", validators=[InputRequired()])
    # param_type_choice = SelectField('type', choices=[('application/json', 'application/json'),
    #                                            ('text/plain', 'text/plain'),
    #                                            ('application/xml', 'application/xml')],
    #                           validators=[DataRequired()])
    # param_type = StringField('type', validators=[DataRequired()])
    status = BooleanField('生效标识', default=True)
    submit = SubmitField('发送')


class SecretFrom(FlaskForm):
    __formname__ = "Secret"
    secret_name = SelectField('加密方式', choices=[ ('md5', 'md5'),('ras', 'ras')],
                              validators=[DataRequired(message='不能为空')])
    private_key = MyStringField('private_key',default=" ", validators=[InputRequired()])
    public_key = MyStringField('public_key',default=" ", validators=[InputRequired()])
    secret = StringField('加密字段', validators=[DataRequired(message='不能为空')])
    submit = SubmitField('运行')


class GoogleFrom(FlaskForm):
    __formname__ = "googleform"
    google_number = StringField('Google验证码', validators=[DataRequired(message='不能为空')])
    submit = SubmitField('开始')


class Concurrency(FlaskForm):
    __formname__ = "concurform"
    url = StringField('url', validators=[DataRequired(message='不能为空')])
    number = IntegerField('并发数量', validators=[DataRequired(message='不能为空')])
    data = StringField('data', validators=[DataRequired(message='不能为空')])
    submit = SubmitField('开始')


class AsynchronousForm(FlaskForm):
    __formname__ = "asyncform"
    url = StringField('url', validators=[DataRequired(message='不能为空')])
    number = IntegerField('并发数量', validators=[DataRequired(message='不能为空')])
    data = StringField('data', default={},validators=[DataRequired(message='不能为空')])
    token = StringField('token', default={},validators=[DataRequired(message='不能为空')])
    method = SelectField('method', choices=[('GET', 'GET'), ('POST', 'POST'), ('PUT', 'PUT'), ('DEL', 'DELETE')],
                         validators=[DataRequired(message='不能为空')])
    submit = SubmitField('开始')


class ComparePicture(FlaskForm):
    pass

class ChangePassword(FlaskForm):
    password = StringField('password', validators=[DataRequired(message='不能为空')])
    change_password = StringField('password', validators=[DataRequired(message='不能为空')])
    again_password = StringField('password', validators=[DataRequired(message='不能为空')])
    submit = SubmitField('提交')