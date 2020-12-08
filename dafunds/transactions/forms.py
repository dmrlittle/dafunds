# -*- coding: utf-8 -*-
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FloatField
from wtforms.validators import DataRequired, Length

class TransactForm(FlaskForm):
    amount = FloatField("Amount",validators=[DataRequired()])
    #tran_type = RadioField('Type', choices=[(u'CR','CR'),(u'DB','DB')],validators=[DataRequired()])
    remark = StringField("Remark",validators=[DataRequired(),Length(max=20)])
    submit = SubmitField('Proceed')
