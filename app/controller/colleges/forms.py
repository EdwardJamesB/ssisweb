from flask_wtf import FlaskForm
from wtforms import StringField, validators, SubmitField, SelectField, HiddenField
import app.models.college as models
class CollegeForm(FlaskForm):
    code = StringField("Code", [validators.DataRequired()])
    name = StringField("Name", [validators.DataRequired()])
    submit = SubmitField("Submit")
class DeleteCollegeForm(FlaskForm):
    id = HiddenField("ID", [validators.DataRequired()])