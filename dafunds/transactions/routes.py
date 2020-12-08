# -*- coding: utf-8 -*-
from flask import render_template, url_for, redirect, request, flash, abort, Blueprint
from dafunds.transactions.forms import TransactForm
from dafunds.models import Vault, Transactions, System
from dafunds import db
from dafunds.payment import initiatepay, validatevpa
from flask_login import current_user, login_required

transactions_ = Blueprint('transactions', __name__)

@transactions_.route('/vault/<int:vault_id>/transact',methods=['POST','GET'])
@login_required
def transact(vault_id):
    form=TransactForm()
    vault = Vault.query.get_or_404(vault_id)
    if vault.user != current_user:
        abort(403)
    if form.validate_on_submit():
        tran_type=request.form.get('tran_type_opt')
        tran=Transactions(vault_id=vault_id,tran_type=tran_type,
                          amount=form.amount.data,remark=form.remark.data)
        db.session.add(tran)
        System.query.filter_by(key='pend_tran').first().value \
            =int(System.query.filter_by(key='pend_tran').first().value)+1
        db.session.commit()
        flash('Money success !', 'success')
        return redirect(url_for('bunker.vault',vault_id=vault_id))
        
    return render_template('transact.html',form=form,vault=vault,title='Transaction')    


    


@transactions_.route('/transact_cntl',methods=['GET','POST'])
@login_required
def transact_cntl():
    if request.method == 'POST':
        tran_stat = request.args.get('tran_stat')
        tran_id = request.args.get('tran_id')
        Transactions.query.get_or_404(tran_id).tran_stat=tran_stat
        System.query.filter_by(key='pend_tran').first().value \
            =int(System.query.filter_by(key='pend_tran').first().value)-1
        db.session.commit()
        flash(f'Transaction processed successfully !', 'success')
        
        return redirect(url_for('transactions.transact_cntl'))
    transacts=Transactions.query.filter_by(tran_stat=u'ST03').all()
    return render_template('transact_cntl.html',transacts=transacts,title='Transact_cntl')



@login_required
@transactions_.route('/payment',methods=['GET','POST'])
def payment():
    paydict={
    'tmid' : 'BcQNyT61707278565114',
    'tmkey' : 'JLBb5si@1KhcZ0wb',
    'torderId' : 'ORDERID_0012',
    'tvpa' : 'sshyamselvaraj@okhdfcbank',
    'tcallbackUrl' : url_for('transactions.callback')
    }
    
    response,_=initiatepay(paydict['tmid'],paydict['torderId'],paydict['tmkey'],paydict['tcallbackUrl'])
    
    if response['body']['resultInfo']['resultStatus'] == 'S':
        paydict.update(ttxnToken = response['body']['txnToken'])
        response2=validatevpa(paydict['tmid'],paydict['torderId'],paydict['ttxnToken'],paydict['tvpa'])
        flash(response['body']['resultInfo']['resultMsg'],'success')
    else:
        flash(response['body']['resultInfo']['resultMsg'],'failure')
        
    return render_template('payment.html',paydict=paydict,response=response,title='Payment')

@login_required
@transactions_.route('/payment_callback',methods=['GET','POST'])
def callback():
    flash('callback','failure')
    return render_template('home.html',title='Payment')