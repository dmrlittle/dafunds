# -*- coding: utf-8 -*-

import json
from datetime import datetime
from dafunds import db,login_manager
from flask_login import UserMixin
from sqlalchemy_utils.types.choice import ChoiceType
from sqlalchemy.ext import mutable

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class DictEncoder(db.TypeDecorator):
    impl = db.Text
    
    def process_bind_param(self, value, dialect):
        if value is None:
            return '{}'
        else:
            return json.dumps(value)

    def process_result_value(self, value, dialect):
        if value is None:
            return {}
        else:
            return json.loads(value)

mutable.MutableDict.associate_with(DictEncoder)
    

class User(db.Model,UserMixin):
    __tablename__ = 'user'
    id=db.Column(db.Integer,primary_key=True)
    username=db.Column(db.String(20),unique=True,nullable=False)    
    email=db.Column(db.String(100),unique=True,nullable=False)    
    password=db.Column(db.String(60),nullable=False)
    vaults=db.relationship('Vault',backref='user')
    items=db.Column(DictEncoder)
    
    def __repr__(self):
        return f'{self.username},{self.email}'
        
class Vault(db.Model):
    __tablename__= 'vault'
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(20),unique=True,nullable=False)
    invault=db.Column(db.Float,nullable=False,default=0.0)
    incirculation=db.Column(db.Float,nullable=False,default=0.0)
    lock=db.Column(db.Boolean,nullable=False,default=False)
    user_id=db.Column(db.Integer,db.ForeignKey('user.id'),nullable=False)
    treasury_id=db.Column(db.Integer,db.ForeignKey('treasury.id'))
    treasury=db.relationship('Treasury',backref='vaults')
    transactions=db.relationship('Transactions',backref='vault')

    def __repr__(self):
        return f'{self.name},{self.treasury_id}'

class Transactions(db.Model):
    __tablename__= 'transactions'
    stat_types = {u'ST01': {'value': u'Success','color': "success"},
                  u'ST02': {'value': u'Failure','color': "danger"},
                  u'ST03': {'value': u'Processing','color': "secondary"},
                  u'ST04': {'value': u'Unknown','color': "warning"}}
    
    id=db.Column(db.Integer,primary_key=True)
    vault_id=db.Column(db.Integer,db.ForeignKey('vault.id'),nullable=False)
    tran_type=db.Column(db.String(2),nullable=False)
    amount=db.Column(db.Integer,nullable=False)
    remark=db.Column(db.String(20),nullable=False,default="ha ha")
    tran_date=db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    tran_stat=db.Column(db.String(10),nullable=False,default=u'ST03')
    cnf_date=db.Column(db.DateTime,default=None)
    cnf_user=db.Column(db.Integer,db.ForeignKey('treasury.id'),nullable=False,default=0)
    
class Treasury(db.Model):
    __tablename__ = 'treasury'
    id=db.Column(db.Integer,primary_key=True)
    code=db.Column(db.String(60),nullable=False)
    intreasury=db.Column(db.Float,nullable=False,default=0.0)
    incirculation=db.Column(db.Float,nullable=False,default=0.0)
    active=db.Column(db.Boolean,nullable=False,default=False)
    
    def __repr__(self):
        return f'{self.code}'
    
class Payment(db.Model):
    __tablename__='payment'
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(20),nullable=False, default='UPI')
    pay_id=db.Column(db.String(40),nullable=False,unique=True)
    qr=db.Column(db.String(20))
    
class System(db.Model):
    __tablename__ = 'system'
    id=db.Column(db.Integer,primary_key=True)
    key=db.Column(db.String(60),unique=True,nullable=False)
    value=db.Column(db.String(60),nullable=False,default='0')
    
    def __repr__(self):
        return f'{self.key,self.value}'
    
    
    
