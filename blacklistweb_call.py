#!/usr/bin/python
# -*- coding: utf-8 -*-
from flask import Flask,request,render_template,Response
import json
import time
import os,base64
import requests
import random
from gevent import monkey
from gevent.pywsgi import WSGIServer
from geventwebsocket.handler import WebSocketHandler

monkey.patch_all()

app = Flask(__name__)

app.config.update(
    DEBUG=True
)

blacklist = [
        {'idcard':'430681198309180335:650304','mac':'bc:4c:c4:f1:9c:06','imsi':'460023996616776','imei':'86678402040959','passport':'G31035926','name':'李智'},#李智
#	{'idcard':'371327198809051863:650304','mac':'64:09:80:fe:cc:f8','imsi':'11221','imei':'22233','passport':'E90801766','name':'杜红艳'},#杜红艳
	{'idcard':'371327198809051863','mac':'64:09:80:fe:cc:f8','imsi':'11221','imei':'22233','passport':'E90801766','name':'杜红艳'},#杜红艳
#	{'idcard':'620503199309038035','mac':'bc:4c:c4:f1:9c:37','imsi':'11221','imei':'22233','passport':'E90801766','name':'鸟叔'},#鸟叔
	{'idcard':'13092319931013261X:650304','mac':'bc:4c:c4:f1:9c:27','imsi':'11111','imei':'22222','passport':'E90801765','name':'陈贵杰'},#陈贵杰
#	{'idcard':'110110199001010339','mac':'bc:4c:c4:f1:9c:07','imsi':'33333','imei':'44444','passport':'E90801766','name':'胖哥'},#老李
#        {'idcard':'622421199603243813','mac':'90:f0:52:01:d8:e2','imsi':'460021035158615','imei':'86678402040951','passport':'','name':'周武'},#周武
	{'idcard':'22028219931203411X:650304','mac':'90:f0:52:01:d8:e2','imsi':'460021035158615','imei':'86678402040951','passport':'','name':'刘彦宇'}, #lyy\
	{'idcard':'22028219931203411X','mac':'90:f0:52:01:d8:e2','imsi':'460021035158615','imei':'86678402040951','passport':'','name':'刘彦宇'}, #lyy\

#	{'idcard':'21021319791203251X','mac':'d8:9a:34:18:54:2f','imsi':'1111','imei':'1231231','passport':'','name':'刘邦文'},
#        {'idcard':'22072119871022121X','mac':'11','imsi':'22','imei':'33','passport':'','name':'黄志刚'},
#	{'idcard':'210106197612252730:650304','mac':'d8:9a:34:28:24:4f','imsi':'123122344112445','imei':'87779881923411','passport':'S00140405','name':'李超宁'},#lichn
	{'idcard':'210106197612252730','mac':'d8:9a:34:28:24:4f','imsi':'123122344112445','imei':'87779881923411','passport':'S00140405','name':'李超宁'},#lixin
	{'idcard':'11010519830716611X','mac':'d8:9a:34:28:24:4f','imsi':'123122344112445','imei':'87779881923411','passport':'S00140405','name':'zhouyangyang'},#zhouyangyang
]
blacklisthelu = [
        {'idcard':'430681198309180335','color':'红色','type':'在逃人员'},
        {'idcard':'22028219931203411X','color':'黄色，绿色','type':'养犬人员'},
        {'idcard':'22028219931203411X0','color':'黄色','type':'吸毒人员，违法犯罪'}
]

blacklist_helu = [ '430681198309180335','322028219931203411X' ]
blacklist_jcz = ['430681198309180335','322028219931203411X','22072119871022121X']

idlist = [
        {'idcard':'430681198309180335','name':'二维识别结果李智','img':''},#李智\
        {'idcard':'410181198905081535','name':'李思远','img':''},#李思远
        {'idcard':'430223198603117219','name':'老李','img':''},#老李
        {'idcard':'22028219931203411X','name':'刘彦宇','img':''}, #lyy\
      #  {'idcard':'220282199312034115','name':'测试'},
	{'idcard':'210113198307270017','name':'程学武','img':''},
      #  {'idcard':'120101198108191511','name':'王鹏','img':''},
        {'idcard':'130682199206044816','name':'李超宁','img':''},#lichn
]

