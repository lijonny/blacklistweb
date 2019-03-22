#coding:utf8
from flask_sqlalchemy import SQLAlchemy
db=SQLAlchemy()
class blacklist(db.Model):
    __tablename__='blacklist'
    idcard = db.Column(db.String(18),primary_key=True,unique=True)
    mac = db.Column(db.String(20),unique=True)
    imsi = db.Column(db.String(20),nullable=False)
    imei = db.Column(db.String(20),nullable=False)
    passport = db.Column(db.String(20))
    name = db.Column(db.String(20),nullable=False)
    def __init__(self,idcard,mac,imsi,imei,passport,name):
        self.idcard = idcard
        self.mac = mac
        self.imei = imei
        self.imsi = imsi
        self.passport = passport
        self.name = name
class blacklist3suo(db.Model):
    __tablename__ ='blacklist3suo'
    idcard = db.Column(db.String(19),unique=True)

