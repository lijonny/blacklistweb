#coding:utf8
import json
import base64
import requests
import os
url = "http://10.0.1.107:8080/face_recognition_cloud/v1.0/search"

def getIDbyImei(imei,blacklist):
    if len(imei)>0:
        for bl in blacklist:
            if bl['imei']==imei:
                return bl['idcard']
    return None
def getIDbyMac(mac,blacklist):
    if len(mac)>0:
        for bl in blacklist:
            if bl['mac']==mac:
                return bl['idcard']
    return '111222333444555'
def getIDbyImsi(imsi,blacklist):
    if len(imsi)>0:
        for bl in blacklist:
            if bl['imsi']==imsi:
                return bl['idcard']
    return None


def getColorFromID(id,blacklisthelu):
    for bl in blacklisthelu:
        if bl['idcard'] == id:
            return bl['color']
    return None


def getTypeFromID(id,blacklisthelu):
    for bl in blacklisthelu:
        if bl['idcard'] == id:
            return bl['type']

    return None
def getIDFromResult(searchResult,count):
    try:
        ids = []
        result = json.loads(searchResult)
        for i in range(0,count):
            id ={'id':'','score':0}
            id['id'] = result.get('data',"")[i]["id"]
            id['score'] = result.get('data',"")[i]["similarity"]
#            print "%d------%s"%(i,id)
            ids.append(id)
        return ids
    except Exception:
        return None

def base64tojpg(data,jpgfile):
    if len(data)>0:
        base64data = base64.b64decode(data)
        file = open(jpgfile,'wb')
        file.write(base64data)
        file.close()
        return True
    return False
def jpgtobase64(jpgfile):
    f=open(jpgfile,'rb') #二进制方式打开图文件
    ls_f=base64.b64encode(f.read()) #读取文件内容，转换为base64编码
    f.close()
    return ls_f

def searchFile(pic,count):
    payload = {"api_key":"TeZhen2","api_secret":"111","group_name":"16201h","count":count}
    f = {"image":open(pic, 'rb')}
    response = requests.request("POST", url, data=payload, files=f)
 #   print response.text
    return response.text
def getNameFromID(id,idlist):
    for bl in idlist:
        if bl['idcard'] == id:
            return bl['name']
    return u'测试人员'

def getIMGFromID(id,idlist):
    for bl in idlist:
        if bl['idcard'] == id:
            jpgfile = id + '.jpg'
            jpgpath = os.path.join(os.getcwd(),jpgfile)
            bl['image'] = jpgtobase64(jpgpath)
            return bl['image']
    return ''