url = "http://10.0.1.107:8080/face_recognition_cloud/v1.0/search"

number = 0

data1v1 = {"status":"0","message":"成功","data":[]}
dataPerson = [
{"id":"430681198309180335","name":"","sex":"男","birthday":"19830918","nationality":"中国","nation":"维吾尔族","address":"北京的卢","passport_type":"普通护照","passport_id":"G31035926","score":89.1,"image":''},
{"id":"220282199312034115","name":"","sex":"男","birthday":"20161122","nationality":"中国","nation":"汉族","address":"北京的卢","passport_type":"普通护照","passport_id":"E12334555","score":70.2,"image":''}, 
{"id":"41018119890508153X","name":"","sex":"男","birthday":"20161122","nationality":"中国","nation":"汉族","address":"北京的卢","passport_type":"普通护照","passport_id":"E12334555","score":65.04,"image":'' },
{"id":"130682199206044816","name":"","sex":"男","birthday":"20161122","nationality":"中国","nation":"汉族","address":"北京的卢","passport_type":"普通护照","passport_id":"E12334555","score":63.04,"image":'' }]

for i in range(0,30):
    data = {"id":i,"name":"","sex":"男","birthday":"19830918","nationality":"中国","nation":"维吾尔族","address":"北京的卢","passport_type":"普通护照","passport_id":"G31035926","score":89.1,"image":''}
    dataPerson.append(data)

#current_time = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
#logfile = open("result_%s.txt"%(current_time),'rw')

blacklist3suo = ['#430681198309180335','#22028219931203411X','#130682199206044816']

blacklist_idcard = []
blacklist_mac = []
blacklist_imei = []
blacklist_imsi = []
blacklist_passport = []
for bl in blacklist:
    blacklist_idcard.append(bl['idcard'])
    blacklist_mac.append(bl['mac'])
    blacklist_imei.append(bl['imei'])
    blacklist_imsi.append(bl['imsi'])
    blacklist_passport.append(bl['passport'])
vacationlist = ['410181198905081535','22028219931203411XTTT','61032319911025001','430681198309180335','G31035926']
inBlackListData = {"status":"0","message":"success","jobId":"CC0000005963AD750159721904E33780","isBlackList":1}
outBlackListData = {"status":"0","message":"success","jobId":"CC0000005963AD750159721904E33780","isBlackList":0}

sjmpt_idlist = ['430681198309180335','22028219931203411X','610323199110250015','110110199001010339','652927199011132168']
device_list = ['Device1','Device2']

def getColorFromID(id):
    for bl in blacklisthelu:
        if bl['idcard'] == id:
            return bl['color']
    return None

def getTypeFromID(id):
    for bl in blacklisthelu:
        if bl['idcard'] == id:
            return bl['type']
        
    return None

def getNameFromID(id):
    for bl in idlist:
        if bl['idcard'] == id:
            return bl['name']
    return '测试人员'

def getIMGFromID(id):
    for bl in idlist:
        if bl['idcard'] == id:
            jpgfile = id + '.jpg'
            jpgpath = os.path.join(os.getcwd(),jpgfile)
            bl['image'] = jpgtobase64(jpgpath)
            return bl['image']
    return ''

def searchFile(pic,count):
    payload = {"api_key":"TeZhen2","api_secret":"111","group_name":"16201h","count":count}
    f = {"image":open(pic, 'rb')}
    response = requests.request("POST", url, data=payload, files=f)
 #   print response.text
    return response.text

def jpgtobase64(jpgfile):
    f=open(jpgfile,'rb') #二进制方式打开图文件
    ls_f=base64.b64encode(f.read()) #读取文件内容，转换为base64编码
    f.close()
    return ls_f

def base64tojpg(data,jpgfile):
    if len(data)>0:
        base64data = base64.b64decode(data)
        file = open(jpgfile,'wb')
        file.write(base64data)
        file.close() 
        return True
    return False

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
    except Exception,e:
        return None



