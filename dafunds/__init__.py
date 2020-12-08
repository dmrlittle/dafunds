# -*- coding: utf-8 -*-

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from dafunds.config import Config
from flask_bcrypt import Bcrypt


db=SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'
login_manager.login_message = 'Login to access !'


def create_app(config_class=Config,first_time=False):
    app = Flask(__name__)
    app.config.from_object(Config)
    
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    
    from dafunds.users.routes import users_
    from dafunds.bunker.routes import bunker_
    from dafunds.fortress.routes import fortress_
    from dafunds.transactions.routes import transactions_
    from dafunds.others.routes import others_
    
    app.register_blueprint(users_)
    app.register_blueprint(bunker_)
    app.register_blueprint(fortress_)
    app.register_blueprint(transactions_)
    app.register_blueprint(others_)
    
    from dafunds.models import System
    @app.context_processor
    def inject_check():
        def syscheck(val1,val2):
            if System.query.filter_by(key=val1).first().value == str(val2) :
                return True
            return False
        def sysget(val1):
            return System.query.filter_by(key=val1).first().value
     
        return dict(syscheck=syscheck,sysget=sysget)
    
    return app

    