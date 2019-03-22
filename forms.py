#coding:utf8
from flask_wtf import FlaskForm
from wtforms import StringField,RadioField,IntegerField,FloatField,SubmitField
from wtforms.validators import InputRequired,length,DataRequired

class SuoForm(FlaskForm):
    #构建add三所表单
    idcard = StringField(label=u'身份证号',validators=[InputRequired(u'身份证号不能为空'),length(18,18,u'请输入合法的身份证号码')])
    submit = SubmitField('Register')
class BlacklistForm(FlaskForm):
    idcard = StringField(label=u'身份证号',validators=[InputRequired(u'身份证号不能为空'),length(18,18)])
    name = StringField(label=u'姓名', validators=[InputRequired(u'姓名不能为空')])
    mac = StringField(label=u'mac地址',validators=[InputRequired(u'mac地址不能为空')])
    imsi = StringField(label=u'imsi码',validators=[InputRequired(u'imsi码不能为空')])
    imei = StringField(label=u'imei码',validators=[InputRequired(u'imei码不能为空')])
    passport = StringField(label=u'passport',validators=[InputRequired(u'passport不能为空')])

class PersonForm(FlaskForm):
    idcard = StringField(label=u'身份证号', validators=[InputRequired(u'身份证号不能为空'), length(18, 18, u'请输入合法的身份证号码')])
    name = StringField(label=u'姓名', validators=[InputRequired(u'姓名不能为空')])
    sex = RadioField(label=u'性别',choices=[('m',u'男'),('f',u'女')])
    birthday = IntegerField(label=u'生日',validators=[InputRequired(u'生日不能为空')])
    nationality = StringField(label=u'国籍',validators=[InputRequired(u'国籍不能为空')])
    nation = StringField(label=u'民族',validators=[InputRequired(u'民族不能为空')])
    address = StringField(label=u'地址',validators=[InputRequired(u'地址不能为空')])
    passport_type = RadioField(label=u'护照类型',choices=[(u'普通护照',u'普通护照')])
    passport_id = StringField(label=u'护照id',validators=[InputRequired(u'护照id不能为空')])
    score = FloatField(label=u'分数',validators=[InputRequired(u'分数不能为空')])
    image = StringField(label=u'照片')
class IdlistForm(FlaskForm):
    idcard = StringField(label=u'身份证号', validators=[InputRequired(u'身份证号不能为空'), length(18, 18, u'请输入合法的身份证号码')])
    name = StringField(label=u'姓名', validators=[InputRequired(u'姓名不能为空')])
    img = StringField(label=u'照片')



