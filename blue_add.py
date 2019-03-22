from flask import Blueprint,request,g,flash,redirect,url_for,render_template
from forms import SuoForm,BlacklistForm,PersonForm,IdlistForm
bp = Blueprint('add',__name__,url_prefix='/add')
@bp.context_processor
def context_bp():
    blacklform = BlacklistForm()
    blacklist = g.db.execute('select * from blacklist')
    idcards = g.db.execute('select * from blacklist3suo')
    person = g.db.execute('select * from person')
    helu = g.db.execute('select * from blacklist_helu')
    idlist=g.db.execute('select * from idlist')
    jcz = g.db.execute('select * from blacklist_jcz')
    suoform = SuoForm()
    personform = PersonForm()
    idlistform= IdlistForm()
    context = {
        'idcards': idcards,
        'suoforms': suoform,
        'blacklform': blacklform,
        'blacklist': blacklist,
        'personform': personform,
        'person': person,
        'helu':helu,
        'jcz':jcz,
        'idlist':idlist,
        'idlistform':idlistform
    }
    return context
@bp.route('/',methods=['get'])
def index():
    if request.method =='GET':
        return render_template('index.html')

@bp.route('/suo3/',methods=['post'])
def suo3():
    #print request.form
    form = SuoForm(request.form)
    #print form.validate()
    if form.validate_on_submit():
        idcard = g.db.execute('select * from blacklist3suo where idcard=(?)', [form.idcard.data])
        idcard = idcard.fetchall()
        if idcard:
            return 'idcard is exist'
        g.db.execute('insert into blacklist3suo (idcard) values (?)',[form.idcard.data])
        g.db.commit()
        flash('new idcard was successfully posted')
        return redirect(url_for('add.index'))
    return str(form.errors).encode('gbk')
    # else:
    #     return str(form.errors).encode('gbk')

@bp.route('/blacklist/',methods=['post','get'])
def blacklist():
    if request.method == 'POST':
        form = BlacklistForm(request.form)
        if form.validate():
            idcard = g.db.execute('select * from blacklist where idcard=(?)', [form.idcard.data])
            idcard = idcard.fetchall()
            if idcard:
                return 'idcard is exist'
            g.db.execute('insert into blacklist (idcard,name,mac,imei,imsi,passport) values (?,?,?,?,?,?)',[form.idcard.data,form.name.data,form.mac.data,form.imei.data,form.imsi.data,form.passport.data])
            g.db.commit()
            flash('new blacklist was successfully posted')
            return redirect(url_for('add.index'))
        else:
            return str(form.errors).encode('gbk')
    else:
        return redirect(url_for('add.index'))
@bp.route('/person/',methods=['post','get'])
def person():
    if request.method == 'POST':
        #print request.form
        form = PersonForm(request.form)
        #print form
        if form.validate():
            idcard =g.db.execute('select * from person where idcard=(?)',[form.idcard.data])
            idcard = idcard.fetchall()
            if idcard:
                return 'idcard is exist'
            g.db.execute('insert into person (idcard,name,sex,birthday,nationality,nation,address,passport_type,passport_id,score,image) values (?,?,?,?,?,?,?,?,?,?,?)',[form.idcard.data,form.name.data,form.sex.data,form.birthday.data,form.nationality.data,form.nation.data,form.address.data,form.passport_type.data,form.passport_id.data,form.score.data,form.image.data])
            g.db.commit()
            flash('new person was successfully posted')
            return redirect(url_for('add.index'))
        else:
            return str(form.errors).encode('gbk')
    else:
        return redirect(url_for('add.index'))
@bp.route('/helu/',methods=['post','get'])
def helu():
    if request.method=="POST":
        form = SuoForm(request.form)
        if form.validate():
            idcard = g.db.execute('select * from blacklist_helu where idcard=(?)',[form.idcard.data])
            idcard=idcard.fetchall()
            if idcard:
                return 'idcard is exist'
            g.db.execute('insert into blacklist_helu (idcard) values (?)',[form.idcard.data])
            g.db.commit()
            flash('new helu was successfully posted')
            return redirect(url_for('add.index'))
        return redirect(url_for('add.index'))
    return redirect(url_for('add.index'))
@bp.route('/jcz/',methods=['post','get'])
def jcz():
    if request.method =="POST":
        form =SuoForm(request.form)
        if form.validate():
            idcard= g.db.execute('select * from blacklist_jcz where idcard=(?)',[form.idcard.data])
            idcard=idcard.fetchall()
            if idcard:
                return 'idcard is exist'
            g.db.execute('insert into blacklist_jcz (idcard) values (?)',[form.idcard.data])
            g.db.commit()
            flash('new jcz was successfully posted')
            return redirect(url_for('add.index'))
        flash(form.errors)
        return redirect(url_for('add.index'))
    return redirect(url_for('add.index'))
@bp.route('/idlist/',methods=['post','get'])
def idlist():
    if request.method=="POST":
        form=IdlistForm(request.form)
        if form.validate():
            idcard=g.db.execute('select * from idlist where idcard=(?)',[form.idcard.data])
            idcard=idcard.fetchall()
            if idcard:
                return 'idcard is exist'
            g.db.execute('insert into idlist (idcard,name,img) values (?,?,?)',[form.idcard.data,form.name.data,form.img.data])
            g.db.commit()
            flash('new idlist was successfully posted')
            return redirect(url_for('add.index'))
        return redirect(url_for('add.index'))
    return redirect(url_for('add.index'))