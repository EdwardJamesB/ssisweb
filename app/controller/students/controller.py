from flask import render_template, request, redirect, url_for
from . import student
from app.controller.students.forms import StudentForm
import app.models.student as StudentModel
import app.models.course as CourseModel
import app.models.college as CollegeModel
from app.cloudinary_config import cloudinary
import cloudinary.uploader

# Show list of students
@student.route('/', endpoint='index')
def index():
    keyword = request.args.get('keyword', default='', type=str)
    sort_order = request.args.get('sort', 'asc')
    sort_by = request.args.get('sort_by', 'student_id')  # Default sort
    students = StudentModel.Students.all(keyword, sort_order, sort_by)
    return render_template('student/student.html', students=students, sort_order=sort_order, sort_by=sort_by)

# Create student
@student.route('/create', methods=['GET', 'POST'])
def create():
    form = StudentForm()

    # Populate dropdowns
    form.gender.choices = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Prefer not to say', 'Prefer not to say')
    ]
    form.year.choices = [
        ('1st Year', '1st Year'),
        ('2nd Year', '2nd Year'),
        ('3rd Year', '3rd Year'),
        ('4th Year', '4th Year')
    ]
    form.college.choices = [("", "-- Please select a college --")] + [
        (str(c['id']), c['name']) for c in CollegeModel.Colleges.all()
    ]
    form.course.choices = [("", "-- Please select a course --")] + [
        (c["code"], f'{c["code"]} - {c["name"]}') for c in CourseModel.Courses.all()
    ]

    if request.method == 'POST' and form.validate():
        student = StudentModel.Students(
            student_id=form.student_id.data,
            firstname=form.firstname.data,
            lastname=form.lastname.data,
            gender=form.gender.data,
            course=form.course.data,  
            year=form.year.data
        )
        student.add()
        return redirect(url_for('.index'))
    
    if request.method == 'POST' and form.validate():
        image_url = None
        if form.profile_pic.data:
            upload_result = cloudinary.uploader.upload(form.profile_pic.data)
            image_url = upload_result['secure_url']

        student = StudentModel.Students(
            student_id=form.student_id.data,
            firstname=form.firstname.data,
            lastname=form.lastname.data,
            gender=form.gender.data,
            course=form.course.data,
            year=form.year.data,
            image_url=image_url
        )
        student.add()
        return redirect(url_for('.index'))

    return render_template('student/create.html', form=form)

# Edit student
@student.route('/edit/<string:student_id>', methods=['GET'])
def edit(student_id):
    student = StudentModel.Students.edit(student_id)
    if not student:
        return redirect(url_for('.index'))

    form = StudentForm()

    # Assign the current values from the database
    form.student_id.data = student[0]
    form.firstname.data = student[1]
    form.lastname.data = student[2]
    form.gender.data = student[3]
    form.course.data = student[4]
    form.year.data = student[5]

    # Repopulate dropdown choices
    form.gender.choices = [('Male', 'Male'), ('Female', 'Female'), ('Prefer not to say', 'Prefer not to say')]
    form.year.choices = [('1st Year', '1st Year'), ('2nd Year', '2nd Year'), ('3rd Year', '3rd Year'), ('4th Year', '4th Year')]
    form.course.choices = [("", "-- Please select a course --")] + [
        (c["code"], f'{c["code"]} - {c["name"]}') for c in CourseModel.Courses.all()
    ]

    return render_template('student/edit.html', form=form, student_id=student_id)

@student.route('/update/<string:student_id>', methods=['POST'])
def update(student_id):
    form = StudentForm()

    # Repopulate choices
    form.course.choices = [(c['code'], c['name']) for c in CourseModel.Courses.all()]
    form.year.choices = [('1st Year', '1st Year'), ('2nd Year', '2nd Year'), ('3rd Year', '3rd Year'), ('4th Year', '4th Year')]
    form.college.choices = [(c['code'], c['name']) for c in CollegeModel.Colleges.all()]
    
    # Get data
    firstname = request.form.get('firstname')
    lastname = request.form.get('lastname')
    gender = request.form.get('gender')
    course = request.form.get('course')
    year = request.form.get('year')
    remove_pic = request.form.get('remove_pic')  # checkbox

    image_url = form.image_url.data  # current image

    file = request.files.get('profile_pic')
    if file and file.filename:
        result = cloudinary.uploader.upload(file, folder="students")
        image_url = result.get('secure_url')
    elif remove_pic:  # checkbox checked
        image_url = None

    StudentModel.Students.update(
        student_id=student_id,
        firstname=firstname,
        lastname=lastname,
        gender=gender,
        course=course,
        year=year,
        image_url=image_url
    )

    return redirect(url_for('student.index'))

# Delete student
@student.route('/delete', methods=['POST'])
def delete():
    student_id = request.form['student_id']
    StudentModel.Students.delete(student_id)
    return redirect(url_for('.index'))
