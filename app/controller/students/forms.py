from flask_wtf import FlaskForm
from wtforms import StringField, SelectField
from wtforms.validators import DataRequired

class StudentForm(FlaskForm):
    student_id = StringField('Student ID', validators=[DataRequired()])
    firstname = StringField('First Name', validators=[DataRequired()])
    lastname = StringField('Last Name', validators=[DataRequired()])
    gender = SelectField('Gender', choices=[('Male', 'Male'), ('Female', 'Female')], validators=[DataRequired()])
    course = SelectField('Course', coerce=str, validators=[DataRequired()])
    year = SelectField('Year Level', choices=[('1st Year', '1st Year'), ('2nd Year', '2nd Year'),
                                               ('3rd Year', '3rd Year'), ('4th Year', '4th Year')], validators=[DataRequired()])
    college = SelectField('College', coerce=str, validators=[DataRequired()])