from flask_wtf import FlaskForm
from wtforms import StringField, SelectField
from wtforms.validators import DataRequired

class StudentForm(FlaskForm):
    student_id = StringField('Student ID', validators=[DataRequired()])
    firstname = StringField('First Name', validators=[DataRequired()])
    lastname = StringField('Last Name', validators=[DataRequired()])
    gender = SelectField(
        'Gender',
        choices=[
            ('Male', 'Male'),
            ('Female', 'Female'),
            ('Prefer not to say', 'Prefer not to say')
        ],
        validators=[DataRequired()]
    )
    course = SelectField('Course', coerce=str, validators=[DataRequired()])
    year = SelectField(
        'Year Level',
        choices=[
            ('1', '1st Year'),
            ('2', '2nd Year'),
            ('3', '3rd Year'),
            ('4', '4th Year')
        ],
        validators=[DataRequired()]
    )