def getIDbyMac(mac):
    if len(mac)>0:
        for bl in blacklist:
            if bl['mac']==mac:
                return bl['idcard']
    return '111222333444555'

def getIDbyImei(imei):
    if len(imei)>0:
        for bl in blacklist:
            if bl['imei']==imei:
                return bl['idcard']
    return None

def getIDbyImsi(imsi):
    if len(imsi)>0:
        for bl in blacklist:
            if bl['imsi']==imsi:
                return bl['idcard']
    return None


@app.route('/3suo', methods=['GET', 'POST']) 
def template3suo():
    if request.method == 'POST':
#        time.sleep(5)       
#        print "request data is %s"%request.get_data()
        postdata = json.loads(request.get_data())
        id = postdata.get('cardNo',"")
        if id in blacklist3suo:
#            print inBlackListData
            return json.dumps(inBlackListData)
        else:
            return json.dumps(outBlackListData)
    else:
        return '200 OK'

@app.route('/3hui', methods=['GET', 'POST'])
def template3hui():
    if request.method == 'GET':
        #time.sleep(4)
	global number 
	number = number + 1
	app.logger.info("%s - NO.%d"%(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())),number))
#        app.logger.info('%d'%number)
        ids = request.args.get('id')
        print ids
        datalist = {"msg":u"品恩、海康身份证接口调用成功!"+os.path.abspath(os.path.dirname(__file__)),"data":[]}
        if ids is None or len(ids) <1:
            return "Notice:none input"
#        print "id length is %d"%len(ids) 
        for id in ids.split(','):
#            print "id length is %d"%len(ids)
            if id in blacklist_idcard:
		#time.sleep(20)
                sanhuiinBlacklistData = {"id":id,"message":u"(测试布控信息)进一步落地监控，防止造成危害%s"%id,"tag":u"(测试Tag)一体化录入人员%s"%id,\
                "flag":('1' if getIDbyMac(id) in vacationlist else '0'),"reserved1":u"(测试布控标签)res1%s"%id,"reserved2":u"(测试处置意见)res2发现即抓捕%s，同时通知原籍公安机关"%id,"reserved3":"res3","reserved4":"idcard","reserved5":"1:null+asd12345"}
                datalist["data"].append(sanhuiinBlacklistData)
            elif id in blacklist_mac:
#            elif id.find(':')>0:
                sanhuiinBlacklistData = {"id":id,"message":u"进一步落地监控，防止造成危害","tag":u"一体化录入人员",\
                "flag":"0","reserved1":u"不放心人员","reserved2":u"信息采集","reserved3":getIDbyMac(id),"reserved4":"mac","reserved5":"res5"}
                datalist["data"].append(sanhuiinBlacklistData)
            elif id in blacklist_imei:
                sanhuiinBlacklistData = {"id":id,"message":u"进一步落地监控，防止造成危害","tag":u"[一体化录入人员]的同家族人员|一体化录入人员|不准出境人员|危安管控对象",\
                "flag":"","reserved1":u"一体化布控","reserved2":u"发现即抓捕，同时通知原籍公安机关","reserved3":getIDbyImei(id),"reserved4":"imei","reserved5":'"null"'}
                datalist["data"].append(sanhuiinBlacklistData)
            elif id in blacklist_imsi:
                sanhuiinBlacklistData = {"id":id,"message":u"进一步落地监控，防止造成危害","tag":u"[一体化录入人员]的同家族人员|一体化录入人员|不准出境人员|危安管控对象",\
                "flag":"","reserved1":u"一体化布控","reserved2":u"发现即抓捕，同时通知原籍公安机关","reserved3":getIDbyImsi(id),"reserved4":"imsi","reserved5":'"null"'}
                datalist["data"].append(sanhuiinBlacklistData)
        #print datalist
        return json.dumps(datalist,ensure_ascii=False)
        #return str(datalist)
    else:
        return "200 OK"

