#coding:utf8
from flask import Flask,request,render_template,Response,g,abort,make_response
import json
import time
import random
from geventwebsocket.handler import WebSocketHandler
from gevent.pywsgi import WSGIServer
from contextlib import closing
from modules import getIMGFromID,getNameFromID,searchFile,getIDbyImei,getIDbyMac,getIDbyImsi,getColorFromID,getTypeFromID,base64tojpg,getIDFromResult
import sqlite3
from gevent import monkey
from blue_add import bp as addbp
from blue_del import bp as delbp
import logging
vacationlist = ['410181198905081535','22028219931203411XTTT','61032319911025001','430681198309180335','G31035926']
inBlackListData = {"status":"0","message":"success","jobId":"CC0000005963AD750159721904E33780","isBlackList":1}
outBlackListData = {"status":"0","message":"success","jobId":"CC0000005963AD750159721904E33780","isBlackList":0}
data1v1 = {"status":"0","message":"成功","data":[]}
monkey.patch_all()
app = Flask(__name__)
#db.init_app(app)
app.config.from_pyfile('config.py')
def connect_db():
    app.logger.info(app.config['DATABASE'])
    return sqlite3.connect(app.config['DATABASE'])

@app.before_first_request
def init_db():
    with closing(connect_db()) as db:
        with app.open_resource('schema.sql') as f:
            db.cursor().executescript(f.read().decode())
        db.commit()
@app.before_request
def before_request():
    g.db=connect_db()

@app.teardown_request
def teardown_request(exception):
    db = getattr(g,'db',None)
    if db is not None:
        db.close()



@app.route('/3suo/', methods=['GET', 'POST'])
def template3suo():
    if request.method == 'POST':
#        time.sleep(5)
#        print "request data is %s"%request.get_data()
        postdata = json.loads(request.get_data())
        id = postdata.get('cardNo',"")
        idcard =g.db.execute('select idcard from blacklist3suo where idcard={0}'.format(id))
        if id == idcard:
#            print inBlackListData
            return json.dumps(inBlackListData)
        else:
            return json.dumps(outBlackListData)
    else:
        return '200 ok'
number = 0
@app.route('/3hui', methods=['GET', 'POST'])
def template3hui():
    if request.method == 'GET':
#       time.sleep(5)
        global number
        number += 1
        blacklist = g.db.execute('select * from blacklist')
        idcard =g.db.execute('select idcard from blacklist')
        mac =g.db.execute('select mac from blacklist')
        imei =g.db.execute('select imei from blacklist')
        imsi =g.db.execute('select imsi from blacklist')
        app.logger.info("%s - NO.%d"%(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())),number))
#        app.logger.info('%d'%number)
        ids = request.args.get('id')
#        print ids
        datalist = {"msg":u"品恩、海康身份证接口调用成功!","data":[]}
        if ids is None or len(ids) <1:

            return "Notice:none input"
#        print "id length is %d"%len(ids)
        for id in ids.split(','):
#            print "id length is %d"%len(ids)
            if id in idcard:
                sanhuiinBlacklistData = {"id":id,"message":u"布控信息:进一步落地监控，防止造成危害%s"%id,"tag":u"Tag:一体化录入人员%s"%id,\
                "flag":('1' if getIDbyMac(id,blacklist) in vacationlist else '0'),"reserved1":u"布控标签res1%s"%id,"reserved2":u"处置意见:res2发现即抓捕%s，同时通知原籍公安机关"%id,"reserved3":"res3","reserved4":"idcard","reserved5":"null"}
                datalist["data"].append(sanhuiinBlacklistData)
            elif id in mac:
#            elif id.find(':')>0:
                sanhuiinBlacklistData = {"id":id,"message":u"进一步落地监控，防止造成危害","tag":u"一体化录入人员",\
                "flag":"0","reserved1":u"不放心人员","reserved2":u"信息采集","reserved3":getIDbyMac(id,blacklist),"reserved4":"mac","reserved5":"res5"}
                datalist["data"].append(sanhuiinBlacklistData)
            elif id in imei:
                sanhuiinBlacklistData = {"id":id,"message":u"进一步落地监控，防止造成危害","tag":u"[一体化录入人员]的同家族人员|一体化录入人员|不准出境人员|危安管控对象",\
                "flag":"","reserved1":u"一体化布控","reserved2":u"发现即抓捕，同时通知原籍公安机关","reserved3":getIDbyImei(id,blacklist),"reserved4":"imei","reserved5":'"null"'}
                datalist["data"].append(sanhuiinBlacklistData)
            elif id in imsi:
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
        #print(key)
        if key is None or len(key)<1:
            return "Notice:none input"

        datalist = {"color":"","type":""}
        # print key
        # print blacklisthelu
        blacklist_helu = g.db.execute('select idcard from blacklist_helu')
        if key in blacklist_helu:
            datalist["color"] = getColorFromID(key,blacklist_helu)
            datalist["type"] = getTypeFromID(key,blacklist_helu)
        else:
            datalist = {"color":"none"}
   # return json.dumps(datalist,ensure_ascii=False)
        r = Response(json.dumps(datalist,ensure_ascii=False))
        r.headers["Content-Type"]="application/json"
        return r

@app.route('/jcz',methods=['GET', 'POST'])
def templatejcz():
    if request.method == 'GET':
        time.sleep(1)
        key = request.args.get('key')
        #print(key)
        if key is None or len(key)<1:
            return "Notice:none input"

        datalist = {"color":"","type":""}
       # print key
       # print blacklisthelu
        blacklist_jcz= g.db.execute('select idcard from blacklist_jcz')
        if key in blacklist_jcz:
            datalist["color"] = getColorFromID(key,blacklist_jcz)
            datalist["type"] = getTypeFromID(key,blacklist_jcz)
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


        #blacklist = g.db.execute('select * from blacklist')
        idcard = g.db.execute('select idcard from blacklist')
        passport = g.db.execute('select passport from blacklist')
        if type==0:           #身份证
            for id in ids:
                if id in idcard:
    #                print id
                    sanhuiinBlacklistData = {"id":id,"message":u"进一步落地监控，防止造成危害","tag":u"[一体化录入人员]的同家族人员|一体化录入人员|不准出境人员|危安管控对象",\
                    "flag":('1' if id in vacationlist else '0'),"reserved1":u"一体化布控","reserved2":u"发现即抓捕，同时通知原籍公安机关","reserved3":"","reserved4":"idcard","reserved5":""}
                    datalist["data"].append(sanhuiinBlacklistData)
        elif type==1:         #护照
            for id in ids:
                if id in passport:
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
        dataPerson = g.db.execute('select * from person')
        idlist = g.db.execute('select * from idlist')
        ids = getIDFromResult(ret,count)
        for i in range(0,count):
            dataPerson[i]['id'] = ids[i]['id']
            dataPerson[i]['name'] = getNameFromID(ids[i]['id'],idlist)
            dataPerson[i]['image'] = getIMGFromID(ids[i]['id'],idlist)
            dataPerson[i]['score'] = ids[i]['score']*100
            data1v1["data"].append(dataPerson[i])
        #print(data1v1)
        r = Response(json.dumps(data1v1))
        r.headers["Content-Type"]="application/json,charset=utf-8"
        return r

@app.route('/1vnFake', methods=['GET', 'POST'])
def template1vnFake():
    if request.method == 'POST':
#        time.sleep(15)
#        print 'start to get haikang fake'
        data1v1["data"] = []
        postdata = json.loads(request.get_data())
#        print postdata
        count = postdata.get('count',1)
