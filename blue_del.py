from flask import Blueprint,request,g,redirect,url_for,flash
bp = Blueprint('del',__name__,url_prefix='/del')
@bp.route('/suo3/',methods=['post'])
def suo3():
    #print request.form,request.form.get('id')
    id = request.form.get('id')
    g.db.execute('delete  from blacklist3suo where id=(?)',[id])
    g.db.commit()
    flash('delete 3suo  id:{0} succeeded'.format(id))
    return redirect(url_for('add.index'))
@bp.route('/person/',methods=['post'])
def person():
    #print request.form
    idcard = request.form.get('id')
    #print idcard
    g.db.execute('delete from person where idcard=(?)',[idcard])
    g.db.commit()
    flash('delete person  idcard:{0} succeeded'.format(idcard))
    return redirect(url_for('add.index'))
@bp.route('/blacklist/',methods=['post'])
def blacklist():
    id = request.form.get('id')
    g.db.execute('delete from blacklist where id=(?)',[id])
    g.db.commit()
    flash('delete blacklist id:{} succeeded'.format(id))
    return redirect(url_for('add.index'))
@bp.route('/helu/',methods=['post'])
def helu():
    id = request.form.get('id')
    g.db.execute('delete from blacklist_helu where id=(?)',[id])
    g.db.commit()
    flash('delete blacklist_helu id:{} succeeded'.format(id))
    return redirect(url_for('add.index'))
@bp.route('/jcz/',methods=['post'])
def jcz():
    id = request.form.get('id')
    g.db.execute('delete from blacklist_jcz where id=(?)',[id])
    g.db.commit()
    flash('delete blacklist_jcz id:{} succeeded'.format(id))
    return redirect(url_for('add.index'))
@bp.route('/idlist/',methods=['post'])
def idlist():
    #print request.form
    idcard = request.form.get('id')
    #print idcard
    g.db.execute('delete from idlist where idcard=(?)',[idcard])
    g.db.commit()
    flash('delete idlist idcard:{} succeeded'.format(idcard))
    return redirect(url_for('add.index'))