@app.route('/helu',methods=['GET', 'POST'])
def templatehelu():
    if request.method == 'GET':
        time.sleep(1)
        key = request.args.get('key')
        print key
        if key is None or len(key)<1:
            return "Notice:none input"

        datalist = {"color":"","type":""}
       # print key
       # print blacklisthelu
        if key in blacklist_helu:
            datalist["color"] = getColorFromID(key)+'color'
            datalist["type"] = getTypeFromID(key)+'type'
        else:
            datalist = {"color":"none"}
   # return json.dumps(datalist,ensure_ascii=False)
        r = Response(json.dumps(datalist,ensure_ascii=False))
        r.headers["Content-Type"]="application/json"
        return r
        #return '{"color":"黄色"  "type":"违法犯罪"}'

@app.route('/jcz',methods=['GET', 'POST'])
def templatejcz():
    if request.method == 'GET':
        time.sleep(1)
        key = request.args.get('key')
        print key
        if key is None or len(key)<1:
            return "Notice:none input"

        datalist = {"color":"","type":""}
       # print key
       # print blacklisthelu
        if key in blacklist_jcz:
            datalist["color"] = getColorFromID(key)+'jcz'
            datalist["type"] = getTypeFromID(key)+'jcz'
        else:
            datalist = {"color":"none"}
   # return json.dumps(datalist,ensure_ascii=False)
        r = Response(json.dumps(datalist,ensure_ascii=False))
        r.headers["Content-Type"]="application/json"
        return r


@app.route('/huzhao', methods=['GET', 'POST']) 
def templatehuzhao():
    if request.method == 'POST':
#        time.sleep(5)       
#        print "request data is %s"%request.get_data()
        postdata = json.loads(request.get_data())
        type = postdata.get('type',"")
        ids = postdata.get('id',"")
        datalist = {"status":"0","message":"成功","data":[]}
        if len(ids)==0:
            datalist = {"status":"1","message":"失败","data":[]}
            return json.dumps(datalist,ensure_ascii=False)
        if type==0:           #身份证
            for id in ids:
                if id in blacklist_idcard:
    #                print id
                    sanhuiinBlacklistData = {"id":id,"message":u"进一步落地监控，防止造成危害","tag":u"[一体化录入人员]的同家族人员|一体化录入人员|不准出境人员|危安管控对象",\
                    "flag":('1' if id in vacationlist else '0'),"reserved1":u"一体化布控","reserved2":u"发现即抓捕，同时通知原籍公安机关","reserved3":"","reserved4":"idcard","reserved5":""}
                    datalist["data"].append(sanhuiinBlacklistData)
        elif type==1:         #护照
            for id in ids:
                if id in blacklist_passport:
                    sanhuiinBlacklistData = {"id":id,"message":u"进一步落地监控，防止造成危害","tag":u"[一体化录入人员]的同家族人员|一体化录入人员|不准出境人员|危安管控对象",\
                    "flag":('1' if id in vacationlist else '0'),"reserved1":u"一体化布控","reserved2":u"发现即抓捕，同时通知原籍公安机关","reserved3":"","reserved4":"passport","reserved5":""}
                    datalist["data"].append(sanhuiinBlacklistData)
        return json.dumps(datalist)


@app.route('/1vn', methods=['GET', 'POST']) 
def template1v1():
    if request.method == 'POST':
#        time.sleep(15)
        data1v1["data"] = []
        postdata = json.loads(request.get_data())
#        print postdata
        count = postdata.get('count',1)
        faceImg = postdata.get('faceImg',"")
       # print 'count is %d'%count
        base64tojpg(faceImg,'test.jpg')
        ret = searchFile('test.jpg',count)
        #print ret
        ids = getIDFromResult(ret,count)
        for i in range(0,count):
            dataPerson[i]['id'] = ids[i]['id']
            dataPerson[i]['name'] = getNameFromID(ids[i]['id'])
            dataPerson[i]['image'] = getIMGFromID(ids[i]['id'])
            dataPerson[i]['score'] = ids[i]['score']*100
            data1v1["data"].append(dataPerson[i])
        print data1v1
        r = Response(json.dumps(data1v1))
        r.headers["Content-Type"]="application/json,charset=utf-8"
        return r

