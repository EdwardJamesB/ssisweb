from flask_wtf import FlaskForm
from wtforms import StringField, SelectField
from wtforms.validators import DataRequired

class CourseForm(FlaskForm):
    code = StringField('Course Code', validators=[DataRequired()])
    name = StringField('Course Name', validators=[DataRequired()])
    college = SelectField('College', coerce=str, validators=[DataRequired()])
