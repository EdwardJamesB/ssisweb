from flask_wtf import FlaskForm
from wtforms import StringField, validators, SubmitField, SelectField
import app.models.college as models


class collegeForm(FlaskForm):
    code = StringField("Code", [validators.DataRequired()])
    name = StringField("Name", [validators.DataRequired()])
    submit = SubmitField("Submit")