from flask_wtf import FlaskForm
from wtforms import StringField, SelectField
from wtforms.validators import DataRequired
from wtforms import HiddenField
class CourseForm(FlaskForm):
    code = StringField('Course Code', validators=[DataRequired()])
    name = StringField('Course Name', validators=[DataRequired()])
    college = SelectField('College', coerce=str, validators=[DataRequired()])

class DeleteCourseForm(FlaskForm):
    code = HiddenField('Course Code', validators=[DataRequired()])
