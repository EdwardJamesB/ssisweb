from flask_wtf import FlaskForm
from wtforms import StringField, SelectField
from wtforms.validators import DataRequired
from flask_wtf.file import FileField, FileAllowed

class StudentForm(FlaskForm):
    student_id = StringField('Student ID', validators=[DataRequired()])
    firstname = StringField('First Name', validators=[DataRequired()])
    lastname = StringField('Last Name', validators=[DataRequired()])
    gender = SelectField('Gender', choices=[
        ('Male', 'Male'), 
        ('Female', 'Female'),
        ('Prefer not to say', 'Prefer not to say')
    ], validators=[DataRequired()])
    course = SelectField('Course', coerce=str, validators=[DataRequired()])
    year = SelectField('Year Level', coerce=str, validators=[DataRequired()])
    profile_pic = FileField('Profile Picture', validators=[
        FileAllowed(['jpg', 'jpeg', 'png'], 'Images only!')
    ])
    image_url = StringField()