# -*- coding: utf-8 -*-
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length

class CreateTreasuryForm(FlaskForm):
    code = StringField("Treasury's Name",validators=[DataRequired(),Length(max=20)])
    #basevault = StringField("Vault's Name",validators=[DataRequired(),Length(max=20)])
    submit = SubmitField('Build')