#        faceImg = postdata.get('faceImg',"")
#        print 'count is %d'%count
#        base64tojpg(faceImg,'test.jpg')
#        ret = searchFile('test.jpg',count)
        #print ret
        ids = [{'id':'430681198309180335','score':85.22},{'id':'410181198905081535','score':70.1},{'id':'22028219931203411X','score':55.1}]
        dataPerson = g.db.execute('select * from person')
        idlist = g.db.execute('select * from idlist')
        for i in range(count):
            dataPerson[i]['id'] = ids[i]['id']
            dataPerson[i]['name'] = getNameFromID(ids[i]['id'],idlist)
            dataPerson[i]['image'] = getIMGFromID(ids[i]['id'],idlist)
            dataPerson[i]['score'] = ids[i]['score']
            data1v1["data"].append(dataPerson[i])
#        print data1v1
#        datatest = {"status":"0","message":"成功","data":[{"name":"李"}]}

        r = Response(json.dumps(data1v1,ensure_ascii=False))
#        r = Response("test")
#        r = Response(json.dumps(datatest,ensure_ascii=False))
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
@app.route('/post_dianke',methods=['GET','POST'])
def post_dianke():
    if request.method == 'POST':
        if not request.json:
            abort(400)
        else:
            content = request.get_json()
            #parameters = ['3d_1v1_class1', 'address', 'birthdate', 'flag', 'capture_image', 'capture_time', 'end_date', 'idcard_image', 'identity', 'is_a_person', 'is_alarm', 'message', 'name', 'nation', 'reserved1', 'reserved2', 'reserved3', 'reserved4', 'reserved5', 'serial_number', 'sex', 'start_date', 'tag', 'uuid', 'similarity_person', 'equipment_id']
            required_paramerters = ['name','sex','nation','identity','address','capture_time',
                                    'serial_number','is_a_person','is_alarm','_3d_1vn',
                                    'capture_image','idcard_image','equipment_id']
            content_keys = content.keys()
            for i in content_keys:
                if i in required_paramerters:
                    required_paramerters.remove(i)
            if len(required_paramerters) !=0:
                    app.logger.error("{} parmeters not exit".format(str(required_paramerters).strip(']').strip('[')))
                    sl = '''{"code": 1005,"msg": "%s parmeters are to be required field"}'''%(required_paramerters)
                    res = make_response(sl)
                    return res

            if type(content['is_alarm']) is int and content['is_alarm'] >0:
                is_alarm_paramerters = ['uuid','flag','tag','message','reserved1','reserved2','reserved3','reserved4','reserved5']
                for key in content_keys:
                    if key in is_alarm_paramerters:
                        is_alarm_paramerters.remove(key)
                if len(is_alarm_paramerters) !=0:
                    app.logger.error('{} parmeters are to be required field when is_alarm >0'.format(str(is_alarm_paramerters).strip(']').strip('[')))
                    return '''{"code": 1005,"msg": "%s parmeters are to be required field when is_alarm>0."}'''%(is_alarm_paramerters)
                else:
                    pass

            if type(content['_3d_1vn']) is int and content['_3d_1vn']==2:
                _3d_1vn_paramerters='similarity_person'
                if _3d_1vn_paramerters not in content_keys:
                    app.logger.error('{} parmeter is to be required field when _3d_1vn=2'.format(_3d_1vn_paramerters))
                    return '''{"code": 1005,"msg": "%s parmeter is to be required field when _3d_1vn=2}"'''%(_3d_1vn_paramerters)
                else:
                    pass

            app.logger.info('{}'.format(json.dumps(content)))
            return '''{"code": 0,"msg": "success"}'''
    else:

        abort(400)

app.register_blueprint(addbp)
app.register_blueprint(delbp)
#print(app.url_map)
if __name__ == '__main__':
    app.debug = app.config['DEBUG']
    handler = logging.FileHandler(app.config['LOG_PATH'])
    app.logger.addHandler(handler)
    app.run(host='0.0.0.0',port =5001)
    #http_server = WSGIServer(('0.0.0.0', 5003), app, handler_class=WebSocketHandler)
    #http_server.serve_forever()

