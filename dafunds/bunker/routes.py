# -*- coding: utf-8 -*-
from flask import render_template, url_for, redirect, request, flash, abort, Blueprint
from dafunds.bunker.forms import CreateVaultForm
from dafunds.models import User, Vault
from dafunds import db
from flask_login import current_user, login_required

bunker_ = Blueprint('bunker', __name__)

@bunker_.route('/bunker',methods=['GET','POST'])
@login_required
def bunker():
    form=CreateVaultForm()
    vaults=User.query.get(current_user.id).vaults
    if form.validate_on_submit():
        vault=Vault(name=form.name.data,user_id=current_user.id)
        db.session.add(vault)
        db.session.commit()
        flash('Vault has been built successfully !', 'success')
        return redirect(url_for('bunker.bunker'))
    return render_template('bunker.html',form=form,vaults=vaults,title='Bunker')

@bunker_.route('/vault/<int:vault_id>',methods=['GET','POST'])
@login_required
def vault(vault_id):
    vault = Vault.query.get_or_404(vault_id)
    transactions = vault.transactions
    if vault.user != current_user:
        abort(403)
    if request.method == 'POST':
        if(request.form.get('lock_opt')=='Lock'):
            vault.lock=True
            flash('Vault door has been Locked !','success')
        else:
            vault.lock=False
            flash('Vault door has been Unlocked !','warning')
        db.session.commit()
        return redirect(url_for('bunker.vault',vault_id=vault_id))
    return render_template('vault.html',vault=vault,transactions=transactions,title='Vault')

@bunker_.route('/vault/<int:vault_id>/destroy',methods=['POST'])
@login_required
def destroy_vault(vault_id):
    vault = Vault.query.get_or_404(vault_id)
    if vault.user != current_user:
        abort(403)
    db.session.delete(vault)
    db.session.commit()
    flash('Your Vault has been destroyed !', 'success')
    return redirect(url_for('bunker.bunker'))
