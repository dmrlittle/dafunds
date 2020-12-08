# -*- coding: utf-8 -*-
from run import app
from dafunds import db
from dafunds.models import System

with app.app_context():
    db.create_all()
    
    temp=[System(key="gardian"),
      System(key="pend_tran")]

    [ db.session.add(i) for i in temp if not System.query.filter_by(key=i.key).first() ]
    db.session.commit()


