from flask import render_template, request, redirect, url_for
from . import student
from app.controller.students.forms import StudentForm
import app.models.student as StudentModel
import app.models.course as CourseModel

# Show list of students
@student.route('/', endpoint='index')
def index():
    keyword = request.args.get('keyword', default='', type=str)
    sort_order = request.args.get('sort', 'asc')
    students = StudentModel.Students.all(keyword, sort_order)
    return render_template('student/student.html', students=students, sort_order=sort_order)


# Create student
@student.route('/create', methods=['GET', 'POST'])
def create():
    form = StudentForm()

    # Dynamically populate course choices
    courses = CourseModel.Courses.all()
    form.course.choices = [(c['id'], c['name']) for c in courses]

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

    return render_template('student/create.html', form=form)

# Edit student
@student.route('/edit/<string:student_id>', methods=['GET'])
def edit(student_id):
    student = StudentModel.Students.edit(student_id)
    if not student:
        return redirect(url_for('.index'))

    return render_template('student/edit.html', data=student)

# Update student
@student.route('/update/<string:student_id>', methods=['POST'])
def update(student_id):
    form = request.form
    StudentModel.Students.update(
        student_id=student_id,
        firstname=form['firstname'],
        lastname=form['lastname'],
        gender=form['gender'],
        course=form['course'],
        year=form['year']
    )
    return redirect(url_for('.index'))

# Delete student
@student.route('/delete', methods=['POST'])
def delete():
    student_id = request.form['student_id']
    StudentModel.Students.delete(student_id)
    return redirect(url_for('.index'))
