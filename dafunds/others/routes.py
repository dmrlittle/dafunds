# -*- coding: utf-8 -*-
from flask import render_template, url_for, redirect, request, flash, Blueprint
from dafunds.models import System
from dafunds import db
from flask_login import current_user, login_required

others_ = Blueprint('others', __name__)

@others_.route('/')
@others_.route('/home')
def home():
    return render_template('home.html')

@others_.route("/spell",methods=['GET','POST'])
@login_required
def spell():
    spelldict={"colovaria aurum":"VIP1",
               "colovaria aqua":"VIP2",
               "aurum reverte":"ROLE",
               "avada kedavra":"XXX"}
    spells=request.form.getlist('spellcaster')
    for j in spells:
        j=j.lower()
        if (j in spelldict.keys()) and spelldict[j]=='VIP1':
            current_user.items.update(VIP='warning')
        elif (j in spelldict.keys()) and spelldict[j]=='VIP2':
            current_user.items.update(VIP='primary')
        elif (j in spelldict.keys()) and spelldict[j]=='ROLE':
            if(System.query.filter_by(key='gardian').first().value == '0'):
                System.query.filter_by(key='gardian').first().value=current_user.id
            elif System.query.filter_by(key='gardian').first().value == str(current_user.id):
                System.query.filter_by(key='gardian').first().value='0'
            else:
                flash('Somebody has chanted counter spell !','danger')
                break
        elif (j in spelldict.keys()) and spelldict[j]=='XXX':
            current_user.items.clear()
        else:
            break
        flash(f'Spell Activation Complete !', 'primary')
        db.session.commit()
            
    return redirect(url_for('bunker.bunker'))

@others_.context_processor
def inject_check():
    def syscheck(val1,val2):
        if System.query.filter_by(key=val1).first().value == str(val2) :
            return True
        return False
    def sysget(val1):
        return System.query.filter_by(key=val1).first().value
 
    return dict(syscheck=syscheck,sysget=sysget)