@app.route('/1vnFake', methods=['GET', 'POST'])
def template1vnFake():
    if request.method == 'POST':
        time.sleep(1.7)
#        print 'start to get haikang fake'
        data1v1["data"] = []
        postdata = json.loads(request.get_data())
#       app.logger.info("%s - count is %s"%(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())),count))
#        print postdata
        count = int(postdata.get('count',1))
        app.logger.info("%s - count is %s"%(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())),count))

#        faceImg = postdata.get('faceImg',"")
#        print 'count is %d'%count
#        base64tojpg(faceImg,'test.jpg')
#        ret = searchFile('test.jpg',count)
        #print ret
        ids = [{'id':'430681198309180335','score':90.22},{'id':'410181198905081535','score':70.1},{'id':'22028219931203411X','score':35.1}]
       #ids = [{'id':'853225199406092025','score':80.22},{'id':'410181198905081535','score':70.1},{'id':'22028219931203411X','score':55.1}]
        for j in range(0,30):
            idJ= {'id':j,'score':55.1-j}
            ids.append(idJ)

        for i in range(0,count):
            dataPerson[i]['id'] = ids[i]['id']
            dataPerson[i]['name'] = getNameFromID(ids[i]['id'])
            dataPerson[i]['image'] = getIMGFromID(ids[i]['id'])
            dataPerson[i]['score'] = ids[i]['score']
            data1v1["data"].append(dataPerson[i])
#        print data1v1
#        datatest = {"status":"0","message":"成功","data":[{"name":"李"}]}

        r = Response(json.dumps(data1v1,ensure_ascii=False))
#        r = Response("test")
#        r = Response(json.dumps(datatest,ensure_ascii=False))
        r.headers["Content-Type"]="application/json,charset=utf-8"
        return r

@app.route('/3d1vnFake', methods=['GET', 'POST'])
def template3d1vnFake():
    if request.method == 'POST':
        time.sleep(0.4)
        data1vn = {"code":"0","msg":"OK","time":"450","data":[{"similarity":0.9534053373336792,"id":"654125199508666623","id_type":"1","image_url":"http://10.0.1.86:8080/photo/5ab8bd4d5722f23bedf6bdb6","id_card_image_url":"http://10.0.1.86:8080/photo/5ab8bd4d5722f23bedf6bdb8","texture_url":"http://10.0.1.86:8080/photo/5ab8bd4d5722f23bedf6bdba","model_url":"http://10.0.1.86:8080/photo/5ab8bd4d5722f23bedf6bdbc","name":"巴革江·巴合提1","gender":"男","birthday":"1995-08-13","ethnicity":"哈萨克族","id_card_image":"","address":"新疆新源县别斯托别乡卡普河牧业村233号"}]}
        data1vn["data"][0]["id_card_image"] = jpgtobase64("120101198108191511_idcardimage.jpg")
        r = Response(json.dumps(data1vn,ensure_ascii=False))
        r.headers["Content-Type"]="application/json,charset=utf-8"
        return r


@app.route('/compare', methods=['GET', 'POST'])
def templateCompare():
    if request.method == 'POST':
        ran = random.randint(1, 10)
        data_success = { "data": { "similarity": (0.9 if ran < 9 else 0.5), "distance":1.00123 }, "code":"0", "msg":"OK" }
        data_fail =  { "code":"10001","msg":"Invalid Parameter (detailed info)" }
        data = {} 
        if ran == 5:
            data = data_fail
        else:
            data = data_success
        r = Response(json.dumps(data))
        r.headers["Content-Type"]="application/json,charset=utf-8"
        return r

@app.route('/evaluation', methods=['GET', 'POST'])
def templateEvaluation():
    if request.method == 'POST':
        data_success = { "data": { "score":random.randint(0,10) }, "code":"0", "msg":"OK" }
        data_fail =  { "code":"10001","msg":"Invalid Parameter (detailed info)" }
        data = {}
        ran = random.randint(1, 10)
        if ran == 5:
            data = data_fail
        else:
            data = data_success
        r = Response(json.dumps(data))
        r.headers["Content-Type"]="application/json,charset=utf-8"
        return r


