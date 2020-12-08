# -*- coding: utf-8 -*-
from flask import render_template, url_for, redirect, request, flash, abort, Blueprint
from dafunds.fortress.forms import CreateTreasuryForm
from dafunds.models import User, Treasury
from dafunds import db
from flask_login import current_user, login_required

fortress_ = Blueprint('fortress', __name__)

@fortress_.route('/fortress',methods=['POST','GET'])
@login_required
def fortress():
    form=CreateTreasuryForm()
    vaults=User.query.get(current_user.id).vaults
    if form.validate_on_submit():
        vault_name_opt=request.form.get('vault_name_opt')
        treasury=Treasury(code=form.code.data)
        db.session.add(treasury)
        db.session.commit()
        for vault in vaults:
            if(vault.id==int(vault_name_opt)):
                flash(f'Treasury has been built successfully ! {vault.treasury}', 'success')
                vault.treasury_id=treasury.id
        db.session.commit()
        #flash(f'Treasury has been built successfully ! {vault_name_opt}', 'success')
        return redirect(url_for('fortress.fortress'))
    return render_template('fortress.html',vaults=vaults,form=form,title='Fortress')

@fortress_.route('/treasury/<int:treasury_id>',methods=['GET','POST'])
@login_required
def treasury(treasury_id):
    treasury = Treasury.query.get_or_404(treasury_id)
    for vault in treasury.vaults:
        if(vault.user == current_user):
            break
    else:
        abort(403)
        
    return render_template('treasury.html',treasury=treasury,title='Treasury')