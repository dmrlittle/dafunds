# -*- coding: utf-8 -*-
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length


class CreateVaultForm(FlaskForm):
    name = StringField("Vault's Name",validators=[DataRequired(),Length(max=20)])
    submit = SubmitField('Build')