@app.route('/verifyperson', methods=['GET', 'POST'])
def templateVerifyperson():
    if request.method == 'POST':
        data_success = { "data": { "score":random.uniform(0.5,1),"similarity":random.uniform(0.79,1), "compareok": 1 }, "code":"0", "msg":"OK" }
        data_fail =  { "data": { "score":-1,"similarity":random.uniform(0.5,0.78), "compareok": 0 }, "code":"0", "msg":"OK" }
        data = {}
        ran = random.randint(1, 10)
        if ran == 5 or ran==2:
            data = data_fail
        else:
            data = data_success
        r = Response(json.dumps(data))
        r.headers["Content-Type"]="application/json,charset=utf-8"
        return r

@app.route('/search',methods=['GET','POST'])
def search():
    time.sleep(5)
    data = {
    "code": "0",
    "msg": "OK",
    "time": "534",
    "data": [
        {
            "similarity": 1,
            "id": "430681198309180335",
            "id_type": "1",
            "image_url": "http://10.0.1.104:8080/photo/597b00ace24ca404264963b9",
            "id_card_image_url": "http://10.0.1.104:8080/photo/597b00ace24ca404264963bb",
            "name": "李智",
            "gender": "男",
            "birthday": "1983-07-27"
        }
    ]
    }   
    r = Response(json.dumps(data))
    r.headers["Content-Type"]="application/json,charset=utf-8"
    return r

@app.route('/rzp',methods=['GET','POST'])
def rzp():
    if request.method == 'GET':
#        time.sleep(5)
        id = request.args.get('gmsfzhm')
        if id in blacklist3suo:
            return '\"true\"'
        else:
            return '\"false\"' 

@app.route('/sjmpt/sjmxt/majorpeople/queryByCard',methods=['GET','POST'])
def sjmpt():
    if request.method == 'GET':
        idcard = request.args.get('crime_cardno')
        device_code = request.args.get('device_code')
        ret = {
       "crime_flag": "0",
       "crime_msg": "",
       "crime_deal": "",
       "police_name": "",
       "police_phone": ""
        }

        if idcard in sjmpt_idlist and device_code in device_list:
            ret["crime_flag"]="1"
            ret["crime_msg"]="违法犯罪"
            ret["crime_deal"]="就地抓捕"
            ret["police_name"]="王警官"
            ret["police_phone"]="13800138000"
        r = Response(json.dumps(ret))
        r.headers["Content-Type"]="application/json,charset=utf-8"
        return r
    else:
        postdata = json.loads(request.get_data())
        idcard = postdata.get("crime_cardno","")
        device_code = postdata.get("device_code","")
        ret = {
       "crime_flag": "0",
       "crime_msg": "",
       "crime_deal": "",
       "police_name": "",
       "police_phone": ""
        }

        if idcard in sjmpt_idlist and device_code in device_list:
            ret["crime_flag"]="1"
            ret["crime_msg"]="违法犯罪"
            ret["crime_deal"]="就地抓捕"
            ret["police_name"]="王警官"
            ret["police_phone"]="13800138000"
        r = Response(json.dumps(ret))
        r.headers["Content-Type"]="application/json,charset=utf-8"
        return r
@app.route('/post_dianke',methods=['GET','POST'])
def post_dianke():
    #print(request.method)
    if request.method == 'POST':
        #print('123')
        #print(request.headers)
        if not request.json:
            abort(400)
        else:
            #print(request.get_json())
            content = request.get_json()
            print(json.dumps(content))
            return '''{"code": 0,"msg": "success"}'''
    else:
        #abort(400)
        return '请使用post方法'    


if __name__ == '__main__':
 #   app.debug = True
 #   app.run(host='0.0.0.0',port = 5000)
    http_server = WSGIServer(('', 5001), app, handler_class=WebSocketHandler)
    http_server.serve_forever()

