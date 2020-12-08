# -*- coding: utf-8 -*-
 
 import os


class Config:
    SECRET_KEY = '529c33dc8e0e0345bf796eaa928bf44e'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DB_URI')
    #MAIL_SERVER = 'smtp.googlemail.com'
    #MAIL_PORT = 587
    #MAIL_USE_TLS = True
    #MAIL_USERNAME = os.environ.get('EMAIL_USER')
    #MAIL_PASSWORD = os.environ.get('EMAIL_PASS')
